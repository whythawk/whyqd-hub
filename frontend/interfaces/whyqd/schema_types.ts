export type IAccrualPolicyType = "closed" | "passive" | "active" | "partial"

export type IAccrualType =
  | "deposit"
  | "donation"
  | "purchase"
  | "loan"
  | "license"
  | "itemCreation"

export type IFrequencyType =
  | "triennial"
  | "biennial"
  | "annual"
  | "semiannual"
  | "threeTimesAYear"
  | "quarterly"
  | "bimonthly"
  | "monthly"
  | "semimonthly"
  | "biweekly"
  | "threeTimesAMonth"
  | "weekly"
  | "semiweekly"
  | "threeTimesAWeek"
  | "daily"
  | "continuous"
  | "irregular"

export type IMimeType = "CSV" | "XLS" | "XLSX" | "PARQUET" | "FEATHER"

export type IResearcherRoleType =
  | "CUSTODIAN"
  | "CURATOR"
  | "WRANGLER"
  | "SEEKER"

export type IReferenceType =
  | "DATASOURCE"
  | "DATA"
  | "SCHEMA"
  | "CROSSWALK"
  | "TRANSFORM"

export type IFieldType =
  | "string"
  | "number"
  | "integer"
  | "boolean"
  | "array"
  | "date"
  | "datetime"
  | "month"
  | "quarter"
  | "year"
  | "any"

export type IStatusType =
  | "BUSY"
  | "READY"
  | "DATA_READY"
  | "SCHEMA_READY"
  | "CROSSWALK_READY"
  | "TRANSFORM_READY"
  | "IMPORT_ERROR"
  | "DATA_ERROR"
  | "SCHEMA_ERROR"
  | "CROSSWALK_ERROR"
  | "TRANSFORM_ERROR"
  | "ERROR"
  | "COMPLETE"

export type InvitationResponseType =
| "WAITING"
| "ACCEPTED"
| "REFUSED"