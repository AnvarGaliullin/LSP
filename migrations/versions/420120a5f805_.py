"""empty message

Revision ID: 420120a5f805
Revises: d22409a11ef7
Create Date: 2019-11-30 02:35:01.610160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '420120a5f805'
down_revision = 'd22409a11ef7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserInfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=100), nullable=True),
    sa.Column('home_region', sa.String(length=100), nullable=True),
    sa.Column('deltailed_description', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('UserSocialPages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('vk', sa.String(length=100), nullable=True),
    sa.Column('facebook', sa.String(length=100), nullable=True),
    sa.Column('linked_in', sa.String(length=100), nullable=True),
    sa.Column('instagram', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.drop_table('user_social_pages')
    op.drop_table('user_info')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_info',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('home_region', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('deltailed_description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_info_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_info_pkey'),
    sa.UniqueConstraint('user_id', name='user_info_user_id_key')
    )
    op.create_table('user_social_pages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('vk', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('facebook', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('instagram', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('linked_in', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_social_pages_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_social_pages_pkey'),
    sa.UniqueConstraint('user_id', name='user_social_pages_user_id_key')
    )
    op.drop_table('UserSocialPages')
    op.drop_table('UserInfo')
    # ### end Alembic commands ###
