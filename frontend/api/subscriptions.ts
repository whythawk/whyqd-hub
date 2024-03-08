import {
  ICode, IOrder, IProduct, IProductPricing, ISubscription, ISubscriptionView, ISubscriptionAdminCreate,
  IStripeCheckoutResponse, IStripeIntent, IStripeCheckoutIntent, IOgunFilters, IUserEmail, IUserProfile, IMsg
} from "@/interfaces"
import { apiCore } from "./core"

export const apiSubscriptions = {
  // ADMINISTRATION
  async getWorkingDirectorySize(token: string) {
    return await useFetch<IMsg>(`${apiCore.url()}/products/working`, 
      {
        headers: apiCore.headers(token)
      }
    )
  },
  async clearWorkingDirectory(token: string) {
    return await useFetch<IMsg>(`${apiCore.url()}/products/working`, 
      {
        method: "POST",
        headers: apiCore.headers(token)
      }
    )
  },
  // SUBSCRIPTIONS & ORDERS
  async getOrders(token: string, payload: IOgunFilters = {}) {
    return await useFetch<IOrder[]>(`${apiCore.url()}/subscriptions/`, 
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async redirectToStripeAccount(token: string) {
    return await useFetch<IStripeCheckoutResponse>(`${apiCore.url()}/subscriptions/stripe-account`, 
      {
        method: "POST",
        headers: apiCore.headers(token),
      }
    )
  },
  async getMulti(token: string, payload: IOgunFilters = {}) {
    return await useFetch<ISubscriptionView[]>(
      `${apiCore.url()}/subscriptions/all`,
      {
        headers: apiCore.headers(token),
        query: payload,
      }
    )
  },
  async getSubscriber(token: string, payload: IUserEmail) {
    return await useFetch<IUserProfile>(
      `${apiCore.url()}/subscriptions/subscriber`,
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async createSubscription(token: string, payload: ISubscriptionAdminCreate) {
    return await useFetch<ISubscription>(
      `${apiCore.url()}/subscriptions/create`,
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async removeSubscription(token: string, key: string) {
    return await useFetch<IMsg>(
      `${apiCore.url()}/subscriptions/${key}`, 
      {
        method: "DELETE",
        headers: apiCore.headers(token),
      }
    )
  },
  async getLatestSubscription(token: string) {
    return await useFetch<ISubscription>(
      `${apiCore.url()}/subscriptions/latest`,
      {
        headers: apiCore.headers(token),
      }
    )
  },
  // STRIPE PAYMENT INTENTS & SESSIONS
  async getSubscriptionProducts(payload: ICode) {
    return await useFetch<IProductPricing[]>(
      `${apiCore.url()}/products/`,
      {
        method: "POST",
        body: payload,
      }
    )
  },
  async getAllSubscriptionProducts(token: string) {
    return await useFetch<IProduct[]>(
      `${apiCore.url()}/products/all`,
      {
        headers: apiCore.headers(token),
      }
    )
  },
  async updateAllSubscriptionProducts(token: string, payload: IProduct[]) {
    return await useFetch<IProduct[]>(
      `${apiCore.url()}/products/all`,
      {
        method: "PUT",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
  async getStripeIntent(payload: IStripeIntent) {
    return await useFetch(`${apiCore.url()}/subscriptions/`, 
    {
      method: "POST",
      body: payload,
      }
    )
  },
  async createCheckoutSession(token: string, payload: IStripeCheckoutIntent) {
    return await useFetch<IStripeCheckoutResponse>(
      `${apiCore.url()}/subscriptions/order`,
      {
        method: "POST",
        body: payload,
        headers: apiCore.headers(token),
      }
    )
  },
}