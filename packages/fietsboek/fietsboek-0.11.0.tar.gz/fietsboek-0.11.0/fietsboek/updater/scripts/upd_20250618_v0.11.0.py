"""Revision upgrade script v0.11.0

Date created: 2025-06-18 13:14:07.849714
"""
from fietsboek.updater.script import UpdateScript

update_id = 'v0.11.0'
previous = [
    'v0.10.0',
]
alembic_revision = '2ebe1bf66430'


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
