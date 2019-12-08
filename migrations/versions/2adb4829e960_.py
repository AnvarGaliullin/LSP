"""empty message

Revision ID: 2adb4829e960
Revises: 420120a5f805
Create Date: 2019-11-30 02:38:43.642666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2adb4829e960'
down_revision = '420120a5f805'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User_Info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=100), nullable=True),
    sa.Column('home_region', sa.String(length=100), nullable=True),
    sa.Column('deltailed_description', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.drop_table('UserInfo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserInfo',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"UserInfo_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('home_region', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('deltailed_description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='UserInfo_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='UserInfo_pkey'),
    sa.UniqueConstraint('user_id', name='UserInfo_user_id_key')
    )
    op.drop_table('User_Info')
    # ### end Alembic commands ###
