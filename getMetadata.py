from sqlalchemy import *
import json
from dicttoxml import dicttoxml


class Meta:
    def __init__(self, conn):
        self.engine = create_engine(conn)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def getTables(self):
        ''' function for getting all the tables in the schema
            this list all the available functions'''
        return self.metadata.tables.keys()

    def getMetaForTable(self, table):
        ''' this is for getting metadata for the given table
            if the table is not found this raises an Exception'''
        if table in self.metadata.tables.keys():
            # for getting the table metadata
            tableMeta = dict(
                [(table, dict(
                    [(i, self.filterColMeta(j))
                     for i, j in self.metadata.tables[table].columns.items()]
                ))])
            return tableMeta
        else:
            raise Exception('Table Not Found')

    def filterColMeta(self, data):
        ''' for converting column object to keys 
            and parsing the data and objects to JSON serializable
            format so that it can be dumped as JSON'''
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
        columMeta = dict([(i, j.__str__()) if i == 'type' else (i, j)
                          for i, j in data.__dict__.items() if i in allowedKeys])
        # convert the Foriegn key object to dict and string
        columMeta['foreign_keys'] = map(
            str, list(columMeta.pop('foreign_keys')))
        # set to list conversion
        columMeta['constraints'] = list(columMeta.pop('constraints'))
        return columMeta


m = Meta('sqlite:///satyam.db')
print m.getTables()
print json.dumps(m.getMetaForTable('user'), indent=4)
print json.dumps(m.getMetaForTable('user_prefs'), indent=4)
print dicttoxml(m.getMetaForTable('user'))
print dicttoxml(m.getMetaForTable('user_prefs'))
