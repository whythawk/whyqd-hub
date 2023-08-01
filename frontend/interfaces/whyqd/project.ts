import {
  IAccrualPolicyType, IAccrualType, IFrequencyType,
  IModelSummary, InvitationResponseType, IResearcherRoleType
} from "./"
import { IProfileSummary } from "../"

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
  auths: IProjectRoleSummary[]
}

export interface IProjectFilters {
  match?: string
  date_from?: string
  date_to?: string
  descending?: boolean
  page?: number
}

export interface IProjectRole {
  id: string
  created: string
  researcher: IProfileSummary
  responsibility: IResearcherRoleType
  project: IModelSummary
  task?: IModelSummary
  resource?: IModelSummary
  reference?: IModelSummary
  referencetemplate?: IModelSummary
}

export interface IProjectRoleSummary {
  id: string
  created: string
  researcher: IProfileSummary
  responsibility: IResearcherRoleType
}

export interface IProjectInvitation {
  id: string
  created: string
  fullName?: string
  email: string
  response: InvitationResponseType
  sender: IProfileSummary
  project?: IModelSummary
}
