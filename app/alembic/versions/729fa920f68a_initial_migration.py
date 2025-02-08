"""initial migration

Revision ID: 729fa920f68a
Revises: 
Create Date: 2025-01-19 15:48:04.452782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision: str = '729fa920f68a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # user table
    op.create_table('user',
    sa.Column('user_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_disabled', sa.Boolean(), server_default='False', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('contact_num', sa.String(), nullable=True)
    )
    op.create_index(op.f('ix_user_user_id'), 'user', ['user_id'], unique=False)


    # category table
    op.create_table('category',
    sa.Column('category_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.create_index(op.f('ix_category_category_id'), 'category', ['category_id'], unique=False)

    # transaction table
    op.create_table('transaction',
    sa.Column('transaction_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    sa.Column('user_id', UUID(as_uuid=True), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('category_id', UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='False', nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.category_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], )
    )
    op.create_index(op.f('ix_transaction_transaction_id'), 'transaction', ['transaction_id'], unique=False)

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_transaction_id'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_index(op.f('ix_category_category_id'), table_name='category')
    op.drop_table('category')
    op.drop_index(op.f('ix_user_user_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
