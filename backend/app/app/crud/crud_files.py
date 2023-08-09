from __future__ import annotations
from typing import TYPE_CHECKING
from fastapi import UploadFile
import base64
from uuid import UUID, uuid4
from pathlib import Path
import posixpath
import urllib
import modin.pandas as pd
import numpy as np
from io import BufferedReader
from collections.abc import Iterator
from botocore.response import StreamingBody
from whyqd.parsers import CoreParser, DataSourceParser
from whyqd.models import DataSourceModel, SchemaModel, CrosswalkModel, TransformModel, VersionModel

from app.core.config import settings
from app.schema_types import MimeType, ReferenceType
from app.schemas.templates import DataSourceTemplateModel, CrosswalkTemplateModel
from app.crud.crud_spaces import spaces

if TYPE_CHECKING:
    from app.models.user import User


class CRUDFiles:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) working data on the local drive.
        """
        self.core = CoreParser()
        self.reader = DataSourceParser()
        self.directory = self.core.check_path(directory=settings.WORKING_PATH + settings.REFERENCE_PATH)
        self.summary = self.core.check_path(directory=settings.WORKING_PATH + settings.SUMMARY_PATH)
        self.temporary = self.core.check_path(directory=settings.WHYQD_DIRECTORY)
        self.use_spaces = settings.USE_SPACES

    def import_source_from_upload(
        self,
        *,
        source: UploadFile,
        datasource_in: DataSourceTemplateModel,
    ) -> DataSourceTemplateModel:
        datasource_in.uuid = uuid4()
        mimetype = self.reader.get_mimetype(mimetype=datasource_in.mime)
        datasource_name = f"{datasource_in.uuid}.{mimetype.name}"
        datasource_in.path = datasource_name
        # https://stackoverflow.com/questions/63048825/how-to-upload-file-using-fastapi/70657621#70657621
        try:
            with open(self.temporary / datasource_name, "wb") as f:
                while contents := source.file.read():
                    f.write(contents)
        except Exception as e:
            raise ValueError(e)
        finally:
            source.file.close()
        return datasource_in

    def import_source(
        self,
        *,
        source: str,
        mimetype: MimeType,
        datasource_in: DataSourceTemplateModel | None = None,
    ) -> DataSourceTemplateModel:
        if not datasource_in:
            datasource_in = DataSourceTemplateModel()
        else:
            # create a new UUID from template
            datasource_in.uuid = uuid4()
        mimetype = self.reader.get_mimetype(mimetype=mimetype)
        datasource_in.mime = mimetype
        datasource_name = f"{datasource_in.uuid}.{mimetype.name}"
        if self.core.check_uri(source=source):
            datasource_in.path = source
            # datasource_in.name = self.core.download_uri_source(source=source, directory=self.temporary).name
            datasource_in.name = self.download_uri_source(source=source, directory=self.temporary).name
            # Rename the source
            Path(self.temporary / datasource_in.name).rename(self.temporary / datasource_name)
        else:
            # Comes from API, so is always a base64 ... causes challenges with mimetypes ...
            data = base64.b64decode(source)
            if not datasource_in.name:
                datasource_in.name = datasource_name
            if not datasource_in.path:
                datasource_in.path = datasource_in.name
            with open(self.temporary / datasource_name, "wb") as f:
                f.write(data)
        return datasource_in

    def import_transform(
        self,
        *,
        data: pd.DataFrame,
        mimetype: MimeType | str | None = None,
    ) -> DataSourceTemplateModel:
        if not mimetype:
            mimetype = settings.WHYQD_DEFAULT_MIMETYPE
        mimetype = self.reader.get_mimetype(mimetype=mimetype)
        datasource_in = DataSourceTemplateModel()
        datasource_in.name = f"{datasource_in.uuid}.{mimetype.name}"
        datasource_in.mime = mimetype
        datasource_in.path = f"{datasource_in.uuid}.{mimetype.name}"
        self.reader.set(df=data, source=self.temporary / datasource_in.path, mimetype=mimetype)
        self.save_source(obj_id=datasource_in.uuid, mimetype=mimetype)
        return datasource_in

    def get_transform_datamodel(
        self,
        *,
        data: pd.DataFrame,
        datasource_in: DataSourceTemplateModel,
    ) -> DataSourceModel:
        data_in = self.reader.get_source_data_model(
            df=data, source=self.temporary / datasource_in.path, mimetype=datasource_in.mime
        )
        data_in.path = f"{datasource_in.uuid}.{datasource_in.mime.name}"
        return data_in

    def get_source_path(
        self,
        *,
        obj_id: str,
        mimetype: MimeType,
        is_temporary: bool = False,
    ) -> Path | None:
        obj_name = f"{obj_id}.{mimetype.name}"
        source_path = self.directory
        if is_temporary:
            source_path = self.temporary
        source_path = source_path / obj_name
        if self.core.check_source(source=source_path):
            return source_path
        if self.use_spaces:
            if spaces.exists(filename=obj_name):
                spaces.download_file(filename=obj_name, source_path=source_path)
        return source_path

    def save_source(
        self,
        *,
        obj_id: str,
        mimetype: MimeType,
    ) -> Path:
        # After import, and all validations, save for storage
        # Assumption is that it is currently in temporary storage
        obj_name = f"{obj_id}.{mimetype.name}"
        temporary_path = self.get_source_path(obj_id=obj_id, mimetype=mimetype, is_temporary=True)
        source_path = self.directory
        if self.use_spaces:
            spaces.upload_file(filename=obj_name, source_path=temporary_path)
        # We still need it
        Path(temporary_path).rename(source_path / obj_name)
        self.delete_source(obj_id=obj_id, mimetype=mimetype, is_temporary=True)
        return source_path / obj_name

    def delete_source(
        self,
        *,
        obj_id: str,
        mimetype: MimeType,
        is_temporary: bool = False,
    ) -> None:
        source_path = self.get_source_path(obj_id=obj_id, mimetype=mimetype, is_temporary=is_temporary)
        if source_path:
            self.core.delete_file(source=source_path)

    def get(
        self,
        *,
        obj_id: UUID | str,
        obj_type: ReferenceType,
        is_template: bool = False,
    ) -> DataSourceTemplateModel | DataSourceModel | SchemaModel | CrosswalkModel | TransformModel | None:
        resource_models = {
            "DATASOURCE": DataSourceTemplateModel,
            "DATA": DataSourceModel,
            "SCHEMA": SchemaModel,
            "CROSSWALK": CrosswalkModel,
            "TRANSFORM": TransformModel,
        }
        obj_in = None
        obj_name = f"{obj_id}.{obj_type.name}"
        resource_model = resource_models[obj_type.name]
        if is_template and obj_type.name == "CROSSWALK":
            resource_model = CrosswalkTemplateModel
        if self.use_spaces:
            if spaces.exists(filename=obj_name):
                obj_in = spaces.get(filename=obj_name)
        else:
            source = self.directory
            obj_in = self.core.load_json(source=str(source / obj_name))
        if obj_in:
            if obj_in.get("fields") and isinstance(obj_in["fields"], list):
                for field in obj_in["fields"]:
                    if field.get("constraints") and isinstance(field["constraints"], dict):
                        if not isinstance(field["constraints"].get("enum"), list):
                            field["constraints"]["enum"] = []
            obj_in = resource_model(**obj_in)
        return obj_in

    def get_data_stream(
        self, *, obj_id: str, mimetype: MimeType | str, folder_id: UUID | str | None = None
    ) -> StreamingBody | Iterator[BufferedReader]:
        mimetype = self.reader.get_mimetype(mimetype=mimetype)
        obj_name = f"{obj_id}.{mimetype.name}"
        if self.use_spaces:
            if spaces.exists(filename=obj_name):
                return spaces.get_stream(filename=obj_name, folder_id=folder_id)
        if self.core.check_source(source=self.directory / obj_name):
            with open(self.directory / obj_name, mode="rb") as stream:
                while chunk := stream.read(settings.CHUNK_SIZE):
                    yield chunk

    def create_or_update(
        self,
        *,
        user: User,
        obj_in: DataSourceTemplateModel | DataSourceModel | SchemaModel | CrosswalkModel | TransformModel,
        obj_type: ReferenceType,
        branch: bool = False,
    ) -> DataSourceTemplateModel | DataSourceModel | SchemaModel | CrosswalkModel | TransformModel:
        # Slight modification of the model
        if "version" in obj_in.dict():
            if len(obj_in.version) >= 1:
                # new UUID - saving a version history
                if branch:
                    obj_in.uuid = uuid4()
                update = VersionModel(**{"description": f"Update save of {obj_in.__class__.__name__}."})
            else:
                update = VersionModel(**{"description": f"Initial save of {obj_in.__class__.__name__}."})
            update.name = user.email
            if user.full_name:
                update.name = f"{user.full_name} <{user.email}>"
            obj_in.version.append(update)
        jsn_obj = obj_in.json(by_alias=True, exclude_defaults=True, exclude_none=True)
        obj_name = f"{obj_in.uuid}.{obj_type.name}"
        if self.use_spaces:
            spaces.update(source=jsn_obj, filename=obj_name)
        else:
            source = self.directory
            self.core.save_file(data=jsn_obj, source=str(source / obj_name))
        return obj_in

    def remove(
        self,
        *,
        obj_id: UUID | str,
        obj_type: ReferenceType | None = None,
        is_temporary: bool = False,
    ):
        obj_name = str(obj_id)
        if obj_type:
            obj_name = f"{obj_name}.{obj_type.name}"
        if not is_temporary and self.use_spaces:
            # `is_temporary` forces for temporary files
            if spaces.exists(filename=obj_name):
                spaces.remove(filename=obj_name)
        else:
            source = self.directory
            if is_temporary:
                source = self.temporary
            self.core.delete_file(source=str(source / obj_name))

    def download_uri_source(self, source: str, directory: Path | str | None = None) -> Path:
        """Downloads a source at a remote uri, and returns a Path for that downloaded source.

        Parameters
        ----------
        source: str
            URI path to source.
        directory: Path | str | None

        Returns
        -------
        Path to local source.
        """
        request = urllib.request.Request(source, method="HEAD")
        request = urllib.request.urlopen(request).info()
        filename = request.get_filename()
        if not filename:
            #  https://stackoverflow.com/a/11783319/295606
            source_path = urllib.request.urlsplit(source).path
            filename = posixpath.basename(source_path)
        if not filename:
            # Make something up ...
            filename = f"temporary-{uuid4()}"
        if not directory:
            directory = self.temporary
        local_source = Path(directory) / filename
        if not self.core.check_source(source=local_source):
            urllib.request.urlretrieve(source, local_source)
        return local_source

    def save_data_summary(self, *, obj_id: UUID | str, obj_in: DataSourceTemplateModel):
        mimetype = self.reader.get_mimetype(mimetype=obj_in.mime)
        datasource_path = self.get_source_path(obj_id=obj_in.uuid, mimetype=mimetype)
        df = self.reader.get(source=datasource_path, mimetype=mimetype, nrows=settings.WHYQD_SUMMARY_ROWS)
        if isinstance(df, dict):
            for sheet_name, dfs in df.items():
                dfs = dfs.fillna(np.nan).replace([np.nan], [None])
                jsn_obj = dfs.to_json(path_or_buf=None, orient="records")
                obj_name = f"{obj_id}-{sheet_name.lower()}.SUMMARY"
                self.core.save_file(data=jsn_obj, source=str(self.summary / obj_name))
        else:
            df = df.fillna(np.nan).replace([np.nan], [None])
            jsn_obj = df.to_json(path_or_buf=None, orient="records")
            obj_name = f"{obj_id}.SUMMARY"
            self.core.save_file(data=jsn_obj, source=str(self.summary / obj_name))

    def get_data_summary(self, *, obj_id, sheet_name: str | None = None) -> list:
        obj_in = None
        obj_name = f"{obj_id}.SUMMARY"
        if sheet_name:
            obj_name = f"{obj_id}-{sheet_name.lower()}.SUMMARY"
        obj_in = self.core.load_json(source=str(self.summary / obj_name))
        if not obj_in:
            return []
        return obj_in

    def delete_data_summary(self, *, obj_id) -> dict | None:
        for source in Path(self.summary).glob(f"{obj_id}*.SUMMARY"):
            self.core.delete_file(source=str(source))


files = CRUDFiles()
