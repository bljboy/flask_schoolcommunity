"""empty message

Revision ID: ffd148f1c948
Revises: cc6993997e57
Create Date: 2023-04-09 10:52:28.296201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffd148f1c948'
down_revision = 'cc6993997e57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('forum', schema=None) as batch_op:
        batch_op.add_column(sa.Column('join_time', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('forum', schema=None) as batch_op:
        batch_op.drop_column('join_time')

    # ### end Alembic commands ###
