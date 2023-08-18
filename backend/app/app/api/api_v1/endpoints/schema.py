from __future__ import annotations
from typing import Any

from fastapi import APIRouter, Depends, WebSocket, HTTPException, WebSocketException
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
from pydantic import ValidationError
from sqlalchemy.orm import Session
import randomname
import json
from uuid import UUID
from whyqd import models as qd_models

from app import crud, models, schema_types, schemas
from app.api import deps, sockets

router = APIRouter()


@router.websocket("/edit")
async def create_and_edit_schema(*, db: Session = Depends(deps.get_db), websocket: WebSocket):
    """
    Create, update, import and edit a schema model. Save, or update, as a schema reference.
    """
    current_user = None
    initialised = False
    schema_obj = None
    success = False
    # 1. Open the socket and validate current user
    await websocket.accept()
    print("OPENING-------------------------------------------------------")
    request = await sockets.receive_request(websocket=websocket)
    response = {"state": "error", "error": "Could not validate credentials."}
    if request.get("token"):
        try:
            current_user = deps.get_active_websocket_user(db=db, token=request["token"])
            response = {"state": "initialised", "data": {"name": randomname.get_name()}}
        except ValidationError:
            pass
    success = await sockets.send_response(websocket=websocket, response=response)
    if response["state"] == "initialised" and success:
        try:
            while True and success:
                # LOOP #################################################################
                request = await sockets.receive_request(websocket=websocket)
                if not request:
                    break
                ########################################################################
                print("REQUEST-------------------------------------------------------")
                print(request)
                print("--------------------------------------------------------------")
                ########################################################################
                state = request.get("state")
                data = request.get("data", {})
                data = sockets.sanitize_data_request(data)
                response = {"state": state}
                try:
                    # IMPORT SCHEMA ####################################################
                    if state == "initialiseSchema":
                        schema_definition = crud.reference.get_schema_definition(as_subject=False)
                        if data:
                            # Check if this happens to be an existing schema with a saved reference
                            if data.get("uuid"):
                                schema_obj = crud.reference.get_by_model(
                                    db=db,
                                    model_id=data["uuid"],
                                    user=current_user,
                                    responsibility=schema_types.RoleType.CURATOR,
                                )
                                if schema_obj and schema_obj.model_type != schema_types.ReferenceType.SCHEMA:
                                    schema_obj = None
                            # Do a quick validation check on the fields
                            if data.get("fields") and isinstance(data["fields"], list):
                                for field in data["fields"]:
                                    if field.get("constraints") and isinstance(field["constraints"], dict):
                                        if not isinstance(field["constraints"].get("enum"), list):
                                            field["constraints"]["enum"] = []
                            try:
                                schema_definition.set(schema=data)
                            except ValidationError:
                                if schema_obj:
                                    schema_model = crud.reference.get_model(db=db, db_obj=schema_obj)
                                    if schema_model:
                                        schema_definition.set(schema=schema_model)
                                    # something wrong with data format
                                    # TODO: fix this in an elegant way
                                    # raise ValidationError("Schema appears corrupted.")
                        initialised = True
                    # INITIALISE SCHEMA ################################################
                    if state == "loadSchema":
                        if not data.get("id"):
                            raise ValidationError("Schema cannot be found.")
                        schema_obj = crud.reference.get(
                            db=db,
                            id=data["id"],
                            user=current_user,
                            responsibility=schema_types.RoleType.CURATOR,
                        )
                        if not schema_obj or schema_obj.model_type != schema_types.ReferenceType.SCHEMA:
                            raise ValidationError("Schema cannot be found.")
                        schema_model = crud.reference.get_model(db=db, db_obj=schema_obj)
                        if not schema_model:
                            raise ValidationError("Schema cannot be found.")
                        schema_definition = crud.reference.get_schema_definition(as_subject=False)
                        schema_definition.set(schema=schema_model)
                        initialised = True
                    # SET METADATA #####################################################
                    if state == "setMetadata" and initialised:
                        # Do a quick validation check on the fields
                        if data.get("fields") and isinstance(data["fields"], list):
                            for field in data["fields"]:
                                if field.get("constraints") and isinstance(field["constraints"], dict):
                                    if not isinstance(field["constraints"].get("enum"), list):
                                        field["constraints"]["enum"] = []
                        schema_definition.set(schema=data)
                    # ADD FIELD ########################################################
                    if state == "addField" and initialised:
                        if data.get("constraints") and isinstance(data["constraints"], dict):
                            if not isinstance(data["constraints"].get("enum"), list):
                                data["constraints"]["enum"] = []
                        schema_definition.fields.add(term=data)
                    # UPDATE FIELD #####################################################
                    if state == "updateField" and initialised:
                        if data.get("constraints") and isinstance(data["constraints"], dict):
                            if not isinstance(data["constraints"].get("enum"), list):
                                data["constraints"]["enum"] = []
                        schema_definition.fields.update(term=data)
                    # REMOVE FIELD #####################################################
                    if state == "removeField" and initialised:
                        schema_definition.fields.remove(name=UUID(data["name"]))
                    # REORDER FIELD ####################################################
                    if state == "reorderFields" and initialised:
                        data = [UUID(x) for x in data]
                        schema_definition.fields.reorder(order=data)
                    # RESET FIELD ######################################################
                    if state == "resetFields" and initialised:
                        schema_definition.fields.reset()
                    # SET CITATION #####################################################
                    if state == "setCitation" and initialised:
                        schema_definition.set_sitation(citation=data)
                    # GET REFERENCE ####################################################
                    if state == "getReference" and initialised:
                        response["data"] = {"id": False}
                        if schema_obj:
                            response["data"] = {"id": str(schema_obj.id)}
                    # SAVE AND CREATE SCHEMA REFERENCE #################################
                    if state == "save" and initialised:
                        # This will close the socket, if it succeeds
                        SCHEMA_OBJECT = schema_definition.get
                        if not schema_obj:
                            schema_obj = crud.reference.create(
                                db=db,
                                user=current_user,
                                reference_in=SCHEMA_OBJECT,
                                reference_type=schema_types.ReferenceType.SCHEMA,
                            )
                        else:
                            schema_obj = crud.reference.update(
                                db=db,
                                id=schema_obj.id,
                                user=current_user,
                                reference_in=SCHEMA_OBJECT,
                                reference_type=schema_types.ReferenceType.SCHEMA,
                            )
                        response["data"] = {"id": str(schema_obj.id)}
                        break
                    if state and initialised and state not in ["getReference"]:
                        # Because UUIDs don't yet serialise AND Pydantic doesn't yet deal with this
                        # https://stackoverflow.com/q/65622045/295606
                        # TODO: https://stackoverflow.com/a/69740271/295606 when you have the time
                        response["data"] = json.loads(schema_definition.get.json(by_alias=True))
                        # Pydantic is sometimes wrecking the aliases for category ("category" instead of "enum")
                        if response["data"].get("fields") and isinstance(response["data"]["fields"], list):
                            for field in response["data"]["fields"]:
                                if field.get("constraints") and isinstance(field["constraints"], dict):
                                    if field["constraints"].get("category") and not field["constraints"].get("enum"):
                                        field["constraints"]["enum"] = field["constraints"]["category"]
                                        field["constraints"].pop("category", None)
                except ValidationError as e:
                    response = {"state": "error", "error": e}
                ########################################################################
                print("RESPOND-------------------------------------------------------")
                print(response)
                print("--------------------------------------------------------------")
                ########################################################################
                success = await sockets.send_response(websocket=websocket, response=response)
                # LOOP #################################################################
        except (WebSocketDisconnect, WebSocketException, ConnectionClosedError) as e:
            response = {"state": "error", "error": e}
    try:
        await sockets.send_response(websocket=websocket, response=response)
        await websocket.close(code=1000)
    except (WebSocketDisconnect, ConnectionClosedError, RuntimeError, WebSocketException):
        pass


