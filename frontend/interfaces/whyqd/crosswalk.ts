/* eslint-disable camelcase */

import type { ISchema, IVersion, ICitation } from "./"

export type IActionType =
  | "CALCULATE"
  | "CATEGORISE"
  | "COLLATE"
  | "DEBLANK"
  | "DEDUPE"
  | "DELETE_ROWS"
  | "NEW"
  | "PIVOT_CATEGORIES"
  | "PIVOT_LONGER"
  | "RENAME"
  | "SELECT"
  | "SELECT_NEWEST"
  | "SELECT_OLDEST"
  | "SEPARATE"
  | "UNITE"

export type IActionModifierType = "+" | "-" | "~"

export interface IActionModifier {
  name: IActionModifierType
  title?: string
}

// export type IActionCalculateArray<T> = Array<T> & {
//   0?: IActionModifier
//   1?: IField
// }
// use as: IActionSelectArray<any>
// export type IActionSelectArray<T> = Array<T> & {
//   0?: IField
//   1?: IActionModifier
//   2?: IField
// }

export interface IActionScript {
  uuid?: string
  script: string
}

export interface IActionModel {
  uuid?: string
  action: IActionType
  destinationField?: string | string[]
  destinationTerm?: boolean | string
  sourceTerm?: string | string[]
  sourceField?: string | string[] | [IActionModifierType, string][] | [string, IActionModifierType, string][] | [IActionModifierType | string][]
  rows?: number[]
}

export interface ICrosswalkCreate {
  uuid?: string
  name: string
  title?: string
  description?: string
  schemaSource?: ISchema
  schemaDestination?: ISchema
  actions: IActionScript[]
  citation?: ICitation
  version?: IVersion[]
}