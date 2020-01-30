"""create facility table

Revision ID: cfb292a49649
Revises: 326a435c7d48
Create Date: 2020-01-31 09:54:21.363455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfb292a49649'
down_revision = '326a435c7d48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('facilities',
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('location', sa.String(length=250), nullable=False),
    sa.Column('certifications', sa.String(length=250), nullable=False),
    sa.Column('phoneNo', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('status', sa.Enum('active', 'inactive', 'blocked', 'archived', 'deleted', name='statustype'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('facilities')
    # ### end Alembic commands ###
