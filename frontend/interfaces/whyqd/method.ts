/* eslint-disable camelcase */

import type { IDentifier, IVersion, IField, IFieldType, IMimeType } from "./"

// month https://stackoverflow.com/a/18648314/295606
export interface ICitation {
  author: string
  title: string
  url?: URL
  publisher?: string
  institution?: string
  doi?: string
  month?: string
  year?: number
  note?: string
}

export interface IColumnCreate extends IDentifier {
  name: string
  type: IFieldType
}
export interface IColumn extends IDentifier, IColumnCreate {}

export interface IActionScriptCreate {
  script: string
}

export interface IActionScript extends IDentifier, IActionScriptCreate {}

export interface IDataUpdate extends IDentifier {
  names?: (IColumnCreate | IColumn)[]
  actions?: (IActionScriptCreate | IActionScript)[]
  preserve?: IColumn[]
  key?: IColumn
}

export interface IData extends IDentifier {
  path: string
  mime: IMimeType
  sheet_name?: string
  names?: IColumn[]
  columns: IColumn[]
  preserve?: IColumn[]
  key?: IColumn
  actions?: IActionScriptCreate[] | IActionScript[]
  checksum: string
  citation?: ICitation
}

export interface IMethodCreate {
  name: string
  title?: string
  description?: string
  schema_fields: IField[]
  input_data: IData[]
  working_data?: IData
  restructured_data?: IData
  citation?: ICitation
  version?: IVersion[]
}

export interface IMethodUpdate extends IDentifier {}

export interface IMethod extends IDentifier, IMethodCreate {}
