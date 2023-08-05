
import { IReferenceType, IMimeType, IResearcherRoleType, ICitation, IActionScript, } from "./"

export interface IReference {
  id: string
  created: string
  is_private: boolean
  name: string
  title?: string
  description?: string
  model: string
  model_type: IReferenceType
  version?: string
  hash?: string
  mime_type?: IMimeType
  index?: number
}


export interface IReferenceTemplate {
  id: string
  created: string
  is_private: boolean
  name: string
  title?: string
  description?: string
  model: string
  model_type: IReferenceType
  version?: string
  mime_type?: IMimeType
}

interface IKeyable {
  [key: string]: any | any[]
}

export interface IDataSourceTemplate {
    uuid?: string
    created?: string
    name?: string
    title?: string
    description?: string
    path?: string
    mime?: IMimeType
    header?: number | number[]
    attributes?: IKeyable
    citation?: ICitation
}

export interface ICrosswalkTemplate {
  uuid?: string
  created?: string
  name?: string
  title?: string
  description?: string
  schemaObject?: string
  actions?: IActionScript[]
}

export interface IReferenceFilters {
  match?: string
  reference_type?: IReferenceType
  responsibility?: IResearcherRoleType
  mime_type?: IMimeType
  date_from?: string
  date_to?: string
  version_from?: string
  version_to?: string
  descending?: boolean
  page?: number
}
