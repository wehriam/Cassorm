from django.conf import settings
import pycassa
from pycassa.system_manager import SystemManager


MANAGER_MAPS = {}


class CassandraKeyError(KeyError):
    pass


class CassandraDictManager(pycassa.ColumnFamily):
    """Manager for CassandraDict, provides schema creation."""

    def __init__(self, cls):
        self.cls = cls    
        super(CassandraDictManager, self).__init__(
            settings.CASSANDRA_POOL, 
            self.cls.__name__.lower())


class CassandraMetaDict(type):
    """Metaclass for CassandraDict, provides access to CassandraDictManager"""

    @property
    def objects(cls):
        """CassandraListManager Singletons"""
        if cls.__name__ not in MANAGER_MAPS:
            MANAGER_MAPS[id(cls)] = CassandraDictManager(cls)
        return MANAGER_MAPS[id(cls)]

    def sync(cls, default_validation_class=None, destructive=False):
        """Create the Cassandra List schema."""
        if default_validation_class is None:
            default_validation_class = cls.default_validation_class
        sys = SystemManager(settings.CASSANDRA_SERVERS[0])
        if destructive:
            try:
                sys.drop_column_family(settings.CASSANDRA_KEYSPACE, cls.__name__.lower())
            except:
                pass
        sys.create_column_family(
            settings.CASSANDRA_KEYSPACE, 
            cls.__name__.lower(), 
            comparator_type=pycassa.UTF8_TYPE,
            default_validation_class=default_validation_class)
        sys.close()


class CassandraDict(object):
    "A dictionary that stores its data persistantly in Cassandra"

    default_validation_class = pycassa.UTF8_TYPE
    
    __metaclass__ = CassandraMetaDict
    
    def __init__(self, row_key):
        self.row_key = row_key
        self.cf = self.__class__.objects

    def get(self, key, default=None):
        try:
            return self.cf.get(self.row_key, columns=[key]).values()[0]
        except pycassa.NotFoundException, e:
            if default is None:
                raise CassandraKeyError(key)
            else:
                return default
                
    def __getitem__(self, key):
        try:
            return self.cf.get(self.row_key, columns=[key]).values()[0]
        except pycassa.NotFoundException, e:
            raise CassandraKeyError(key)
            
    def __setitem__(self, key, value):
        self.cf.insert(self.row_key, {key:value})

    def __delitem__(self, key):
        self.cf.remove(self.row_key, columns=[key])

    def update(self, d):
        return self.cf.insert(self.row_key, d)

    def remove(self, seq):
        if isinstance(seq, list):
            self.cf.remove(self.row_key, columns=seq)
        elif isinstance(seq, dict):
            self.cf.remove(self.row_key, columns=seq.keys())
            
    def keys(self):
        try:
            return self.cf.get(self.row_key).keys()
        except pycassa.NotFoundException, e:
            return []
        
    def values(self):
        try:
            return self.cf.get(self.row_key).values()
        except pycassa.NotFoundException, e:
            return []
        
    def items(self):
        try:
            return self.cf.get(self.row_key)
        except pycassa.NotFoundException, e:
            return []
    
    def iterkeys(self):
        return self.keys()
        
    def itervalues(self):
        return self.values()
        
    def iteritems(self):
        return self.items()

    def has_key(self, key):
        return key in dict(self.items())

    def __contains__(self, key):
        return self.has_key(key)

    def __len__(self):
        return self.cf.get_count(self.row_key)
    
    def __dict__(self):
        return dict(self.items())
        
        