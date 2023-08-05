from app.schema_types.base import BaseEnum


class MimeType(BaseEnum):
    # Note that neither `feather` nor `parquet` yet have official mime types.
    CSV = "text/csv"
    XLS = "application/vnd.ms-excel"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    PARQUET = "application/vnd.apache.parquet"
    PRQ = "application/vnd.apache.parquet"
    FEATHER = "application/vnd.apache.feather"
    FTR = "application/vnd.apache.feather"
