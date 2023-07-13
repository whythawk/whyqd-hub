from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
import stripe
from uuid import uuid4

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.config import settings
from app.utilities import (
    send_failed_order_email,
    send_successful_order_processing_error_email,
    send_admin_successful_order_processing_error_email,
)


router = APIRouter()
stripe.api_key = settings.STRIPE_API_KEY


@router.get("/", response_model=List[schemas.Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all member orders.
    """
    orders = crud.order.get_multi_orders(db=db, user=current_user, skip=skip, limit=limit)
    return orders


@router.get("/all", response_model=List[schemas.SubscriptionInView])
def read_current_subscribers(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve all current subscribers.
    """
    return crud.subscription.get_multi(db=db, skip=skip, limit=limit)


@router.post("/create", response_model=schemas.Subscription)
def create_subscription(
    *,
    db: Session = Depends(deps.get_db),
    subscription_in: schemas.SubscriptionAdminCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve all current subscribers.
    """
    user = crud.user.get_by_email(db=db, email=subscription_in.subscriber)
    if not user:
        raise HTTPException(status_code=404, detail="Customer not found")
    subscription_in = schemas.SubscriptionCreate(
        **{
            "subscription_id": uuid4().hex,
            "subscription_event_type": schema_types.SubscriptionEventType.RENEWED,
            "subscription_type": subscription_in.subscription_type,
            "started": datetime.now(),
            "ends": subscription_in.ends,
            "override": subscription_in.override,
            "subscriber_id": user.id,
        }
    )
    return crud.subscription.create(db=db, obj_in=subscription_in)


@router.post("/order", response_model=schemas.StripeCheckoutRedirect)
def create_subscription_order(
    *,
    db: Session = Depends(deps.get_db),
    order: schemas.StripeCheckoutIntent,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    try:
        # Ensure customer id exists
        current_user = crud.order.set_customer_id(db=db, user=current_user)
        # Check products exist
        price_obj = crud.price.get(db=db, id=order.price_id)
        if not price_obj:
            raise HTTPException(status_code=404, detail="Product not found")
        # Create a subscription session
        checkout_session = stripe.checkout.Session.create(
            customer=current_user.customer_id,
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "quantity": 1,
                    "price": price_obj.id,
                }
            ],
            success_url=f"{settings.SERVER_HOST}/profile/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.SERVER_HOST}/pricing/",
        )
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=403, detail=str(e))
    # Provision an order
    # https://fastapi.tiangolo.com/tutorial/header-params/
    country_obj = crud.price.get_country(user_ip=order.ip)
    order_in = schemas.OrderCreate(
        **{
            "subscription_event_type": schema_types.SubscriptionEventType.PENDING,
            "subscription_type": price_obj.product.subscription,
            "currency": price_obj.currency,
            "amount": price_obj.per_annum,
            "checkout_id": checkout_session.id,
            "country_code": country_obj.country_short,
            "country_name": country_obj.country_long,
            "product_id": price_obj.product.id,
            "price_id": price_obj.id,
            "payer_id": current_user.id,
        }
    )
    crud.order.create(db=db, obj_in=order_in)
    # This redirect is used in the client
    return {"redirect": checkout_session.url}


@router.post("/stripe-account", response_model=schemas.StripeCheckoutRedirect)
def redirect_to_stripe_account(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Redirect a subscriber to their Stripe account
    """
    if not current_user.customer_id:
        raise HTTPException(status_code=404, detail="Customer account not found")
    # https://stripe.com/docs/billing/quickstart
    portalSession = stripe.billing_portal.Session.create(
        customer=current_user.customer_id,
    )
    return {"redirect": portalSession.url}


@router.post("/webhook", status_code=201)
async def webhook_received(*, db: Session = Depends(deps.get_db), request: Request) -> Any:
    # secret = "whsec_5b3fc08d6652f99518b1d23f2a69d52bc45a4c2b727291536534020f4f17ff66"
    secret = settings.STRIPE_WEBHOOK
    data = await request.body()
    stripe_signature = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload=data, sig_header=stripe_signature, secret=secret)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    # try:
    #     print("-------------------------------------------------------------------")
    #     print(f"Handling: {event.type} - {event.id}")
    #     print(f"Customer id: {event.data.object.customer}")
    #     print(f"Checkout id: {event.data.object.id}")
    #     print(f"Subscription id: {event.data.object.subscription}")
    #     print("-------------------------------------------------------------------")
    # except Exception as e:
    #     print("-------------------------------------------------------------------")
    if event.type in ["invoice.paid", "checkout.session.completed", "invoice.payment_failed"]:
        user = crud.user.get_by_customer_id(db=db, customer_id=event.data.object.customer)
        if not user:
            raise HTTPException(status_code=404, detail="Customer not found")
    # try:
    # Get the type of webhook event sent - used to check the status of PaymentIntents.
    if event.type == "invoice.payment_failed":
        print("-------------------------------------------------------------------")
        print("ORDER FAILED")
        print(event.type)
        print("-------------------------------------------------------------------")
        # The payment failed or the customer does not have a valid payment method.
        # Update their individual order - irrespective of the number of line-items - to let
        # the customer know they must fix things.
        order_obj = crud.order.get_latest_pending_order_for_failed_payment(db=db, user=user)
        if order_obj:
            crud.order.set_pending_to_failed(db=db, db_obj=order_obj, invoice_url=event.data.object.hosted_invoice_url)
        # It may be that no order object could be found, so we send an email regardless with the appropriate details
        if settings.EMAILS_ENABLED and user.email:
            send_failed_order_email(email_to=user.email, link_url=event.data.object.hosted_invoice_url)
        # print("-------------------------------------------------------------------")
        # print(event)
        # print("-------------------------------------------------------------------")
    elif event.type == "checkout.session.completed":
        # print("-------------------------------------------------------------------")
        # print("ORDER CHANGE")
        # print(event.type)
        # print("-------------------------------------------------------------------")
        # First event
        # Payment is successful and the subscription is created.
        # Update the Subscription checkout id with the new subscription id
        crud.order.set_pending_to_created(
            db=db, checkout_id=event.data.object.id, subscription_id=event.data.object.subscription
        )
    elif event.type == "invoice.paid":
        # print("-------------------------------------------------------------------")
        # print("ORDER PAYMENT")
        # print(event.type)
        # print("-------------------------------------------------------------------")
        # Payment event, created after the subscription is created
        # Continue to provision the subscription as payments continue to be made.
        # Store the status in your database and check when a user accesses your service.
        # This approach helps you avoid hitting rate limits.
        order_obj = crud.order.set_created_to_completed(
            db=db,
            subscription_id=event.data.object.subscription,
            charge_id=event.data.object.charge,
            invoice_url=event.data.object.hosted_invoice_url,
        )
        # Validation step ... if something goes wrong here, we got a problem
        if not order_obj:
            # First step... check if the user has previous completed orders and this is a renewal
            order_obj = crud.order.create_renewal_from_last_completed(
                db=db,
                user=user,
                subscription_id=event.data.object.subscription,
                charge_id=event.data.object.charge,
                invoice_url=event.data.object.hosted_invoice_url,
            )
        if not order_obj:
            # We have a problem we need to deal with as we can't reconcile the order
            # Send as an email to the administrator and to the customer ...
            if settings.EMAILS_ENABLED and user.email:
                send_successful_order_processing_error_email(
                    email_to=user.email, link_url=event.data.object.hosted_invoice_url
                )
            if settings.EMAILS_ENABLED:
                send_admin_successful_order_processing_error_email(customer_email=user.email, event_id=event.id)
            # print("-------------------------------------------------------------------")
            # print("ORDER FAILURE")
            # print(event.type)
            # print(event.data.object.charge)
            # print("-------------------------------------------------------------------")
            raise HTTPException(status_code=403, detail="Order can't be reconciled.")
        # Get start and end dates from first row of event lines data
        event_line = event.data.object.lines.data[0]
        subscription_type = crud.price.get(db=db, id=order_obj.price_id)
        subscription_in = schemas.SubscriptionCreate(
            **{
                "subscription_id": order_obj.subscription_id,
                "subscription_event_type": schema_types.SubscriptionEventType.RENEWED,
                "subscription_type": subscription_type.product.subscription,
                "started": datetime.fromtimestamp(event_line.period.start),
                "ends": datetime.fromtimestamp(event_line.period.end),
                "subscriber_id": user.id,
            }
        )
        crud.subscription.create(db=db, obj_in=subscription_in)
        # print("-------------------------------------------------------------------")
        # print("ORDER SUCCEEDED")
        # print(event.type)
        # print("-------------------------------------------------------------------")
    return {"status": "success"}
    # except Exception as e:
    #     print("-------------------------------------------------------------------")
    #     print(f"Event failed: {event.type} - {event.id}")
    #     print(str(e))
    #     print("-------------------------------------------------------------------")
    #     raise HTTPException(status_code=403, detail=str(e))


# @router.put("/member", response_model=schemas.UserCustodialProfile)
# def read_member_subscription(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_in: schemas.SearchEmail,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Read a member's subscription rights.
#     """
#     user = crud.user.get_by_email(db, email=user_in.email)
#     if not user:
#         raise HTTPException(
#             status_code=404, detail="The user with this username does not exist in the system",
#         )
#     return user


# @router.post("/member", response_model=schemas.UserCustodialProfile)
# def update_member_subscription(
#     *,
#     db: Session = Depends(deps.get_db),
#     subscription_in: schemas.SubscriptionUpdate,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Update a member's subscription rights.
#     """
#     subscription = crud.subscription.get(db, id=subscription_in.id)
#     if not subscription:
#         raise HTTPException(
#             status_code=404, detail="This subscription does not exist in the system",
#         )
#     subscription = crud.subscription.update(db, db_obj=subscription, obj_in=subscription_in)
#     return subscription.subscriber
