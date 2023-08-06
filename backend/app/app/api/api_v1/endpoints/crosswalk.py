from __future__ import annotations
from typing import Any

from fastapi import APIRouter, Depends, WebSocket, HTTPException, WebSocketException
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
from pydantic import ValidationError
from sqlalchemy.orm import Session
import json
from uuid import UUID

from app import crud, models, schemas, schema_types
from app.api import deps, sockets

router = APIRouter()


@router.websocket("/edit/{id}")
async def create_or_edit_crosswalk(*, db: Session = Depends(deps.get_db), id: str, websocket: WebSocket):
    """
    Create, update, import and edit a crosswalk model. Save, or update, as a crosswalk reference.
    """
    current_user = None
    initialised = False
    resource_obj = None
    crosswalk_obj = None
    crosswalk_dfn = None
    success = False
    # 1. Open the socket and validate current user
    #    The principle: load an existing reference. User cannot change the schemas. That is done from the resource as
    #    this may have knockons to other resources using the same crosswalk.
    await websocket.accept()
    request = await sockets.receive_request(websocket=websocket)
    response = {"state": "error", "error": "Could not validate credentials."}
    if request.get("token"):
        try:
            current_user = deps.get_active_websocket_user(db=db, token=request["token"])
            response = {
                "state": "error",
                "error": "Either resource does not exist, or user does not have the rights for this request.",
            }
            crosswalk_obj = crud.reference.get(
                db=db, id=id, user=current_user, responsibility=schema_types.RoleType.WRANGLER
            )
            if crosswalk_obj:
                resource_obj = crosswalk_obj.crosswalks.first()
            else:
                # This is a creation step
                resource_obj = crud.resource.get(
                    db=db, id=id, user=current_user, responsibility=schema_types.RoleType.WRANGLER
                )
            if resource_obj:
                data = crud.reference.get_resource_crosswalk_manager(
                    db=db, db_obj=resource_obj, user=current_user, responsibility=schema_types.RoleType.WRANGLER
                )
                if data:
                    response = {"state": "initialised", "data": json.loads(data.json(by_alias=True))}
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
                    # INITIALISE CROSSWALK ####################################################
                    if state == "initialiseCrosswalk":
                        # Used to reinitialise
                        crosswalk_dfn = crud.reference.get_crosswalk_definition(db_obj=resource_obj)
                        initialised = True
                    # LOAD CROSSWALK ##########################################################
                    if state == "loadCrosswalk":
                        # For local versions that have yet to be saved
                        crosswalk_dfn = crud.reference.get_crosswalk_definition(db_obj=resource_obj)
                        crosswalk_dfn.actions.reset()
                        crosswalk_dfn.actions.add_multi(terms=data["actions"])
                        crosswalk_dfn.model.name = data["metadata"]["name"]
                        crosswalk_dfn.model.title = data["metadata"].get("title")
                        crosswalk_dfn.model.description = data["metadata"].get("description")
                        initialised = True
                    # SET METADATA #####################################################
                    if state == "setMetadata" and initialised:
                        response["data"] = {"metadata": {}}
                        if data.get("name"):
                            crosswalk_dfn.get.name = data["name"]
                            crosswalk_dfn.get.title = data.get("title")
                            crosswalk_dfn.get.description = data.get("description")
                            response["data"] = {"metadata": data}
                    # ADD ACTION ########################################################
                    if state == "addAction" and initialised:
                        crosswalk_dfn.actions.add(term=data)
                    # UPDATE ACTION #####################################################
                    if state == "updateAction" and initialised:
                        crosswalk_dfn.actions.update(term=data)
                    # REMOVE ACTION #####################################################
                    if state == "removeAction" and initialised:
                        crosswalk_dfn.actions.remove(name=UUID(data["name"]))
                    # REORDER ACTION ####################################################
                    if state == "reorderActions" and initialised:
                        data = [UUID(x) for x in data]
                        crosswalk_dfn.actions.reorder(order=data)
                    # RESET ACTION ######################################################
                    if state == "resetActions" and initialised:
                        crosswalk_dfn.actions.reset()
                    # SET CITATION #####################################################
                    if state == "setCitation" and initialised:
                        crosswalk_dfn.set_sitation(citation=data)
                    # SAVE AND CREATE CROSSWALK REFERENCE #################################
                    if state == "save" and initialised:
                        # This will close the socket, if it succeeds
                        CROSSWALK = crosswalk_dfn.get
                        if not crosswalk_obj:
                            crosswalk_obj = crud.reference.create(
                                db=db,
                                user=current_user,
                                reference_in=CROSSWALK,
                                reference_type=schema_types.ReferenceType.CROSSWALK,
                            )
                        else:
                            crosswalk_obj = crud.reference.update(
                                db=db,
                                id=crosswalk_obj.id,
                                user=current_user,
                                reference_in=CROSSWALK,
                                reference_type=schema_types.ReferenceType.CROSSWALK,
                            )
                        if not resource_obj.crosswalk_id or resource_obj.crosswalk_id != crosswalk_obj.id:
                            resource_in = schemas.ResourceUpdate.from_orm(resource_obj)
                            resource_in.crosswalk_id = crosswalk_obj.id
                            crud.resource.update(
                                db=db,
                                id=resource_obj.id,
                                obj_in=resource_in,
                                user=current_user,
                                responsibility=schema_types.RoleType.WRANGLER,
                            )
                        response["data"] = {"id": str(crosswalk_obj.id)}
                        break
                    if state and initialised and state not in ["setMetadata"]:
                        data = []
                        for action in crosswalk_dfn.actions.get_all():
                            uuid = action.uuid
                            action = crosswalk_dfn.actions.parse(script=action.script)
                            data.append(crud.reference.parse_action_model(uuid=uuid, term=action).dict(by_alias=True))
                        response["data"] = {"actions": data}
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


@router.get("/{id}", response_model=schemas.ResourceCrosswalkManager)
def read_resource_crosswalk_manager(
    *, db: Session = Depends(deps.get_db), id: str, current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get the resource crosswalk model for a resource.
    """
    response = None
    reference_obj = crud.reference.get(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.SEEKER)
    if reference_obj and reference_obj.model_type == schema_types.ReferenceType.CROSSWALK:
        resource_obj = reference_obj.crosswalks.first()
    else:
        # Gives a few options depending on where this is coming from
        resource_obj = crud.resource.get(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.SEEKER)
    if resource_obj:
        response = crud.reference.get_resource_crosswalk_manager(
            db=db, db_obj=resource_obj, user=current_user, responsibility=schema_types.RoleType.SEEKER
        )
    if not resource_obj or not response:
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    return response
