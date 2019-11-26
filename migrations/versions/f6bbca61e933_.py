"""empty message

Revision ID: f6bbca61e933
Revises: 41f89478a23b
Create Date: 2019-11-25 19:30:20.215498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6bbca61e933'
down_revision = '41f89478a23b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('plantings', sa.Column('current_air_humidity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('plantings', 'current_air_humidity')
    # ### end Alembic commands ###