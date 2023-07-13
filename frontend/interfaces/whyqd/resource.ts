import { IKeyable } from "../utilities"
import { IMimeType, IStatusType, IReferenceType, IModelSummary, IFieldCreate, IActionModel } from "./"

export interface IResource {
  // https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
  id: string
  created: string
  modified: string
  is_private: boolean
  name: string
  title?: string
  description?: string
  state: IStatusType
  data?: IModelSummary
  schema_subject?: IModelSummary
  crosswalk?: IModelSummary
  schema_object?: IModelSummary
  transform?: IModelSummary
  transformdata?: IModelSummary
  task?: IModelSummary
}

interface IResourceModelLinks {
  id: string
  model_type: IReferenceType
}

export interface IResourceDataReference {
  id?: string
  created?: string
  isPrivate: boolean
  name?: string
  title?: string
  description?: string
  links?: IResourceModelLinks[]
  sheet_name?: string
  mime_type?: IMimeType
  index?: number
  summarykeys?: string[]
  summary?: IKeyable[]
}

export interface IResourceSchemaReference {
  id?: string
  created?: string
  isPrivate: boolean
  name?: string
  title?: string
  description?: string
  links?: IResourceModelLinks[]
  fields?: IFieldCreate[]
}

export interface IResourceCrosswalkReference {
  id?: string
  created?: string
  isPrivate: boolean
  name?: string
  title?: string
  description?: string
  links?: IResourceModelLinks[]
  actions?: IActionModel[]
}

export interface IResourceManager {
  id: string
  created: string
  modified: string
  is_private: boolean
  name: string
  title?: string
  description?: string
  state: IStatusType
  data?: IResourceDataReference
  schema_subject?: IResourceSchemaReference
  crosswalk?: IModelSummary
  schema_object?: IModelSummary
  transform?: IModelSummary
  transformdata?: IResourceDataReference
  task?: IModelSummary
}

export interface IResourceCrosswalkManager {
  id: string
  created: string
  modified: string
  is_private: boolean
  name: string
  title?: string
  description?: string
  state: IStatusType
  data?: IResourceDataReference
  schema_subject: IResourceSchemaReference
  crosswalk: IResourceCrosswalkReference
  schema_object: IResourceSchemaReference
  task?: IModelSummary
}

export interface IResourceFilters {
  state?: IStatusType
  date_from?: string
  date_to?: string
  descending?: boolean
  skip?: number
  limit?: number
}