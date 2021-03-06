"""empty message

Revision ID: c906f8ca6628
Revises: de08af91cf95
Create Date: 2017-11-16 15:18:00.274181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c906f8ca6628'
down_revision = 'de08af91cf95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pastes', sa.Column('code_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'pastes', 'codelanguages', ['code_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pastes', type_='foreignkey')
    op.drop_column('pastes', 'code_id')
    # ### end Alembic commands ###
