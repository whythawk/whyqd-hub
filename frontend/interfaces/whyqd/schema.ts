/* eslint-disable camelcase */

import type { IFieldType, IVersion, ICitation } from "./"

export interface IDentifier {
  uuid: string
}

export interface ICategoryCreate {
  uuid?: string
  name: boolean | string
  description?: string
}

export interface ICategory extends IDentifier {
  name: boolean | string
  description?: string
}

export interface IConstraintsCreate {
  required?: boolean
  unique?: boolean
  enum?: ICategoryCreate[]
  default?: ICategoryCreate
  minimum?: number
  maximum?: number
}

export interface IConstraints {
  required?: boolean
  unique?: boolean
  enum?: ICategory[]
  default?: ICategory
  minimum?: number
  maximum?: number
}

export interface IFieldCreate {
  uuid?: string
  name: string
  title?: string
  description?: string
  type: IFieldType
  example?: string
  constraints?: IConstraintsCreate
}

export interface IField extends IDentifier {
  name: string
  title?: string
  description?: string
  type: IFieldType
  example?: string
  constraints?: IConstraints
}

export interface ISchemaCreate {
  uuid?: string
  name: string
  title?: string
  description?: string
  fields?: IFieldCreate[]
  missingValues?: string[]
  primaryKey?: string | string[]
  index?: number
  citation?: ICitation
  version?: IVersion[]
}

export interface ISchema extends IDentifier {
  name: string
  title?: string
  description?: string
  fields: IFieldCreate[]
  missingValues: string[]
  primaryKey?: string | string[]
  index?: number
  citation?: ICitation
  version?: IVersion[]
}

// export interface ISchemaInDB {
//   id: string
//   name: string
//   title?: string
//   description?: string
//   created: Date
//   modified: Date
//   version?: Date
//   reference: IReference
// }

// export interface ISchemaFilters {
//   date_from?: string
//   date_to?: string
//   descending?: boolean
// }