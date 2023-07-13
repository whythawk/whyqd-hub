/* eslint-disable camelcase */

import {
  IDublinCore,
  IDublinCoreTerms,
  IDublinCoreIdentifier,
  IDublinCoreInDB,
  IDentifier,
  IReferenceType,
  IResearcherRoleType,
  IStatusType,
} from "./"

import { IUserProfile } from "@/interfaces"

// https://www.typescriptlang.org/docs/handbook/2/objects.html#extending-types
export interface IProjectCreate extends IDublinCore, IDublinCoreInDB {}
export interface IProject
  extends IDublinCoreIdentifier,
    IDublinCore,
    IDublinCoreInDB {}

export interface ICollectionCreate extends IDublinCore, IDublinCoreInDB {}
export interface ICollection
  extends IDublinCoreIdentifier,
    IDublinCore,
    IDublinCoreInDB {
  project: string
  schemaRule?: string
}

export interface IDatasetCreate
  extends IDublinCore,
    IDublinCoreTerms,
    IDublinCoreInDB {
  schemaIdentifier: string
}
export interface IDataset
  extends IDublinCoreIdentifier,
    IDublinCore,
    IDublinCoreTerms,
    IDublinCoreInDB {
  schemaIdentifier: string
  collection: string
}

export interface IMethodSource
  extends IDublinCoreIdentifier,
    IDublinCore,
    IDublinCoreTerms,
    IDublinCoreInDB {
  filename: string
}

export interface IDatasource
  extends IDublinCoreIdentifier,
    IDublinCore,
    IDublinCoreTerms,
    IDublinCoreInDB {
  status: IStatusType
  sources: string[]
  directory: string
  dataset: string
  method: string
  build: string
}

export interface IResearchResourceCreate {
  resource_type: IReferenceType
}
export interface IResearchResource
  extends IDentifier,
    IResearchResourceCreate {}

export interface IResearcherRoleCreate {
  resource_id: string
  resource_type: IReferenceType
  researcher_id: string
  research_roles: IResearcherRoleType[]
}
export interface IResearcherRole extends IResearcherRoleCreate {
  id: string
}

export interface IResearchTeamMemberCreate {
  email: string
  full_name: string
}
export interface IResearchTeamMember extends IUserProfile {
  roles: IResearcherRole[]
}

export interface IResearchTeamMemberInvitationCreate {
  email: string
  full_name: string
  sendor_id: string
  team_id: string
}
export interface IResearchTeamMemberInvitationUpdate {
  id: string
  response: "ACCEPTED" | "REFUSED"
}
export interface IResearchTeamMemberInvitation
  extends IResearchTeamMemberInvitationCreate {
  id: string
  created: string
  response: "WAITING" | "ACCEPTED" | "REFUSED"
}

export interface IResearchMemberInvitation
  extends IResearchTeamMemberInvitation {
  team: { title: string; description?: string }
}

export interface IResearchTeamCreate {
  title: string
  description?: string
  projects?: IProject[]
  resources?: IResearchResource[]
  members?: IUserProfile[]
}
export interface IResearchTeamUpdate extends IResearchTeamCreate {
  id: string
}
export interface IResearchTeam extends IResearchTeamCreate {
  id: string
  created: Date
  updated: Date
  members: IResearchTeamMember[]
}
