"""empty message

Revision ID: 087c75694d0f
Revises: 
Create Date: 2023-09-18 21:13:39.813539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '087c75694d0f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activeroom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room', sa.String(length=16), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('active_users', sa.Integer(), nullable=True),
    sa.Column('new_messages', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('room')
    )
    with op.batch_alter_table('activeroom', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_activeroom_timestamp'), ['timestamp'], unique=False)

    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room', sa.String(length=16), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_message_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_timestamp'), ['timestamp'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('user_role', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('ls', sa.String(length=12), nullable=True),
    sa.Column('room', sa.String(length=16), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('last_message_read_time', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_last_message_read_time'), ['last_message_read_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_last_seen'), ['last_seen'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_ls'), ['ls'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_token'), ['token'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_token'))
        batch_op.drop_index(batch_op.f('ix_user_ls'))
        batch_op.drop_index(batch_op.f('ix_user_last_seen'))
        batch_op.drop_index(batch_op.f('ix_user_last_message_read_time'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_message_timestamp'))
        batch_op.drop_index(batch_op.f('ix_message_name'))

    op.drop_table('message')
    with op.batch_alter_table('activeroom', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_activeroom_timestamp'))

    op.drop_table('activeroom')
    # ### end Alembic commands ###
