/* eslint-disable camelcase */
import { IMimeType } from "./"

export interface IDataUpload {
  mime: IMimeType
  data: string
  name?: string
}

export interface IDatasourceUpload {
  data: IDataUpload[]
  urls?: string[]
  directory?: string
}

export interface IDataSummary {
  name: string
  sheet_name?: string
  uuid: string
  data?: object[]
  row_count?: number
}
