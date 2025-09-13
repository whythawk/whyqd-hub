from __future__ import annotations
from typing import Optional, List, Union, Dict
import urllib
import base64
import json
import sys
import hashlib
from pathlib import Path
from botocore.response import StreamingBody

# import pandas as pd
import modin.pandas as pd
from pandas import util as pd_util
import locale
from sqlalchemy.orm import Session
from sqlalchemy import and_
import celery.bin.amqp

from app.crud.base import CRUDBase
from app.crud.crud_spaces import spaces as crud_spaces
from app import crud as enqueue
from app.models import SourceHistory, DataPublishingAuthority
from app.schema_types import SourceDataType
from app.schema_types.mime import MimeType
from app.core.config import settings
from app.core.celery_app import celery_app


class CRUDSource(CRUDBase[SourceHistory, SourceHistoryCreate, SourceHistoryUpdate]):
    def exists(
        self, *, db: Session, data: SourceDataType, name: Optional[str] = None, checksum: Optional[str] = None
    ) -> bool:
        if not name and not checksum:
            raise ValueError("Provide at least one of either `name` or `checksum` to validate source exists.")
        if name:
            f = and_(self.model.data == data, self.model.name == name)
        if name and checksum:
            f = and_(f, self.model.checksum == checksum)
        if not name and checksum:
            f = and_(self.model.data == data, self.model.checksum == checksum)
        if db.query(self.model).filter(f).first():
            return True
        return False

    def get_by_checksum(self, db: Session, checksum: str) -> Optional[SourceHistory]:
        return db.query(self.model).filter(self.model.checksum == checksum).first()

    ###################################################################################################
    # SOURCE DEFINITION GENERIC LOAD & SAVE
    ###################################################################################################

    def get_definition_sources(self, *, source_type: SourceDataType) -> List[SourceFile]:
        return [
            SourceFile(**{"filename": f, "type": source_type})
            for f in crud_spaces.get_definition_list(team_id=self.team_id, source_type=source_type)
        ]

    def get_definition(self, *, obj_in: SourceFile) -> Optional[SourceDefinitionMake]:
        save_obj = crud_spaces.get(team_id=self.team_id, filename=obj_in.filename, source_type=obj_in.type)
        if not save_obj:
            return None
        # save_obj = json.loads(save_obj.decode("utf8"))
        obj_out = {"source": obj_in.model_dump(exclude_unset=True), "definition": save_obj}
        return SourceDefinitionMake(**obj_out)

    def save_definition(self, *, obj_in: SourceDefinitionMake) -> None:
        # Mechanism to preserve a source definition and wrangling actions. May be many, depending on events.
        save_obj = base64.b64encode(obj_in.definition.json().encode())
        crud_spaces.create(
            team_id=self.team_id,
            source_type=obj_in.source.type,
            filename=obj_in.source.filename,
            source=save_obj,
        )

    ###################################################################################################
    # SOURCE HISTORY AND TASK IMPLEMENTATION
    ###################################################################################################

    def get_source_history(
        self, db: Session, *, source_type: Optional[SourceDataType] = None, skip: int = 0, limit: int = 50
    ) -> List[SourceHistory]:
        query = db.query(self.model)
        if source_type:
            query = query.filter(self.model.data == source_type)
        return query.order_by(self.model.created.desc()).offset(skip).limit(limit).all()

    def enqueue_task(self, *, obj_in: SourceFile) -> bool:
        tasks = {
            "POINT": enqueue.point.task,
            "BOUNDARY": enqueue.boundary.task,
            "VALUATION": enqueue.valuation.task,
            "OCCUPATION": enqueue.occupier.task,
            "OWNERSHIP": None,
            "EMPLOYMENT": None,
            "DEMOGRAPHY": enqueue.demography.task,
            "REPORT": enqueue.report.task,
            "SHARED": None,
        }
        if not tasks.get(obj_in.type.value):
            # Nothing to do here.
            return False
        task = tasks.get(obj_in.type.value)
        task(dfn_name=obj_in.filename)
        return True

    def initialise_database(self, *, db: Session) -> bool:
        if db.query(DataPublishingAuthority).first():
            # Gotten all the way to adding legacy publishers, so
            # data already added to db ... therefore don't initialise.
            return False
        celery_app.send_task("app.worker.initialise_structure_and_legacy_data")
        return True

    # def get_task_queue():
    #     """
    #     Return a formated list of tasks currently run by Celery.
    #     """
    #     i = celery_app.control.inspect()
    #     active = [
    #         {k: v for k, v in row.items() if k in ["id", "name", "args", "kwargs"]}
    #         for row in [c for c in i.active().values()][0]
    #     ]
    #     return active

    def get_celery_active_tasks(self) -> List[str]:
        i = celery_app.control.inspect()
        active = [{k: v for k, v in row.items() if k in ["name"]} for row in [c for c in i.active().values()][0]]
        return [a["name"].split(".")[-1] for a in active]

    # def get_celery_active_tasks(self, *, queue_name: str = "main-queue") -> List[str]:
    #     # https://stackoverflow.com/a/57807913/295606
    #     connection = celery_app.connection()
    #     try:
    #         channel = connection.channel()
    #         name_, tasks, consumers_ = channel.queue_declare(queue=queue_name, passive=True)
    #         active_tasks = []

    #         def dump_message(message):
    #             active_tasks.append(message.properties["application_headers"]["task"])

    #         channel.basic_consume(queue=queue_name, callback=dump_message)

    #         for _ in range(tasks):
    #             connection.drain_events()

    #         return active_tasks
    #     finally:
    #         connection.close()

    def purge_celery_queue(self, *, queue_name: str = "main-queue"):
        # Throw the boat at it and make sure nothing is running
        # https://stackoverflow.com/a/24463916/295606
        # Purge queue
        amqp = celery.bin.amqp.amqp(app=celery_app)
        amqp.run("queue.purge", queue_name)
        # Purge active
        # https://stackoverflow.com/a/9369466/295606
        inspect = celery_app.control.inspect()
        task_owner = next(iter(inspect.active()))
        rvk = [r["id"] for r in inspect.active()[task_owner]]
        inspect.app.control.revoke(rvk, terminate=True)
        # Purge reserved
        task_owner = next(iter(inspect.reserved()))
        rvk = [r["id"] for r in inspect.reserved()[task_owner]]
        inspect.app.control.revoke(rvk, terminate=True)
        celery_app.control.purge()


source = CRUDSource(SourceHistory)
