
/* eslint-disable camelcase */
import { IStatusType } from "./"

export interface IUserSummary {
  email: string
  full_name?: string
}

export interface IModelSummary {
  id?: string
  created?: string
  modified?: string
  is_private: boolean
  name?: string
  title?: string
  description?: string
  state?: IStatusType
}

// month https://stackoverflow.com/a/18648314/295606
export interface ICitation {
  author: string
  title: string
  url?: string
  publisher?: string
  institution?: string
  doi?: string
  month?: string
  year?: number
  licence?: string
  note?: string
}