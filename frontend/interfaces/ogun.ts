
import { IResearcherRoleType } from "./whyqd"

export interface IOgunCreate {
  id: string
  created: string
  authorises_id: string
  responsibility: IResearcherRoleType
  access_key: string
  secret_key: string
}

export interface IOgunUser {
  id: string
  created: string
  authorises_id: string
  responsibility: IResearcherRoleType
  access_key: string
}

export interface IOgunToken {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface IOgunFilters {
  page?: number
}