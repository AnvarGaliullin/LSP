"""add constraint to unique course+responsible person

Revision ID: 9a69c04ab912
Revises: 807622c61947
Create Date: 2019-12-09 23:44:35.273404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a69c04ab912'
down_revision = '807622c61947'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_course_person_uniq_const', 'Course_Responsible_Person', ['course_id', 'person_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_course_person_uniq_const', 'Course_Responsible_Person', type_='unique')
    # ### end Alembic commands ###