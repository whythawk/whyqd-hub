from __future__ import annotations
from sqlalchemy.orm import Session, Query

# from app.schema_types import ReferenceType

# from pydantic import parse_obj_as
# from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate  # , Role as RoleInDB
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.resource import Resource
from app.models.reference import Reference
from app.models.reference_template import ReferenceTemplate
from app.schema_types import RoleType


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def create(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
        db_obj: Project | Task | Resource | Reference | ReferenceTemplate,
        is_validated: bool = False,
    ) -> Role:
        obj_in = {"researcher_id": user.id, "responsibility": responsibility, "is_validated": is_validated}
        obj_in[self._get_by_type(db_obj=db_obj)] = db_obj.id
        obj_in = RoleCreate(**obj_in)
        return super().create(db=db, obj_in=obj_in)

    def extend(
        self,
        db: Session,
        *,
        user: User,
        old_obj: Project | Task | Resource | Reference | ReferenceTemplate,
        new_obj: Project | Task | Resource | Reference | ReferenceTemplate,
    ) -> None:
        db_objs = (
            db.query(Role)
            .filter(
                (self._get_by_type(db_obj=old_obj, as_model=True) == old_obj.id) & (self.model.researcher_id != user.id)
            )
            .all()
        )
        for obj in db_objs:
            obj_in = RoleUpdate.from_orm(obj).dict()
            for term in ["created", "id", self._get_by_type(db_obj=old_obj)]:
                # The two resources don't have to be the same so pop it here
                obj_in.pop(term, None)
            obj_in[self._get_by_type(db_obj=new_obj)] = new_obj.id
            obj_in = RoleCreate(**obj_in)
            super().create(db=db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: Role, responsibility: RoleType = RoleType.SEEKER) -> Role:
        obj_in = RoleUpdate.from_orm(db_obj)
        obj_in.responsibility = responsibility
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def validate(self, db: Session, *, db_obj: Role) -> Role:
        obj_in = RoleUpdate.from_orm(db_obj)
        obj_in.is_validated = True
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def _get_responsibility(self, *, responsibility: RoleType) -> list[RoleType]:
        responsibilities = [RoleType.CUSTODIAN]
        if responsibility == RoleType.CURATOR:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR]
        if responsibility == RoleType.WRANGLER:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR, RoleType.WRANGLER]
        if responsibility == RoleType.SEEKER:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR, RoleType.WRANGLER, RoleType.SEEKER]
        return responsibilities

    def _get_filter(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType,
        db_obj: Project | Task | Resource | Reference | ReferenceTemplate,
    ) -> Query | None:
        query = db.query(self.model)
        responsibilities = self._get_responsibility(responsibility=responsibility)
        filter = (
            (self.model.researcher_id == user.id)
            & (self.model.responsibility.in_(responsibilities))
            & (self.model.is_validated)
        )
        if isinstance(db_obj, Project):
            return query.filter(filter & (self.model.project_id == db_obj.id))
        if isinstance(db_obj, Task):
            return query.filter(filter & (self.model.task_id == db_obj.id))
        if isinstance(db_obj, Resource):
            return query.filter(filter & (self.model.resource_id == db_obj.id))
        if isinstance(db_obj, Reference):
            return query.filter(filter & (self.model.reference_id == db_obj.id))
        if isinstance(db_obj, ReferenceTemplate):
            return query.filter(filter & (self.model.referencetemplate_id == db_obj.id))
        return None

    def has_responsibility(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType,
        db_obj: Project | Task | Resource | Reference | ReferenceTemplate,
    ) -> bool:
        if user.is_superuser:
            return True
        query = self._get_filter(db=db, user=user, responsibility=responsibility, db_obj=db_obj)
        if query:
            return query.first() is not None
        return False

    def _get_by_type(
        self, *, db_obj: Project | Task | Resource | Reference | ReferenceTemplate, as_model: bool = False
    ) -> str:
        # This will fail if the `rtn_obj` doesn't have these terms
        if isinstance(db_obj, Project):
            if as_model:
                return self.model.project_id
            return "project_id"
        if isinstance(db_obj, Task):
            if as_model:
                return self.model.task_id
            return "task_id"
        if isinstance(db_obj, Resource):
            if as_model:
                return self.model.resource_id
            return "resource_id"
        if isinstance(db_obj, Reference):
            if as_model:
                return self.model.reference_id
            return "reference_id"
        if isinstance(db_obj, ReferenceTemplate):
            if as_model:
                return self.model.referencetemplate_id
            return "referencetemplate_id"

    # def get_by_terms(self, db: Session, *, obj_in: RoleUpdate | RoleCreate) -> Optional[Role]:
    #     return (
    #         db.query(self.model)
    #         .filter(
    #             and_(
    #                 self.model.resource_id == obj_in.resource_id,
    #                 self.model.researcher_id == obj_in.researcher_id,
    #                 self.model.resource_type == obj_in.resource_type,
    #             )
    #         )
    #         .first()
    #     )

    # def create_or_update(self, db: Session, *, obj_in: Union[RolesUpdate, RolesCreate]) -> Roles:
    #     db_obj = self.get_by_terms(db=db, obj_in=obj_in)
    #     if not db_obj:
    #         # CREATE
    #         db_obj = self.create(db=db, obj_in=obj_in)
    #         return db_obj
    #     # UPDATE - only need to check and set 'research_roles'
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     field = "research_roles"
    #     if field not in update_data:
    #         return db_obj
    #     # Check the role types for uniqueness and completeness (i.e. if has CUSTODIAN, doesn't need the others)
    #     research_roles = list(set(update_data[field]))
    #     if ResearcherRoleType.CUSTODIAN in research_roles:
    #         research_roles = [ResearcherRoleType.CUSTODIAN]
    #     setattr(db_obj, field, research_roles)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def teams(self, user: User) -> List[Team]:
    #     return user.teams  # .all()

    # def roles(self, user: User) -> List[Roles]:
    #     return user.roles  # .all()

    # def can_modify_role(self, *, user: User, role_in: RolesInDB, role: Optional[Roles] = None) -> bool:
    #     if user.is_superuser:
    #         return True
    #     if role:
    #         if user.id == role_in.researcher_id and user.id == role.researcher_id:
    #             return True
    #     else:
    #         if user.id == role_in.researcher_id:
    #             return True
    #     return False

    # def can_view_resource(self, *, user: User, resource: ResearchResources) -> bool:
    #     # A member can view all resources in a team where they have any role.
    #     if user.is_superuser:
    #         return True
    #     roles = parse_obj_as(List[RolesInDB], self.roles(user))
    #     for role in roles:
    #         user_resource = ResearchResources(**{"resource_id": role.resource_id, "resource_type": role.resource_type})
    #         if resource == user_resource:
    #             return True
    #     return False

    # def has_researcher_role(
    #     self, *, user: User, has_role: Optional[ResearcherRoleType] = None, research_roles: List[ResearcherRoleType]
    # ) -> bool:
    #     if user.is_superuser:
    #         return True
    #     return has_role in research_roles

    # def can_modify_resource(
    #     self, user: User, resource: ResearchResources, has_role: Optional[ResearcherRoleType] = None
    # ) -> bool:
    #     if user.is_superuser:
    #         return True
    #     # Role permits modification of resource RolesInDB
    #     roles = parse_obj_as(List[RolesInDB], self.roles(user))
    #     for role in roles:
    #         user_resource = ResearchResources(**{"resource_id": role.resource_id, "resource_type": role.resource_type})
    #         if resource != user_resource:
    #             continue
    #         if has_role and (
    #             self.has_researcher_role(user=user, has_role=has_role, research_roles=role.research_roles)
    #             or self.has_researcher_role(
    #                 user=user, has_role=ResearcherRoleType.CUSTODIAN, research_roles=role.research_roles
    #             )
    #         ):
    #             return True
    #         elif set(role.research_roles) - set([ResearcherRoleType.SEEKER]):
    #             return True
    #         else:
    #             return False
    #     return False

    # def get_multi_members_by_resource(
    #     self, db: Session, *, skip: int = 0, limit: int = 100, resource: ResearchResources
    # ) -> List[Roles]:
    #     return (
    #         db.query(self.model)
    #         .filter(and_(Roles.resource_id == resource.resource_id, Roles.resource_type == resource.resource_type))
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

    # def get_custodial_team_member_subscriptions(self, db: Session, *, custodian: User) -> List[User]:
    #     team_ids = [
    #         r.resource_id
    #         for r in custodian.roles
    #         if ResearcherRoleType.CUSTODIAN in r.research_roles and r.resource_type == ReferenceType.TEAM
    #     ]
    #     role_objs = (
    #         db.query(self.model)
    #         .filter(and_(Roles.resource_id.in_(team_ids), Roles.resource_type == ReferenceType.TEAM))
    #         .all()
    #     )
    #     return set([r.researcher for r in role_objs if r.researcher.is_active == True])

    # def get_multi_members_by_resource_and_role(
    #     self, db: Session, *, skip: int = 0, limit: int = 100, resource: ResearchResources, has_role: ResearcherRoleType
    # ) -> List[Roles]:
    #     # https://stackoverflow.com/a/23545530/295606
    #     return (
    #         db.query(self.model)
    #         .filter(
    #             and_(
    #                 Roles.resource_id == resource.resource_id,
    #                 Roles.resource_type == resource.resource_type,
    #                 Roles.research_roles.contains([has_role]),
    #             )
    #         )
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

    # def can_remove_custodial_role_from_resource(
    #     self,
    #     db: Session,
    #     *,
    #     resource: ResearchResources,
    # ) -> List[Roles]:
    #     # Complex one ... if the team member is the last custodian, they can neither remove themselves, nor change their
    #     # role. They must first add someone else in that role. Or they must delete the team.
    #     custodians = self.get_multi_members_by_resource_and_role(
    #         db=db, resource=resource, has_role=ResearcherRoleType.CUSTODIAN
    #     )
    #     return len(custodians) > 1


role = CRUDRole(Role)
