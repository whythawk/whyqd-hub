from raven import Client
from typing import Union, List
from whyqd.parsers.datasource import DataSourceParser

from app.core.celery_app import celery_app
from app.core.config import settings
from app.worker.session import get_scoped_session
from app import crud, schemas, schema_types

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(name="app.worker.process_data_import")  # (acks_late=True)
def process_data_import(user_id: str, datasource_in: dict, task_id: Union[str, None] = None) -> str:
    # call with celery_app.send_task("app.worker.process_data_import", args=[user_id, datasource_in, task_id])
    SessionScoped = get_scoped_session()
    db = SessionScoped()
    # GET DEPENDENCIES
    user_obj = crud.user.get(db=db, id=user_id)
    datasource_in = schemas.DataSourceTemplateModel(**datasource_in)
    task_obj = None
    if task_id:
        task_obj = crud.task.get(db=db, id=task_id, user=user_obj, responsibility=schema_types.RoleType.WRANGLER)
    # PROCESS
    crud.reference.import_source(db=db, user=user_obj, datasource_in=datasource_in, task=task_obj)
    response = f"Process data import complete: {datasource_in.name}, {user_obj.email}"
    if task_obj:
        response = f"Process data import complete: {datasource_in.name}, {user_obj.email} - {task_obj.name}"
    db.close()
    SessionScoped.remove()
    return response


@celery_app.task(name="app.worker.process_schema_categorisation")  # (acks_late=True)
def process_schema_categorisation(user_id: str, resource_id: str, field_name: str, term_type: str) -> str:
    # call with celery_app.send_task("app.worker.process_schema_categorisation", args=[user_id, resource_id, field_name])
    SessionScoped = get_scoped_session()
    db = SessionScoped()
    # GET DEPENDENCIES
    user_obj = crud.user.get(db=db, id=user_id)
    resource_obj = crud.resource.get(
        db=db, id=resource_id, user=user_obj, responsibility=schema_types.RoleType.WRANGLER
    )
    # PROCESS
    as_bool = term_type == "boolean"
    crud.reference.derive_schema_categories(
        db=db, resource_obj=resource_obj, user=user_obj, field_name=field_name, as_bool=as_bool
    )
    response = f"Process schema categorisation complete: {resource_obj.name}, {field_name} - {user_obj.email}"
    db.close()
    SessionScoped.remove()
    return response


@celery_app.task(name="app.worker.process_create_multi_tasks_from_project")  # (acks_late=True)
def process_create_multi_tasks_from_project(
    user_id: str, project_id: str, models_in: List[dict], field_name: Union[str, None] = None
) -> str:
    # call with celery_app.send_task("app.worker.process_create_multi_tasks_from_project", args=[user_id, project_id, models_in, field_name])
    SessionScoped = get_scoped_session()
    db = SessionScoped()
    # GET DEPENDENCIES
    user_obj = crud.user.get(db=db, id=user_id)
    project_obj = crud.project.get(db=db, id=project_id, user=user_obj, responsibility=schema_types.RoleType.WRANGLER)
    # PROCESS
    tasks_in = [schemas.TaskCreate(**model_in) for model_in in models_in]
    crud.reference.create_multi_tasks_from_project(
        db=db, user=user_obj, project_obj=project_obj, tasks_in=tasks_in, field_name=field_name
    )
    response = f"Process bulk task creation complete: {project_obj.name} - {user_obj.email}"
    db.close()
    SessionScoped.remove()
    return response


@celery_app.task(name="app.worker.process_transform")  # (acks_late=True)
def process_transform(user_id: str, resource_id: str, mimetype: Union[str, None] = None) -> str:
    # call with celery_app.send_task("app.worker.process_transform", args=[user_id, resource_id, mimetype])
    SessionScoped = get_scoped_session()
    db = SessionScoped()
    # GET DEPENDENCIES
    user_obj = crud.user.get(db=db, id=user_id)
    resource_obj = crud.resource.get(
        db=db, id=resource_id, user=user_obj, responsibility=schema_types.RoleType.WRANGLER
    )
    if mimetype:
        reader = DataSourceParser()
        mimetype = reader.get_mimetype(mimetype=mimetype)
    # PROCESS
    crud.reference.perform_transform(db=db, resource_obj=resource_obj, mimetype=mimetype, user=user_obj)
    response = f"Process transform complete: {resource_obj.name}, {user_obj.email}"
    if mimetype:
        response = f"Process data import complete: {resource_obj.name}, {user_obj.email} - {mimetype.name}"
    db.close()
    SessionScoped.remove()
    return response
