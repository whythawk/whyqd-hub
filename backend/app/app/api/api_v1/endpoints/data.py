from __future__ import annotations
from typing import Any, List
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Form
from sqlalchemy.orm import Session
import json
import io

from app import crud, models, schemas, schema_types
from app.core.celery_app import celery_app
from app.api import deps

# from app.core.config import settings

router = APIRouter()


def datasource_validator(data: str = Form(...)):
    # https://stackoverflow.com/questions/65504438/how-to-add-both-file-and-json-body-in-a-fastapi-post-request/70640522#70640522
    # https://stackoverflow.com/questions/65342833/fastapi-uploadfile-is-slow-compared-to-flask/70667530#70667530
    # https://stackoverflow.com/questions/63048825/how-to-upload-file-using-fastapi/70657621#70657621
    try:
        model = schemas.DataSourceTemplateModel.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return model


@router.post("/upload/", response_model=schemas.Msg)
async def create_upload_files(
    *,
    db: Session = Depends(deps.get_db),
    data: schemas.DataSourceTemplateModel = Depends(datasource_validator),
    files: List[UploadFile] = File(...),
    current_user: models.User = Depends(deps.get_subscribed_user),
) -> Any:
    for source in files:
        try:
            datasource_in = crud.files.import_source_from_upload(source=source, datasource_in=data)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=e,
            )
        datasource_in = json.loads(datasource_in.json(by_alias=True))
        celery_app.send_task("app.worker.process_data_import", args=[current_user.id, datasource_in, None])
    return {
        "msg": "Source files successfully uploaded. Check your activity log to see when they're ready to process further."
    }


@router.post("/upload/task/{id}", response_model=schemas.Msg)
async def create_upload_files_for_task(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    files: List[UploadFile] = File(...),
    data: schemas.DataSourceTemplateModel = Depends(datasource_validator),
    current_user: models.User = Depends(deps.get_subscribed_user),
) -> Any:
    task_obj = crud.task.get(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.CURATOR)
    if not task_obj:
        raise HTTPException(
            status_code=400,
            detail="Either the task does not exist, or you do not have the rights for this request.",
        )
    for source in files:
        try:
            datasource_in = crud.files.import_source_from_upload(source=source, datasource_in=data)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=e,
            )
        datasource_in = json.loads(datasource_in.json(by_alias=True))
        celery_app.send_task("app.worker.process_data_import", args=[current_user.id, datasource_in, task_obj.id])
    return {
        "msg": "Source files successfully uploaded. Check your activity log to see when they're ready to process further."
    }


@router.get("/download/model/{id}", response_class=StreamingResponse)
def download_reference_model(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Download a JSON model from a reference.
    """
    reference_obj = crud.reference.get(db=db, id=id, user=current_user)
    if not reference_obj:
        raise HTTPException(
            status_code=400,
            detail="Either the reference does not exist, or you do not have the rights for this request.",
        )
    model_obj = crud.reference.get_model(db_obj=reference_obj)
    if not model_obj:
        raise HTTPException(
            status_code=400,
            detail="Either the reference does not exist, or you do not have the rights for this request.",
        )
    # https://stackoverflow.com/a/69799463/295606
    stream = io.StringIO(model_obj.json(by_alias=True))
    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={model_obj.name}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/download/source/{id}", response_model=None)
async def download_reference_data(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> StreamingResponse:
    """
    Download source data from a reference. Must be of "DATA" or "DATASOURCE" type.
    """
    stream = None
    reference_obj = crud.reference.get(db=db, id=id, user=current_user)
    if reference_obj and reference_obj.model_type == schema_types.ReferenceType.DATA:
        # It will be either of DATA or TRANSFORMDATA
        resource_obj = reference_obj.data.first()
        if resource_obj:
            reference_obj = resource_obj.datasource
        else:
            resource_obj = reference_obj.transformdata.first()
            if resource_obj:
                reference_obj = resource_obj.transformdatasource
    if reference_obj and reference_obj.model_type == schema_types.ReferenceType.DATASOURCE:
        model_obj = crud.reference.get_model(db_obj=reference_obj)
        if model_obj:
            mime = crud.files.reader.get_mimetype(mimetype=model_obj.mime)
            stream = crud.files.get_data_stream(obj_id=model_obj.uuid, mimetype=mime)
    if not stream:
        raise HTTPException(
            status_code=400,
            detail="Either the reference does not exist, or you do not have the rights for this request.",
        )
    media_type = "application/octet-stream"
    if mime in [schema_types.MimeType.CSV, schema_types.MimeType.XLS, schema_types.MimeType.XLSX]:
        media_type = mime.value
    return StreamingResponse(
        content=stream,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={model_obj.name}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
