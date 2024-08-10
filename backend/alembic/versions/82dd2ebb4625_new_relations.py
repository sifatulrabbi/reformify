"""new relations

Revision ID: 82dd2ebb4625
Revises: 
Create Date: 2024-08-10 14:28:08.305043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82dd2ebb4625'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile_sections',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='reformify'
    )
    op.create_index(op.f('ix_reformify_profile_sections_id'), 'profile_sections', ['id'], unique=True, schema='reformify')
    op.create_table('user_profiles',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('fullname', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='reformify'
    )
    op.create_index(op.f('ix_reformify_user_profiles_email'), 'user_profiles', ['email'], unique=True, schema='reformify')
    op.create_index(op.f('ix_reformify_user_profiles_id'), 'user_profiles', ['id'], unique=True, schema='reformify')
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='reformify'
    )
    op.create_index(op.f('ix_reformify_users_email'), 'users', ['email'], unique=True, schema='reformify')
    op.create_table('user_careers',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('start_date', sa.String(), nullable=False),
    sa.Column('end_date', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['reformify.user_profiles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='reformify'
    )
    op.create_index(op.f('ix_reformify_user_careers_id'), 'user_careers', ['id'], unique=True, schema='reformify')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reformify_user_careers_id'), table_name='user_careers', schema='reformify')
    op.drop_table('user_careers', schema='reformify')
    op.drop_index(op.f('ix_reformify_users_email'), table_name='users', schema='reformify')
    op.drop_table('users', schema='reformify')
    op.drop_index(op.f('ix_reformify_user_profiles_id'), table_name='user_profiles', schema='reformify')
    op.drop_index(op.f('ix_reformify_user_profiles_email'), table_name='user_profiles', schema='reformify')
    op.drop_table('user_profiles', schema='reformify')
    op.drop_index(op.f('ix_reformify_profile_sections_id'), table_name='profile_sections', schema='reformify')
    op.drop_table('profile_sections', schema='reformify')
    # ### end Alembic commands ###
