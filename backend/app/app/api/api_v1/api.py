from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login,
    users,
    proxy,
    services,
    activities,
    data,
    reference,
    schema,
    crosswalk,
    template,
    resource,
    task,
    project,
)

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])
api_router.include_router(services.router, prefix="/service", tags=["service"])
api_router.include_router(activities.router, prefix="/activity", tags=["activity"])
api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(reference.router, prefix="/reference", tags=["reference"])
api_router.include_router(schema.router, prefix="/schema", tags=["schema"])
api_router.include_router(crosswalk.router, prefix="/crosswalk", tags=["crosswalk"])
api_router.include_router(template.router, prefix="/template", tags=["template"])
api_router.include_router(resource.router, prefix="/resource", tags=["resource"])
api_router.include_router(task.router, prefix="/task", tags=["task"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
