"""change user_id in topics

Revision ID: 28b2caee696e
Revises: 6463fe8ed261
Create Date: 2023-03-05 21:18:20.921383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28b2caee696e'
down_revision = '6463fe8ed261'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('topics_user_id_fkey', 'topics', type_='foreignkey')
    op.create_foreign_key(None, 'topics', 'users', ['user_id'], ['telegram_id'])
    op.drop_constraint('users_username_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_constraint(None, 'topics', type_='foreignkey')
    op.create_foreign_key('topics_user_id_fkey', 'topics', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###