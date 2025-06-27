from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'services',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index(
        'product_search_idx',
        'products',
        [sa.text("to_tsvector('french', name || ' ' || coalesce(description,''))")],
        postgresql_using='gin'
    )
    op.create_index(
        'service_search_idx',
        'services',
        [sa.text("to_tsvector('french', name || ' ' || coalesce(description,''))")],
        postgresql_using='gin'
    )


def downgrade():
    op.drop_index('service_search_idx', table_name='services')
    op.drop_index('product_search_idx', table_name='products')
    op.drop_table('services')

