/* eslint-disable camelcase */
export type ICurrencyTypes = "usd" | "gbp" | "eur"

export type IProductTypes =
  | "REVIEWER"
  | "EXPLORER"
  | "RESEARCHER"
  | "INVESTIGATOR"

export type ISubscriptionEventTypes =
  | "PENDING"
  | "CREATED"
  | "COMPLETED"
  | "RENEWED"
  | "FAILED"
  | "ENDED"

export interface ICode {
  ip: string | null
}

export interface IStripeIntent {
  amount: number
  currency: ICurrencyTypes
}

export interface IStripeCheckoutIntent {
  price_id: string
  subscriber_id: string
  ip: string | null
}

export interface IStripeCheckoutResponse {
  redirect: string
}

export interface IStripePortalSessionIntent {
  session_id: string
}

export interface IPrice {
  id: string
  currency: ICurrencyTypes
  per_annum: number
}

export interface IProduct {
  id: string
  name: string
  description: string
  subscription: IProductTypes
  prices: IPrice[]
}

export interface IOrder {
  id: string
  created: Date
  subscription_event_type: ISubscriptionEventTypes
  country_code: string
  country_name: string
  subscription_type: IProductTypes
  currency: ICurrencyTypes
  amount: number
  invoice_url: string
}

export interface ISubscription {
  id: string
  subscription_id: string
  subscription_event_type: ISubscriptionEventTypes
  subscription_type: IProductTypes
  created: Date
  started: Date
  ends: Date
  override: boolean
  subscriber_id: string
}

export interface ISubscriptionProfile {
  membership: IProductTypes
  ends: Date
  override: boolean
}

export interface ISubscriptionView {
  id: string
  subscription_id: string
  subscription_event_type: ISubscriptionEventTypes
  subscription_type: IProductTypes
  created: Date
  ends: Date
  override: boolean
  subscriber: string
}

export interface ISubscriptionAdminCreate {
  subscription_type: IProductTypes
  ends: Date | string
  override: boolean
  subscriber: string
}
