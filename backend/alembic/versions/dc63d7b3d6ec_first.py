"""first

Revision ID: dc63d7b3d6ec
Revises: 
Create Date: 2024-08-08 19:42:02.200548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dc63d7b3d6ec'
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
    op.drop_index('ix_conversations_bot_user_id', table_name='conversations')
    op.drop_index('ix_conversations_id', table_name='conversations')
    op.drop_table('conversations')
    op.drop_table('widget_conversations')
    op.drop_table('conversation_sessions')
    op.drop_index('ix_widget_users_id', table_name='widget_users')
    op.drop_table('widget_users')
    op.drop_index('ix_bot_users_id', table_name='bot_users')
    op.drop_index('ix_bot_users_whatsapp_number', table_name='bot_users')
    op.drop_table('bot_users')
    op.drop_index('ix_dashboard_users_id', table_name='dashboard_users')
    op.drop_table('dashboard_users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dashboard_users',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('role', postgresql.ENUM('SUPER_ADMIN', 'MANAGER', 'AGENT', name='dashboardtype'), autoincrement=False, nullable=True),
    sa.Column('prompt_description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('bot_phone_number', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('fcm_token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='dashboard_users_pkey'),
    sa.UniqueConstraint('email', name='dashboard_users_email_key'),
    sa.UniqueConstraint('fcm_token', name='dashboard_users_fcm_token_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_dashboard_users_id', 'dashboard_users', ['id'], unique=False)
    op.create_table('bot_users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('whatsapp_number', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='bot_users_pkey')
    )
    op.create_index('ix_bot_users_whatsapp_number', 'bot_users', ['whatsapp_number'], unique=True)
    op.create_index('ix_bot_users_id', 'bot_users', ['id'], unique=False)
    op.create_table('widget_users',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('external_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('fcm_token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='widget_users_pkey'),
    sa.UniqueConstraint('email', name='widget_users_email_key'),
    sa.UniqueConstraint('fcm_token', name='widget_users_fcm_token_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_widget_users_id', 'widget_users', ['id'], unique=False)
    op.create_table('conversation_sessions',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('session_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('agent_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('session_type', postgresql.ENUM('human', 'bot', name='session_type'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['dashboard_users.id'], name='conversation_sessions_agent_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['widget_users.id'], name='conversation_sessions_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='conversation_sessions_pkey'),
    sa.UniqueConstraint('session_id', name='conversation_sessions_session_id_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('widget_conversations',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('sender', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('read', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('message_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('conversation_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversation_sessions.id'], name='widget_conversations_conversation_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='widget_conversations_pkey')
    )
    op.create_table('conversations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('bot_user_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sender', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('response', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('message_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('read', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='conversations_pkey')
    )
    op.create_index('ix_conversations_id', 'conversations', ['id'], unique=False)
    op.create_index('ix_conversations_bot_user_id', 'conversations', ['bot_user_id'], unique=False)
    op.drop_index(op.f('ix_reformify_users_email'), table_name='users', schema='reformify')
    op.drop_table('users', schema='reformify')
    op.drop_index(op.f('ix_reformify_profile_sections_id'), table_name='profile_sections', schema='reformify')
    op.drop_table('profile_sections', schema='reformify')
    # ### end Alembic commands ###
