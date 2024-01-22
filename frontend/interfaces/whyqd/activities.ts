/* eslint-disable camelcase */

import { IReferenceType, IUserSummary, IModelSummary, IStatusType } from "./"

export interface IActivity {
  id: string
  created: string
  custodiansOnly: boolean
  alert: boolean
  message: string
  researcher: IUserSummary
  resource: IModelSummary
  task: IModelSummary
  project: IModelSummary
}

export interface IResourceActivity {
  id: string
  created: string
  custodiansOnly: boolean
  alert: boolean
  message: string
}

export interface IActivityFilters {
  match?: string
  state?: IStatusType
  date_from?: string
  date_to?: string
  alert?: boolean
  custodian?: boolean
  excludeComplete?: boolean
  prioritised?: boolean
  page?: number
}

// REVIEW

export interface IPinnedResource {
  resource_id: string
  resource_type: IReferenceType
  title: string
}
