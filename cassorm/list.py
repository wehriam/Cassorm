import time
import uuid
from django.conf import settings
import pycassa
from pycassa.util import convert_time_to_uuid, convert_uuid_to_time
from pycassa.system_manager import SystemManager
from .exceptions import CassandraIndexError

MANAGER_MAPS = {}

class CassandraIndexError(IndexError):
    pass

class CassandraListManager(pycassa.ColumnFamily):
    """Manager for CassandraList."""
    
    def __init__(self, cls):
        self.cls = cls    
        super(CassandraListManager, self).__init__(
            settings.CASSANDRA_POOL, 
            self.cls.__name__.lower())


class CassandraMetaList(type):
    """Metaclass for CassandraList, provides schema creation, 
       access to CassandraListManager"""
    
    @property
    def objects(cls):
        """CassandraListManager Singletons"""
        if cls.__name__ not in MANAGER_MAPS:
            MANAGER_MAPS[id(cls)] = CassandraListManager(cls)
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
            comparator_type=pycassa.TIME_UUID_TYPE,
            default_validation_class=default_validation_class)
        sys.close()
        

class CassandraList(object):
    
    default_validation_class = pycassa.UTF8_TYPE
    
    __metaclass__ = CassandraMetaList
    
    def __init__(self, row_key):
        self.row_key = row_key
        self.cf = self.__class__.objects

    def append(self, x):
        self.cf.insert(self.row_key, {time.time():x})

    def extend(self, seq):
        rows = {}
        start = uuid.UUID("{%s}" % convert_time_to_uuid(time.time()))
        i = 0
        for x in seq:
            rows[uuid.UUID(int=start.int + i)] = unicode(x)
            i += 10
        self.cf.insert(self.row_key, rows)
    
    def insert(self, i, x):
        try:
            seq = self.cf.get(self.row_key, column_count=i + 1)
        except pycassa.NotFoundException, e:
            self.append(x)
            return
        if i >= len(seq):
            self.append(x)
            return
        old_key = seq.keys().pop()
        old_key_time = convert_uuid_to_time(old_key)
        low, high = convert_time_to_uuid(old_key_time, randomize=True), \
            convert_time_to_uuid(old_key_time, randomize=True)
        if low > high:
            high, low = low, high
        while high > old_key:
            low, high = convert_time_to_uuid(old_key_time, randomize=True), \
                convert_time_to_uuid(old_key_time, randomize=True)
            if low > high:
                high, low = low, high
        old_value = self.cf.get(self.row_key, columns=[old_key]).values().pop()
        self.cf.insert(self.row_key, {high:old_value})
        self.cf.insert(self.row_key, {low:x})
        self.cf.remove(self.row_key, columns=[old_key])
        
    def pop(self):
        try:
            item = self.cf.get(self.row_key, column_count=1, column_reversed=True)
        except pycassa.NotFoundException, e:
            raise CassandraIndexError("pop from empty list")
        self.cf.remove(self.row_key, columns=item.keys())
        return item.values()[0]
    
    def remove(self, x):
        column_start = ""
        while 1:
            try:
                columns = self.cf.get(self.row_key, column_start=column_start, column_count=100)
            except pycassa.NotFoundException, e:
                return
            for key in columns:
                if columns[key] == x:
                    self.cf.remove(self.row_key, columns=[key])
            key = uuid.UUID("{%s}" % key)
            column_start = uuid.UUID(int=key.int + 1)
            
    def delete(self):
        self.cf.remove(self.row_key)
    
    def __len__(self):
        return self.cf.get_count(self.row_key)
    
    def __str__(self):
        try:
            return str([x[1] for x in self.cf.get(self.row_key).items()])
        except pycassa.NotFoundException, e:
            return str([]) 
        
    def __getitem__(self, val):
        if isinstance(val, slice):
            if (val.step is None or val.step > 0) and val.stop is not None:
                seq = [x[1] for x in self.cf.get(self.row_key, column_count=val.stop).items()]
                return seq[val.start:val.stop:val.step]
            seq = [x[1] for x in self.cf.get(self.row_key).items()]
            return seq[val.start:val.stop:val.step]
        elif isinstance(val, int):
            try:
                return self[val:val + 1].pop()
            except Exception, e:
                raise CassandraIndexError("List index out of range.")
        else:
            return super(CassandraList, self).__getitem__(val)
