"""empty message

Revision ID: bf8f2e143d68
Revises: 
Create Date: 2019-11-30 02:26:47.741510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf8f2e143d68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Unique_user', 'user_social_pages', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('Unique_user', 'user_social_pages', ['user_id'])
    # ### end Alembic commands ###
