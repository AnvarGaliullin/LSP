"""Add teacher to course

Revision ID: a1a48e7f393a
Revises: 
Create Date: 2019-11-29 17:21:36.495680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1a48e7f393a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Educational\u0421ourse', sa.Column('teacher_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'EducationalСourse', 'teachers', ['teacher_id'], ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'EducationalСourse', type_='foreignkey')
    op.drop_column('EducationalСourse', 'teacher_id')
    # ### end Alembic commands ###
