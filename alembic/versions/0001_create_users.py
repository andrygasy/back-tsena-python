from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False, server_default='user'),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_login', sa.DateTime(timezone=True)),
        sa.Column('order_count', sa.Integer(), server_default='0'),
        sa.Column('total_spent', sa.Float(), server_default='0'),
        sa.Column('phone', sa.String()),
        sa.Column('avatar', sa.String()),
        sa.Column('is_professional', sa.Boolean(), server_default='false'),
        sa.Column('professional_type', sa.String()),
    )


def downgrade():
    op.drop_table('users')
