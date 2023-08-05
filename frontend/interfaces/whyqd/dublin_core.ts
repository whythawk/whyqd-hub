import { IAccrualPolicyType, IAccrualType, IFrequencyType, IMimeType } from "./"

export interface IDublinCore {
  // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
  title: string
  description?: string
  subject?: string[]
  frequency?: string
  spatial?: string
  temporal?: string[]
  language?: string
  creator?: string
  contributor?: string
  publisher?: string
  format?: IMimeType
  rights?: string
  source?: string
}

export interface IDublinCoreTerms {
  accessRights?: string
  accrualMethod?: IAccrualType
  accrualPeriodicity?: IFrequencyType
  accrualPolicy?: IAccrualPolicyType
  bibliographicCitation?: string
  conformsTo?: string
}

export interface IDublinCoreIdentifier {
  identifier: string
  created: Date
}

export interface IDublinCoreInDB {
  isActive: boolean
  isPrivate: boolean
}
