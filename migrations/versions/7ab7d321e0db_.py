"""empty message

Revision ID: 7ab7d321e0db
Revises: 
Create Date: 2023-09-18 21:40:46.331875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ab7d321e0db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carrinho',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('is_open', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('carrinho_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('carrinho_id', sa.Integer(), nullable=True),
    sa.Column('produto_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['carrinho_id'], ['carrinho.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('carrinho_item')
    op.drop_table('carrinho')
    # ### end Alembic commands ###