@router.get("/{id}", response_model=qd_models.SchemaModel)
def read_schema_model(
    *, db: Session = Depends(deps.get_db), id: str, current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get the schema model for a schema reference.
    """
    response = crud.reference.get_model(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.SEEKER)
    if not response:
        raise HTTPException(status_code=404, detail="Maybe some things aren't meant to be found?")
    return response


@router.post("/subject/{subject_id}/object/{object_id}", response_model=schemas.ResourceManager)
def create_schema_to_schema_crosswalk(
    *,
    db: Session = Depends(deps.get_db),
    subject_id: str,
    object_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a schema-to-schema crosswalk - no data required.
    """
    schema_subject = crud.reference.get(db=db, id=subject_id, user=current_user)
    schema_object = crud.reference.get(db=db, id=object_id, user=current_user)
    if (
        not schema_subject
        or not schema_subject.model_type == schema_types.ReferenceType.SCHEMA
        or not schema_object
        or not schema_object.model_type == schema_types.ReferenceType.SCHEMA
    ):
        raise HTTPException(
            status_code=400,
            detail="Either of subject or object schemas do not exist.",
        )
    resource_obj = crud.reference.create_schema_to_schema_crosswalk(
        db=db, schema_subject=schema_subject, schema_object=schema_object, user=current_user
    )
    return resource_obj


@router.post("/task/{task_id}/schema/{subject_id}", response_model=schemas.ResourceManager)
def create_task_based_schema_to_schema_crosswalk(
    *,
    db: Session = Depends(deps.get_db),
    task_id: str,
    subject_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a schema-to-schema crosswalk - no data required. For a Task with an assigned object schema.
    """
    task_obj = crud.task.get(db=db, id=task_id, user=current_user)
    schema_subject = crud.reference.get(db=db, id=subject_id, user=current_user)
    if (
        not task_obj
        or not task_obj.schema_id
        or not schema_subject
        or not schema_subject.model_type == schema_types.ReferenceType.SCHEMA
    ):
        raise HTTPException(
            status_code=400,
            detail="Either task or schema do not exist, or user does not have the rights for this request.",
        )
    resource_obj = crud.reference.create_schema_to_schema_crosswalk(
        db=db, schema_subject=schema_subject, schema_object=task_obj.schema, task=task_obj, user=current_user
    )
    return resource_obj
