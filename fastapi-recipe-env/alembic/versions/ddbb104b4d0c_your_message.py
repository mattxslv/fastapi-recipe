"""Your message

Revision ID: ddbb104b4d0c
Revises: 
Create Date: 2025-02-12 13:50:49.752712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ddbb104b4d0c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Drop dependent tables first
    tables_to_drop = ['Ratings', 'Comments', 'Recipes', 'users']

    for table in tables_to_drop:
        if table in inspector.get_table_names():
            op.drop_table(table)


def downgrade() -> None:
    # Recreate tables
    op.create_table('users',
        sa.Column('id', sa.Integer, sa.Identity(start=1, increment=1), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False)
    )

    op.create_table('Recipes',
        sa.Column('id', sa.Integer, sa.Identity(start=1, increment=1), primary_key=True),
        sa.Column('name', sa.String, nullable=True),
        sa.Column('ingredients', sa.Text, nullable=True),
        sa.Column('steps', sa.Text, nullable=True),
        sa.Column('prep_time', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=True),
        sa.Column('rating', sa.Float, nullable=True)
    )

    op.create_table('Ratings',
        sa.Column('id', sa.Integer, sa.Identity(start=1, increment=1), primary_key=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('Recipes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rating', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=True),
        sa.Column('user_id', sa.Integer, nullable=True)
    )

    op.create_table('Comments',
        sa.Column('id', sa.Integer, sa.Identity(start=1, increment=1), primary_key=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('Recipes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('comment', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=True)
    )
