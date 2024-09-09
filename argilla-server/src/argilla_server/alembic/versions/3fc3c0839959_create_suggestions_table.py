#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""create suggestions table

Revision ID: 3fc3c0839959
Revises: 8c574ada5e5f
Create Date: 2023-06-27 17:34:49.734260

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3fc3c0839959"
down_revision = "8c574ada5e5f"
branch_labels = None
depends_on = None

suggestion_type_enum = sa.Enum("model", "human", "selection", name="suggestion_type_enum")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "suggestions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("agent", sa.String(), nullable=True),
        sa.Column("type", sa.Enum(name="suggestion_type_enum"), nullable=True),
        sa.Column("record_id", sa.Uuid(), nullable=False),
        sa.Column("question_id", sa.Uuid(), nullable=False),
        sa.Column("inserted_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["record_id"], ["records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("record_id", "question_id", name="suggestion_record_id_question_id_uq"),
    )
    op.create_index(op.f("ix_suggestions_question_id"), "suggestions", ["question_id"], unique=False)
    op.create_index(op.f("ix_suggestions_record_id"), "suggestions", ["record_id"], unique=False)
    op.create_index(op.f("ix_suggestions_type"), "suggestions", ["type"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    bind = op.get_bind()

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_suggestions_type"), table_name="suggestions")
    op.drop_index(op.f("ix_suggestions_record_id"), table_name="suggestions")
    op.drop_index(op.f("ix_suggestions_question_id"), table_name="suggestions")
    op.drop_table("suggestions")
    # ### end Alembic commands ###

    # For this see here: https://github.com/sqlalchemy/alembic/issues/886
    if bind.dialect.name == "postgresql":
        suggestion_type_enum.drop(bind)