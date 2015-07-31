"""empty message

Revision ID: 4f3ae7612da6
Revises: 4543ac4050e3
Create Date: 2015-07-29 10:33:09.214231

"""

# revision identifiers, used by Alembic.
revision = '4f3ae7612da6'
down_revision = '4543ac4050e3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###
