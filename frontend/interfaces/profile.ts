/* eslint-disable camelcase */
import type { ISubscriptionProfile } from "./subscriptions"

export interface IUserProfile {
  id: string
  email: string
  email_validated: boolean
  is_active: boolean
  is_superuser: boolean
  full_name: string
  password: boolean
  totp: boolean
  subscriptions: ISubscriptionProfile
}

export interface IUserProfileUpdate {
  email?: string
  full_name?: string
  original?: string
  password?: string
  is_active?: boolean
  is_superuser?: boolean
}

export interface IUserProfileCreate {
  email: string
  full_name?: string
  password?: string
  is_active?: boolean
  is_superuser?: boolean
}

export interface IUserOpenProfileCreate {
  email: string
  full_name?: string
  password: string
}

export interface IUserEmail {
  email: string
}

export interface IProfileSummary {
  email: string
  full_name?: string
}