from .crud_user import user  # noqa: F401
from .crud_token import token  # noqa: F401
from .crud_ogun import ogun  # noqa: F401
from .crud_oguntoken import oguntoken  # noqa: F401

from .crud_product import product, price  # noqa: F401
from .crud_order import order  # noqa: F401
from .crud_subscription import subscription  # noqa: F401
from .crud_transform_activity import transform_activity  # noqa: F401

from .crud_spaces import spaces  # noqa: F401
from .crud_files import files  # noqa: F401

# from .crud_source import source  # noqa: F401

# WHYQD
from .crud_reference import reference  # noqa: F401
from .crud_referencetemplate import referencetemplate  # noqa: F401
from .crud_resource import resource  # noqa: F401
from .crud_task import task  # noqa: F401
from .crud_project import project  # noqa: F401
from .crud_invitation import invitation  # noqa: F401
from .crud_role import role  # noqa: F401
from .crud_activity import activity  # noqa: F401

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
