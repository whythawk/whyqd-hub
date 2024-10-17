/* eslint-disable camelcase */

import type { IReferenceType, IUserSummary, IModelSummary, IStatusType, IFrequencySubType } from "./"
import type { IKeyable } from "../utilities"

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


export interface IActivityReportFilters {
  project_id?: string
  task_id?: string
  frequency?: IFrequencySubType
  state?: IStatusType
  date_from?: string
  date_to?: string
}

export interface IActivityReport {
  project_id?: string
  project_name?: string
  task_id?: string
  task_name?: string
  frequency?: IFrequencySubType
  state?: IStatusType
  date_from?: string
  date_to?: string
  count?: number
  data?: IKeyable[]
}

// REVIEW

export interface IPinnedResource {
  resource_id: string
  resource_type: IReferenceType
  title: string
}
