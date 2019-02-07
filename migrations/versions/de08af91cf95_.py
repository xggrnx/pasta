"""empty message

Revision ID: de08af91cf95
Revises: 
Create Date: 2017-11-16 13:09:02.472094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de08af91cf95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pastes', 'link',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pastes', 'link',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###