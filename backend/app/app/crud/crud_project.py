from __future__ import annotations
from typing import TYPE_CHECKING

# from fastapi.encoders import jsonable_encoder
# from pydantic import parse_obj_as
from sqlalchemy.orm import Session

# from sqlalchemy import desc, and_, or_
from uuid import UUID

# from copy import deepcopy

from app.crud.whyqd_base import CRUDWhyqdBase

# from app.crud.crud_role import role
from app.models.project import Project
from app.schemas import ProjectCreate, ProjectUpdate  # , ResearchResources, RolesCreate
from app.schema_types import RoleType

# from app.schema_types import RoleType
from app.crud.crud_activity import activity as crud_activity

# from app.schema_types import ReferenceType, ResearcherRoleType

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User
    from app.models.reference import Reference


class CRUDProject(CRUDWhyqdBase[Project, ProjectCreate, ProjectUpdate]):
    def create(self, db: Session, *, obj_in: ProjectCreate, user: User) -> Project:
        db_obj = super().create(db=db, obj_in=obj_in, user=user)
        # https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html
        for subject in obj_in.subjects:
            if subject.lower() not in db_obj.subjects:
                db_obj.subjects.append(subject.lower())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        id: UUID | str,
        obj_in: ProjectCreate,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Project:
        db_obj = super().update(db=db, id=id, obj_in=obj_in, user=user, responsibility=responsibility)
        # https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html
        db_obj.subjects = []
        for subject in obj_in.subjects:
            if subject.lower() not in db_obj.subjects:
                db_obj.subjects.append(subject.lower())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_task(self, db: Session, *, db_obj: Project, task_obj: Task) -> Project | None:
        db_obj.tasks.append(task_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_task(self, db: Session, *, db_obj: Project, task_obj: Task) -> Project | None:
        db_obj.tasks.remove(task_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_schema(
        self,
        db: Session,
        *,
        db_obj: Project,
        schema_obj: Reference,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Project | None:
        obj_in = ProjectUpdate.from_orm(db_obj)
        obj_in.schema_id = schema_obj.id
        return super().update(db=db, id=db_obj.id, obj_in=obj_in, user=user, responsibility=responsibility)

    def remove_schema(
        self,
        db: Session,
        *,
        db_obj: Project,
    ) -> Project | None:
        if not (db_obj.schema_id):
            return None
        db_obj.schema.project_schema.remove(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def record_activity(
        self,
        db: Session,
        *,
        user: User,
        db_obj: Project,
        custodians_only: bool = False,
        alert: bool = False,
        message: str = "",
    ) -> bool:
        obj_in = {
            "custodians_only": custodians_only,
            "alert": alert,
            "message": message,
            "researcher_id": user.id,
            "project_id": db_obj.id,
        }
        return crud_activity.create(db=db, obj_in=obj_in)

    # def _create_team_role(
    #     self, db: Session, *, db_obj: Project, team_member: User, team_role: ResearcherRoleType
    # ) -> Roles:
    #     role_in = RolesCreate(
    #         **{
    #             "resource_id": db_obj.id,
    #             "resource_type": ReferenceType.TEAM,
    #             "researcher_id": team_member.id,
    #             "research_roles": [team_role],
    #         }
    #     )
    #     role_obj = role.create(db=db, obj_in=role_in)
    #     return role_obj

    # def _remove_all_team_roles(self, db: Session, *, db_obj: Project, team_member: User) -> Roles:
    #     objs = (
    #         db.query(Roles).filter(and_(Roles.resource_id == db_obj.id, Roles.researcher_id == team_member.id)).delete()
    #     )
    #     db.commit()
    #     return objs

    # def create(self, db: Session, *, obj_in: ProjectCreate, user_obj: User) -> User:
    #     db_obj = Project(
    #         title=obj_in.title,
    #         description=obj_in.description,
    #     )
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     db_obj = self.append_member(db=db, db_obj=db_obj, team_member=user_obj, team_role=ResearcherRoleType.CUSTODIAN)
    #     return db_obj

    # def append_member(
    #     self,
    #     db: Session,
    #     *,
    #     db_obj: Project,
    #     team_member: User,
    #     team_role: ResearcherRoleType = ResearcherRoleType.SEEKER,
    # ) -> Project:
    #     # https://stackoverflow.com/questions/25668092/flask-sqlalchemy-many-to-many-insert-data
    #     # Default is seeker role
    #     self._create_team_role(db=db, db_obj=db_obj, team_member=team_member, team_role=team_role)
    #     db_obj.members.append(team_member)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def remove_member(self, db: Session, *, db_obj: Project, team_member: User) -> Project:
    #     self._remove_all_team_roles(db=db, db_obj=db_obj, team_member=team_member)
    #     db_obj.members.remove(team_member)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def append_project(self, db: Session, *, db_obj: Project, id: UUID) -> Project:
    #     id_in_obj = id
    #     if not isinstance(id_in_obj, UUID):
    #         id_in_obj = UUID(id)
    #     # Commit the resource to the team
    #     resource_in = ResearchResources(**{"resource_id": id_in_obj, "resource_type": ReferenceType.PROJECT})
    #     db_obj = self.append_resource(db=db, db_obj=db_obj, resource=resource_in)
    #     # Commit the project to the team
    #     id_in_obj = jsonable_encoder(id_in_obj)
    #     obj_original_data = deepcopy(db_obj.projects)
    #     if not obj_original_data:
    #         obj_original_data = []
    #     obj_original_data = set(obj_original_data)
    #     obj_original_data.add(id_in_obj)
    #     db_obj.projects = list(obj_original_data)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def remove_project(self, db: Session, *, db_obj: Project, id: UUID) -> Project:
    #     id_in_obj = id
    #     if not isinstance(id_in_obj, UUID):
    #         id_in_obj = UUID(id)
    #     # Commit the resource to the team
    #     resource_in = ResearchResources(**{"resource_id": id_in_obj, "resource_type": ReferenceType.PROJECT})
    #     db_obj = self.remove_resource(db=db, db_obj=db_obj, resource=resource_in)
    #     # Commit the project to the team
    #     # id_in_obj = jsonable_encoder(id_in_obj)
    #     obj_original_data = deepcopy(db_obj.projects)
    #     try:
    #         obj_original_data.remove(id_in_obj)
    #     except (AttributeError, ValueError) as e:
    #         # There either isn't a list of resources, or the resource isn't in the list
    #         # Should decide if we want to return an error?
    #         print(e)
    #         print(id_in_obj)
    #         return db_obj
    #     db_obj.projects = obj_original_data
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def append_resource(self, db: Session, *, db_obj: Project, resource: ResearchResources) -> Project:
    #     obj_in_data = jsonable_encoder(resource)
    #     obj_original_data = deepcopy(db_obj.resources)
    #     if not obj_original_data:
    #         obj_original_data = []
    #     if obj_in_data in obj_original_data:
    #         # Do nothing
    #         return db_obj
    #     obj_original_data.append(obj_in_data)
    #     db_obj.resources = list(obj_original_data)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def remove_resource(self, db: Session, *, db_obj: Project, resource: ResearchResources) -> Project:
    #     obj_in_data = jsonable_encoder(resource)
    #     obj_original_data = deepcopy(db_obj.resources)
    #     try:
    #         obj_original_data.remove(obj_in_data)
    #     except (AttributeError, ValueError):
    #         # There either isn't a list of resources, or the resource isn't in the list
    #         # Should decide if we want to return an error?
    #         return db_obj
    #     db_obj.resources = obj_original_data
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def get_multi_by_membership(
    #     self, db: Session, *, skip: int = 0, limit: int = 100, member_id: UUID
    # ) -> List[Project]:
    #     # https://stackoverflow.com/questions/36916072/flask-sqlalchemy-filter-on-many-to-many-relationship-with-parent-model
    #     return (
    #         db.query(self.model)
    #         .filter(Project.members.any(User.id == member_id))
    #         # .join(Project.members, Roles)
    #         # .filter(Project.members.any(User.roles.any((Roles.resource_id == Project.id))))
    #         .order_by(desc("created"))
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

    # def get_all_by_membership_and_role(self, db: Session, *, member_id: UUID) -> List[Project]:
    #     # https://stackoverflow.com/questions/36916072/flask-sqlalchemy-filter-on-many-to-many-relationship-with-parent-model
    #     return (
    #         db.query(self.model)
    #         .filter(
    #             and_(
    #                 Project.resources != None,
    #                 Project.members.any(
    #                     User.roles.any(
    #                         and_(
    #                             Roles.resource_id == Project.id,
    #                             Roles.researcher_id == member_id,
    #                             Roles.resource_type == ReferenceType.TEAM,
    #                         )
    #                     )
    #                 ),
    #             )
    #         )
    #         .all()
    #     )

    # def get_team_by_membership_and_resource(
    #     self,
    #     db: Session,
    #     *,
    #     member_id: UUID,
    #     resource_id: UUID,
    #     resource_type: ReferenceType,
    # ) -> Project:
    #     # For finding teams which contain a specific project, collection or dataset
    #     resource_in = {"resource_id": str(resource_id), "resource_type": resource_type.value}
    #     return (
    #         db.query(self.model)
    #         .filter(
    #             and_(
    #                 and_(
    #                     Project.resources != None,
    #                     Project.resources.contains([resource_in]),
    #                 ),
    #                 Project.members.any(
    #                     User.roles.any(
    #                         and_(
    #                             Roles.resource_id == Project.id,
    #                             Roles.researcher_id == member_id,
    #                             Roles.resource_type == ReferenceType.TEAM,
    #                         )
    #                     )
    #                 ),
    #             )
    #         )
    #         .first()
    #     )

    # def get_multi_resources_by_user(
    #     self,
    #     db: Session,
    #     *,
    #     skip: int = 0,
    #     limit: int = 100,
    #     member_id: UUID,
    #     resource_type: ReferenceType,
    # ) -> List[ResearchResources]:
    #     team_objs = self.get_all_by_membership_and_role(db=db, member_id=member_id)
    #     resources = [
    #         ResearchResources(**resource)
    #         for team in team_objs
    #         for resource in team.resources
    #         if resource["resource_type"] == resource_type
    #     ]
    #     return resources[skip : limit + skip]

    # def get_multi_resources_by_team(
    #     self,
    #     *,
    #     skip: int = 0,
    #     limit: int = 100,
    #     db_obj: Project,
    #     resource_type: ReferenceType,
    # ) -> List[ResearchResources]:
    #     resources = [
    #         ResearchResources(**resource) for resource in db_obj.resources if resource["resource_type"] == resource_type
    #     ]
    #     return resources[skip : limit + skip]


project = CRUDProject(Project)
