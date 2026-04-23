"""initial_migration

Revision ID: 001
Revises: 
Create Date: 2026-04-24
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, server_default='user'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

    op.create_table(
        'recipes',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('ingredients', sa.JSON, nullable=False),
        sa.Column('steps', sa.JSON, nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='draft'),
        sa.Column('source', sa.String(50), nullable=False, server_default='ai'),
        sa.Column('rating', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        'cooking_sessions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('recipe_id', sa.String(36), nullable=False),
        sa.Column('completed_steps', sa.JSON, default=list),
        sa.Column('start_time', sa.DateTime, nullable=True),
        sa.Column('estimated_minutes', sa.Integer, nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('cooking_sessions')
    op.drop_table('recipes')
    op.drop_table('users')
