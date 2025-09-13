from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
from pathlib import Path
import IP2Location

from app.core.config import settings
from .base import CRUDBase
from app.models.price import Price, Product
from app.schemas.price import CountryCode, IPCode, PriceCreate, PriceUpdate
from app.schemas.product import ProductCreate, ProductUpdate, ProductPricingView
from app.schema_types.currency import CurrencyType
from app.schema_types.subscription import SubscriptionType

IP2_PATH = Path(f"/app/{settings.IP2_FOLDER}/{settings.IP2_BIN_FILE}")
IP2_BASE = IP2Location.IP2Location(IP2_PATH, "SHARED_MEMORY")


class CRUDPrice(CRUDBase[Price, PriceCreate, PriceUpdate]):
    def get_country(self, user_ip: str) -> CountryCode:
        return IP2_BASE.get_all(user_ip)

    def get_by_ip(self, db: Session, code: IPCode) -> List[ProductPricingView]:
        iso_code = "US"
        currency = CurrencyType.USD
        if code.ip:
            iso_code = IP2_BASE.get_country_short(code.ip)
        if iso_code == "US":
            currency = CurrencyType.USD
        if iso_code == "UK":
            currency = CurrencyType.GBP
        if iso_code in settings.EURO_CURRENCY:
            currency = CurrencyType.EUR
        products = {}
        price_set = db.query(self.model).filter(self.model.currency == currency).all()
        for p in price_set:
            if p.product:
                product = products.get(p.product.name, ProductPricingView.model_validate(p.product))
                product.currency = currency
                if p.per_annum > 0:
                    product.per_annum = PriceUpdate(**{"id": p.id, "currency": currency, "per_annum": p.per_annum})
                if p.per_month > 0:
                    product.per_month = PriceUpdate(**{"id": p.id, "currency": currency, "per_month": p.per_month})
                products[p.product.name] = product
        return list(products.values())


price = CRUDPrice(Price)


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_subscription_type(self, db: Session, *, subscription_type: SubscriptionType) -> Product:
        return db.query(self.model).filter(self.model.subscription == subscription_type).first()

    def _append_price(self, db: Session, *, db_obj: Product, price_obj: Price) -> Product:
        db_obj.prices.append(price_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def _remove_price(self, db: Session, *, db_obj: Product, price_obj: Price) -> Product:
        db_obj.prices.remove(price_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def _remove_all(self, db: Session) -> None:
        objs = db.query(self.model).all()
        for obj in objs:
            for p_obj in obj.prices:
                db.delete(p_obj)
            db.delete(obj)
        db.commit()

    def _initialise(self, db: Session) -> None:
        for subscription in SubscriptionType:
            product_in = ProductCreate(
                **{
                    "id": uuid4().hex,
                    "name": subscription.value.title(),
                    "description": subscription.value.title(),
                    "subscription": subscription,
                }
            )
            product_obj = self.create(db=db, obj_in=product_in)
            for currency in CurrencyType:
                # Per month
                price_in = PriceCreate(**{"id": uuid4().hex, "currency": currency, "per_month": 1000, "per_annum": 0})
                price_obj = price.create(db=db, obj_in=price_in)
                product_obj = self._append_price(db=db, db_obj=product_obj, price_obj=price_obj)
                # Per year
                price_in = PriceCreate(**{"id": uuid4().hex, "currency": currency, "per_month": 0, "per_annum": 100000})
                price_obj = price.create(db=db, obj_in=price_in)
                product_obj = self._append_price(db=db, db_obj=product_obj, price_obj=price_obj)

    def get_all(self, db: Session) -> List[Product]:
        db_obj_list = db.query(self.model).all()
        if not db_obj_list:
            self._initialise(db=db)
        return db.query(self.model).all()

    def update_all(self, db: Session, *, obj_list_in=List[ProductUpdate]) -> List[Product]:
        self._remove_all(db=db)
        for product in obj_list_in:
            product_in = ProductCreate(**product.model_dump(exclude_unset=True))
            product_obj = self.create(db=db, obj_in=product_in)
            for price_in in product.prices:
                price_in = PriceCreate(**price_in.model_dump(exclude_unset=True))
                price_obj = price.create(db=db, obj_in=price_in)
                product_obj = self._append_price(db=db, db_obj=product_obj, price_obj=price_obj)
        return db.query(self.model).all()


product = CRUDProduct(Product)
