import { IAccrualPolicyType, IAccrualType, IFrequencyType, IModelSummary } from "./"

export interface ITask {
  // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
  id?: string
  created?: string
  modified?: string
  is_private: boolean
  name: string
  title?: string
  description?: string
  subjects?: string[]
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
  schema?: IModelSummary
  datasource?: IModelSummary
  crosswalk?: IModelSummary
  project?: IModelSummary
  datasource_id?: string
  crosswalk_id?: string
  schema_id?: string
  project_id?: string
}

export interface ITaskFilters {
  date_from?: string
  date_to?: string
  descending?: boolean
  skip?: number
  limit?: number
}



