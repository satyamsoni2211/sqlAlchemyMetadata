from sqlalchemy import *
import json
from dicttoxml import dicttoxml


class Meta:
    '''
        class to get metadata from any database
        pass the connection string while creating object for the wrapper
        say for sqlite i.e. sqlite:///satyam.db    
        exposed methods:
            getTables
            getMetaForTable
    '''

    def __init__(self, conn):
        self.__engine = create_engine(conn)
        self.__metadata = MetaData()
        self.__metadata.reflect(bind=self.__engine)

    def getTables(self):
        ''' function for getting all the tables in the schema
            this list all the available functions'''
        return self.__metadata.tables.keys()

    def getMetaForTable(self, table):
        ''' this is for getting metadata for the given table
            if the table is not found this raises an Exception'''
        if table in self.__metadata.tables.keys():
            # for getting the table metadata
            tableMeta = dict(
                [(table, dict(
                    [(i, self.__filterColMeta(j))
                     for i, j in self.__metadata.tables[table].columns.items()]
                ))])
            return tableMeta
        else:
            raise Exception('Table Not Found')

    def __parseCols(self, columMeta):
        '''
            formatting columns with class objects
        '''
        # converting type to str representation
        columMeta['type'] = columMeta.pop('type').__str__()
        # convert the Foriegn key object to dict and string
        columMeta['foreign_keys'] = map(
            str, list(columMeta.pop('foreign_keys')))
        # set to list conversion
        columMeta['constraints'] = list(columMeta.pop('constraints'))
        return columMeta

    def __filterColMeta(self, data):
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
                       '_creation_order',
                       'doc',
                       'unique',
                       'constraints',
                       'type']
        columMeta = self.__parseCols(dict([(i, j)
                                           for i, j in data.__dict__.items() if i in allowedKeys]))

        return columMeta


m = Meta('sqlite:///satyam.db')
print m.getTables()
print json.dumps(m.getMetaForTable('user'), indent=4)
print json.dumps(m.getMetaForTable('user_prefs'), indent=4)
print dicttoxml(m.getMetaForTable('user'))
print dicttoxml(m.getMetaForTable('user_prefs'))
