"""Revision upgrade script v0.10.0

Date created: 2025-02-05 20:35:12.364048
"""
from fietsboek.updater.script import UpdateScript

update_id = 'v0.10.0'
previous = [
    'v0.9.0',
]
alembic_revision = '4566843039d6'


class Up(UpdateScript):
    def pre_alembic(self, config):
        pass

    def post_alembic(self, config):
        pass


class Down(UpdateScript):
    def pre_alembic(self, config):
        pass

    def post_alembic(self, config):
        pass
