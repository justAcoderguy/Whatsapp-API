"""empty message

Revision ID: 93eb56e35aeb
Revises: 
Create Date: 2022-07-27 14:41:28.645706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93eb56e35aeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.BigInteger(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('timestamp', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###
