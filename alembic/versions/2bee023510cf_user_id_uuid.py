"""Switch user id to UUID

Revision ID: 2bee023510cf
Revises: 521035f7a38f
Create Date: 2025-07-02 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '2bee023510cf'
down_revision: Union[str, Sequence[str], None] = '521035f7a38f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'id', type_=sa.dialects.postgresql.UUID(), postgresql_using='id::uuid')
    op.alter_column('orders', 'user_id', type_=sa.dialects.postgresql.UUID(), postgresql_using='user_id::uuid')
    op.alter_column('products', 'user_id', type_=sa.dialects.postgresql.UUID(), postgresql_using='user_id::uuid')


def downgrade() -> None:
    op.alter_column('products', 'user_id', type_=sa.Integer(), postgresql_using='user_id::integer')
    op.alter_column('orders', 'user_id', type_=sa.Integer(), postgresql_using='user_id::integer')
    op.alter_column('users', 'id', type_=sa.Integer(), postgresql_using='id::integer')
