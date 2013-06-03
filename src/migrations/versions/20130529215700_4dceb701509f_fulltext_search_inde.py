
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

"""Fulltext search indexes

Revision ID: 4dceb701509f
Revises: 459696baf6e4
Create Date: 2013-05-29 21:57:00.453459

"""

# revision identifiers, used by Alembic.
revision = '4dceb701509f'
down_revision = '459696baf6e4'

from alembic import op, context
import sqlalchemy as sa

def _get_db_scheme():
    url = str(context.get_context().connection.engine.url)
    db_scheme = url.split(':')[0].split('+')[0]
    return db_scheme

def upgrade():
    db_scheme = _get_db_scheme()
    if db_scheme == 'mysql':
        op.create_table('fulltext_record_properties',
        sa.Column('key', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=64), nullable=False),
        sa.Column('tags', sa.String(length=250), nullable=True),
        sa.Column('property', sa.String(length=64), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('key', 'type', 'property'),
        mysql_engine='myisam'
        )

        # Manually trigger fulltext index creation
        ddl = 'ALTER TABLE {tablename} ADD FULLTEXT INDEX {tablename}_text_idx (content)'
        op.execute(ddl.format(tablename='fulltext_record_properties'))
    elif db_scheme == 'sqlite':
        ddl = 'CREATE VIRTUAL TABLE {tablename} USING fts4(key, type, tags, property, content)'
        op.execute(ddl.format(tablename='fulltext_record_properties'))
    else:
        print("Unsupported db scheme {db_scheme} -- should be one of mysql, sqlite".format(
            db_scheme=db_scheme))

def downgrade():
    db_scheme = _get_db_scheme()
    if db_scheme == 'mysql' or db_scheme == 'sqlite':
        op.drop_table('fulltext_record_properties')
    else:
        print("Unsupported db scheme {db_scheme} -- should be one of mysql, sqlite".format(
            db_scheme=db_scheme))