import time
from django.conf import settings
import pycassa
from pycassa.util import convert_time_to_uuid
from pycassa.system_manager import SystemManager
from .exceptions import CassandraIndexError
from .types import DateTime, DateTimeString, Float64, FloatString, Int64, IntString, String
from pycassa import BYTES_TYPE, LONG_TYPE, INT_TYPE, ASCII_TYPE, UTF8_TYPE, TIME_UUID_TYPE, LEXICAL_UUID_TYPE


MANAGER_MAPS = {}


class CassandraMetaModel(type):
    
    @property
    def objects(cls):
        if cls.__name__ not in MANAGER_MAPS:
            MANAGER_MAPS[id(cls)] = CassandraModelManager(cls)
        return MANAGER_MAPS[id(cls)]

    def sync(cls, default_validation_class=None, destructive=False):
        if default_validation_class is None:
            default_validation_class = cls.default_validation_class
        columns = []
        indexes = []
        column_family = cls.__name__.lower()
        for i in cls.__dict__:
            attr = cls.__dict__[i]
            if isinstance(attr, DateTime) or \
                    isinstance(attr, DateTimeString) or isinstance(attr, Float64) or \
                    isinstance(attr, FloatString) or isinstance(attr, Int64) or \
                    isinstance(attr, IntString) or isinstance(attr, String):
                columns.append(i)
                if attr.index:
                    indexes.append(i)
        sys = SystemManager(settings.CASSANDRA_SERVERS[0])
        if destructive:
            try:
                sys.drop_column_family(settings.CASSANDRA_KEYSPACE, cls.__name__.lower())
            except:
                pass
        sys.create_column_family(
            settings.CASSANDRA_KEYSPACE, 
            cls.__name__.lower(), 
            comparator_type=UTF8_TYPE,
            default_validation_class=default_validation_class)
        for column in columns:
            attr = cls.__dict__[column]
            if isinstance(attr, DateTime):
                type = ASCII_TYPE
            elif isinstance(attr, DateTimeString):
                type = ASCII_TYPE
            elif isinstance(attr, Float64):
                type = BYTES_TYPE
            elif isinstance(attr, FloatString):
                type = ASCII_TYPE
            elif isinstance(attr, Int64):
                type = BYTES_TYPE
            elif isinstance(attr, IntString):
                type = ASCII_TYPE
            elif isinstance(attr, String):
                type = UTF8_TYPE
            if column in indexes:
                sys.create_index(
                    settings.CASSANDRA_KEYSPACE, 
                    column_family, 
                    column.lower(), 
                    type,
                    index_name="%s_index" % column)
            else:                
                sys.alter_column(
                    settings.CASSANDRA_KEYSPACE, 
                    column_family, 
                    column.lower(), 
                    type)
        sys.close()
 

class CassandraModel(object):
    
    default_validation_class = UTF8_TYPE
    
    __metaclass__ = CassandraMetaModel
 
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
    
    def save(self):
        if not hasattr(self, "key"):    
            self.key = str(convert_time_to_uuid(time.time()))
        self.__class__.objects.insert(self)


class CassandraModelManager(pycassa.ColumnFamilyMap):
    
    def __init__(self, cls, create=False):
        self.cls = cls
        try:
            super(CassandraModelManager, self).__init__(
                self.cls, 
                pycassa.ColumnFamily(
                    settings.CASSANDRA_POOL, 
                    self.cls.__name__.lower()))
        except:
            pass
        
    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        value.key = key
        self.insert(value)
    
