"""API and search models

Revision ID: 9bccec5f4ea9
Revises: 9974bd3c5638
Create Date: 2023-07-05 20:58:44.276927

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import TSVectorType

# revision identifiers, used by Alembic.
revision = "9bccec5f4ea9"
down_revision = "9974bd3c5638"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ogunuser",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("access_key", sa.UUID(), nullable=False),
        sa.Column("secret_key", sa.String(), nullable=False),
        sa.Column("authorises_id", sa.UUID(), nullable=False),
        sa.Column(
            "responsibility",
            postgresql.ENUM(
                "CUSTODIAN",
                "CURATOR",
                "WRANGLER",
                "SEEKER",
                name="roletype",
                create_type=False,
                checkfirst=True,
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["authorises_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ogunuser_access_key"), "ogunuser", ["access_key"], unique=True)
    op.create_index(op.f("ix_ogunuser_id"), "ogunuser", ["id"], unique=False)
    op.add_column(
        "project",
        sa.Column(
            "name_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"name\")", persisted=True),
            nullable=False,
        ),
    )
    op.add_column(
        "project",
        sa.Column(
            "title_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
            nullable=True,
        ),
    )
    op.add_column(
        "project",
        sa.Column(
            "description_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_project_description_vector", "project", ["description_vector"], unique=False, postgresql_using="gin"
    )
    op.create_index("ix_project_name_vector", "project", ["name_vector"], unique=False, postgresql_using="gin")
    op.create_index("ix_project_title_vector", "project", ["title_vector"], unique=False, postgresql_using="gin")
    op.add_column(
        "reference",
        sa.Column(
            "name_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"name\")", persisted=True),
            nullable=False,
        ),
    )
    op.add_column(
        "reference",
        sa.Column(
            "title_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
            nullable=True,
        ),
    )
    op.add_column(
        "reference",
        sa.Column(
            "description_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_reference_description_vector", "reference", ["description_vector"], unique=False, postgresql_using="gin"
    )
    op.create_index("ix_reference_name_vector", "reference", ["name_vector"], unique=False, postgresql_using="gin")
    op.create_index("ix_reference_title_vector", "reference", ["title_vector"], unique=False, postgresql_using="gin")
    op.add_column(
        "referencetemplate",
        sa.Column(
            "name_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"name\")", persisted=True),
            nullable=False,
        ),
    )
    op.add_column(
        "referencetemplate",
        sa.Column(
            "title_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
            nullable=True,
        ),
    )
    op.add_column(
        "referencetemplate",
        sa.Column(
            "description_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_referencetemplate_name_vector", "referencetemplate", ["name_vector"], unique=False, postgresql_using="gin"
    )
    op.create_index(
        "ix_referencetemplate_title_vector", "referencetemplate", ["title_vector"], unique=False, postgresql_using="gin"
    )
    op.create_index(
        "ix_referencetemplatek_description_vector",
        "referencetemplate",
        ["description_vector"],
        unique=False,
        postgresql_using="gin",
    )
    op.add_column(
        "resource",
        sa.Column(
            "name_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"name\")", persisted=True),
            nullable=False,
        ),
    )
    op.add_column(
        "resource",
        sa.Column(
            "title_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
            nullable=True,
        ),
    )
    op.add_column(
        "resource",
        sa.Column(
            "description_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_resource_description_vector", "resource", ["description_vector"], unique=False, postgresql_using="gin"
    )
    op.create_index("ix_resource_name_vector", "resource", ["name_vector"], unique=False, postgresql_using="gin")
    op.create_index("ix_resource_title_vector", "resource", ["title_vector"], unique=False, postgresql_using="gin")
    op.add_column(
        "task",
        sa.Column(
            "name_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"name\")", persisted=True),
            nullable=False,
        ),
    )
    op.add_column(
        "task",
        sa.Column(
            "title_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
            nullable=True,
        ),
    )
    op.add_column(
        "task",
        sa.Column(
            "description_vector",
            TSVectorType(),
            sa.Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
            nullable=True,
        ),
    )
    op.create_index("ix_task_description_vector", "task", ["description_vector"], unique=False, postgresql_using="gin")
    op.create_index("ix_task_name_vector", "task", ["name_vector"], unique=False, postgresql_using="gin")
    op.create_index("ix_task_title_vector", "task", ["title_vector"], unique=False, postgresql_using="gin")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_task_title_vector", table_name="task", postgresql_using="gin")
    op.drop_index("ix_task_name_vector", table_name="task", postgresql_using="gin")
    op.drop_index("ix_task_description_vector", table_name="task", postgresql_using="gin")
    op.drop_column("task", "description_vector")
    op.drop_column("task", "title_vector")
    op.drop_column("task", "name_vector")
    op.drop_index("ix_resource_title_vector", table_name="resource", postgresql_using="gin")
    op.drop_index("ix_resource_name_vector", table_name="resource", postgresql_using="gin")
    op.drop_index("ix_resource_description_vector", table_name="resource", postgresql_using="gin")
    op.drop_column("resource", "description_vector")
    op.drop_column("resource", "title_vector")
    op.drop_column("resource", "name_vector")
    op.drop_index("ix_referencetemplatek_description_vector", table_name="referencetemplate", postgresql_using="gin")
    op.drop_index("ix_referencetemplate_title_vector", table_name="referencetemplate", postgresql_using="gin")
    op.drop_index("ix_referencetemplate_name_vector", table_name="referencetemplate", postgresql_using="gin")
    op.drop_column("referencetemplate", "description_vector")
    op.drop_column("referencetemplate", "title_vector")
    op.drop_column("referencetemplate", "name_vector")
    op.drop_index("ix_reference_title_vector", table_name="reference", postgresql_using="gin")
    op.drop_index("ix_reference_name_vector", table_name="reference", postgresql_using="gin")
    op.drop_index("ix_reference_description_vector", table_name="reference", postgresql_using="gin")
    op.drop_column("reference", "description_vector")
    op.drop_column("reference", "title_vector")
    op.drop_column("reference", "name_vector")
    op.drop_index("ix_project_title_vector", table_name="project", postgresql_using="gin")
    op.drop_index("ix_project_name_vector", table_name="project", postgresql_using="gin")
    op.drop_index("ix_project_description_vector", table_name="project", postgresql_using="gin")
    op.drop_column("project", "description_vector")
    op.drop_column("project", "title_vector")
    op.drop_column("project", "name_vector")
    op.drop_index(op.f("ix_ogunuser_id"), table_name="ogunuser")
    op.drop_index(op.f("ix_ogunuser_access_key"), table_name="ogunuser")
    op.drop_table("ogunuser")
    # ### end Alembic commands ###
