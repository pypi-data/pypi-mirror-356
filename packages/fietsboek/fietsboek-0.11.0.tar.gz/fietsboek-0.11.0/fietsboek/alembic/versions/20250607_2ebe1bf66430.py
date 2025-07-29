"""switch transfomers from JSON to TEXT

Revision ID: 2ebe1bf66430
Revises: 4566843039d6
Create Date: 2025-06-07 23:24:33.182649

"""
import logging

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2ebe1bf66430'
down_revision = '4566843039d6'
branch_labels = None
depends_on = None

is_sqlite = op.get_bind().dialect.name == "sqlite"

def upgrade():
    if is_sqlite:
        op.add_column('tracks', sa.Column('transformers_text', sa.Text, nullable=True))
        op.execute('UPDATE tracks SET transformers_text=transformers;')
        try:
            op.drop_column('tracks', 'transformers')
        except sa.exc.OperationalError as exc:
            logging.getLogger(__name__).warning(
                "Your SQLite version does not support dropping a column. "
                "We're setting the content to NULL instead: %s",
                exc,
            )
            op.execute("UPDATE tracks SET transformers = NULL;")
            op.alter_column("tracks", "transformers", new_column_name="transformers_old_delete_this_column")
        op.alter_column('tracks', 'transformers_text', new_column_name='transformers')
    else:
        op.alter_column('tracks', 'transformers', type_=sa.Text)

def downgrade():
    if is_sqlite:
        op.add_column('tracks', sa.Column('transfomers_json', sa.JSON, nullable=True))
        op.execute('UPDATE tracks SET transformers_json=transformers;')
        op.drop_column('tracks', 'transformers')
        op.alter_column('tracks', 'transformers_json', new_column_name='transformers')
    else:
        op.alter_column('tracks', 'transformers', type_=sa.JSON)
