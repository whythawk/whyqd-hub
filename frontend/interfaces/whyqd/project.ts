import { IAccrualPolicyType, IAccrualType, IFrequencyType, IModelSummary } from "./"

export interface IProject {
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
  accrualPolicy?: IAccrualPolicyType
  bibliographicCitation?: string
  conformsTo?: string
  schema?: IModelSummary
  schema_id?: string
}

export interface IProjectFilters {
  date_from?: string
  date_to?: string
  descending?: boolean
  page?: number
}


