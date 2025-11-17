"""Add cascade delete to notifications.user_id

Revision ID: 131b095ea3ff
Revises: a1ff5f8524cb
Create Date: 2025-11-17 15:02:47.467117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '131b095ea3ff'
down_revision: Union[str, Sequence[str], None] = 'a1ff5f8524cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the old FK constraint
    op.drop_constraint('notifications_user_id_fkey', 'notifications', type_='foreignkey')

    # Recreate it with ON DELETE CASCADE
    op.create_foreign_key(
        'notifications_user_id_fkey',  # constraint name
        'notifications',               # source table
        'users',                       # target table
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    # Revert back to no cascade
    op.drop_constraint('notifications_user_id_fkey', 'notifications', type_='foreignkey')
    op.create_foreign_key(
        'notifications_user_id_fkey',
        'notifications',
        'users',
        ['user_id'], ['id']
        # no ondelete
    )