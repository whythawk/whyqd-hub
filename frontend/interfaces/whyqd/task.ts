import type { IAccrualPolicyType, IAccrualType, IFrequencyType, IModelSummary } from "./"

export interface ITask {
  // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
  id?: string
  created?: string
  modified?: string
  is_private: boolean
  name: string
  title?: string
  description?: string
  frequency?: string
  spatial?: string
  temporalStart?: string
  temporalEnd?: string
  language?: string
  creator?: string
  contributor?: string
  publisher?: string
  rights?: string
  source?: string
  accessRights?: string
  accrualMethod?: IAccrualType
  accrualPeriodicity?: IFrequencyType
  accrualPriority?: number
  accrualPolicy?: IAccrualPolicyType
  bibliographicCitation?: string
  conformsTo?: string
  resources?: number
  schema?: IModelSummary
  datasource?: IModelSummary
  crosswalk?: IModelSummary
  project?: IModelSummary
  datasource_id?: string
  crosswalk_id?: string
  schema_id?: string
  project_id?: string
}

export interface IScheduledTask {
  // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
  id?: string
  created?: string
  modified?: string
  is_private: boolean
  name: string
  title?: string
  description?: string
  frequency?: string
  spatial?: string
  temporalStart?: string
  temporalEnd?: string
  language?: string
  creator?: string
  contributor?: string
  publisher?: string
  rights?: string
  source?: string
  accessRights?: string
  accrualMethod?: IAccrualType
  accrualPeriodicity?: IFrequencyType
  accrualPriority?: number
  accrualPolicy?: IAccrualPolicyType
  bibliographicCitation?: string
  conformsTo?: string
  lastCompleted?: string
  latestResource?: IModelSummary
  resources?: number
  schema?: IModelSummary
  project?: IModelSummary
}

export interface ITaskFilters {
  match?: string
  date_from?: string
  date_to?: string
  descending?: boolean
  scheduled?: boolean
  prioritised?: boolean
  accrualPolicy?: IAccrualPolicyType
  accrualPeriodicity?: IFrequencyType
  page?: number
}

export interface ITaskScheduleFilters {
  match?: string
  date_from?: string
  date_to?: string
  scheduled?: boolean
  accrualPolicy?: IAccrualPolicyType
  accrualPeriodicity?: IFrequencyType
  page?: number
}



