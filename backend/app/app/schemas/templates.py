from __future__ import annotations
from typing import Optional, List, Union
from pydantic import field_validator, StringConstraints, ConfigDict, Field
from uuid import UUID, uuid4
from datetime import datetime
from whyqd.models import DataSourceAttributeModel, CitationModel, ActionScriptModel
from whyqd.parsers.datasource import DataSourceParser

from app.schema_types import MimeType
from app.schemas.base_schema import BaseSchema
from typing_extensions import Annotated


class DataSourceTemplateModel(BaseSchema):
    uuid: UUID = Field(
        default_factory=uuid4, description="Automatically generated unique identity for the data source."
    )
    created: datetime = Field(
        default_factory=datetime.now, description="Automatically generated date reference was created."
    )
    name: Optional[str] = Field(None, description="A machine-readable name given to the task.")
    title: Optional[str] = Field(None, description="A descriptive name for the data source.")
    description: Optional[str] = Field(
        None,
        description="A complete description of the data source. Depending on how complex your work becomes, try and be as helpful as possible to 'future-you'. You'll thank yourself later.",
    )
    path: Optional[Annotated[str, StringConstraints(strip_whitespace=True)]] = Field(None, description="Full path to valid source data file.")
    mime: Optional[MimeType] = Field(None, description="Mime type for source data. Automatically generated.")
    header: Optional[Union[int, List[int]]] = Field(
        0, description="Row (0-indexed) to use for the column labels of the parsed DataFrame. "
    )
    attributes: Optional[DataSourceAttributeModel] = Field(
        {},
        description="Optional open dictionary for reader-specific attributes for Pandas' API. E.g. 'quoting' for the CSV library.",
    )
    citation: Optional[CitationModel] = Field(None, description="Optional full citation for the source data.")

    @field_validator("mime", mode="before")
    @classmethod
    def evaluate_mime(cls, v):
        reader = DataSourceParser()
        return reader.get_mimetype(mimetype=v)


class CrosswalkTemplateModel(BaseSchema):
    uuid: UUID = Field(default_factory=uuid4, description="Automatically generated unique identity for the crosswalk.")
    created: datetime = Field(
        default_factory=datetime.now, description="Automatically generated date reference was created."
    )
    name: Optional[str] = Field(None, description="A machine-readable name given to the crosswalk.")
    title: Optional[str] = Field(None, description="A human-readable version of the crosswalk name.")
    description: Optional[str] = Field(
        None,
        description="A complete description of the crosswalk. Depending on how complex your work becomes, try and be as helpful as possible to 'future-you'. You'll thank yourself later.",
    )
    schemaObject: Optional[UUID] = Field(
        None,
        description="The destination schema reference UUID which the crosswalk will transform to.",
    )
    schemaHash: Optional[str] = Field(
        None,
        description="The destination schema reference hash which the crosswalk will transform to.",
    )
    actions: list[ActionScriptModel] = Field(
        default=[],
        description="List of Actions in script format to be performed on these data, in this order. Will be parsed and validated seperately.",
    )
    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True, validate_assignment=True)
