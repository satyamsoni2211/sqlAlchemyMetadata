from sqlalchemy import *
import json


class Meta:
    def __init__(self, conn):
        self.engine = create_engine(conn)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def getTables(self):
        return self.metadata.tables.keys()

    def getMetaForTable(self, table):
        if table in self.metadata.tables.keys():
            tableMeta = dict(
                [(table, dict(
                    [(i, self.filterColMeta(j))
                     for i, j in self.metadata.tables[table].columns.items()]
                ))])
            return tableMeta
        else:
            raise 'Table Not Found'

    def filterColMeta(self, data):
        allowedKeys = ['comment',
                       'index',
                       'server_onupdate',
                       'key',
                       'is_literal',
                       'nullable',
                       'default',
                       'autoincrement',
                       'primary_key',
                       'system',
                       'name',
                       'onupdate',
                       'foreign_keys',
                       #    'server_default',
                       '_creation_order',
                       'doc',
                       'unique',
                       'constraints',
                       'type']
        return dict([(i, j.__str__()) if i == 'type' else (i, j) for i, j in data.__dict__.items() if i in allowedKeys])


m = Meta('sqlite:///satyam.db')
print m.getTables()
m.getMetaForTable('abc')

# t = m.metadata.tables['user']
