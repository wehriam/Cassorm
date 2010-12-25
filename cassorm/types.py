import pycassa

def _pycassa_type_init(self, *args, **kwargs):
    """Stores an index kwarg, then passes to standard pycassa Types"""
    if "index" in kwargs:
        self.index = kwargs["index"]
        del kwargs["index"]
    else:
        self.index = False
    super(self.__class__, self).__init__(*args, **kwargs)     

class DateTime(pycassa.DateTime):
    __init__ = _pycassa_type_init
    

class DateTimeString(pycassa.DateTimeString):
    __init__ = _pycassa_type_init
    

class Float64(pycassa.Float64):    
    __init__ = _pycassa_type_init
    

class FloatString(pycassa.FloatString):
    __init__ = _pycassa_type_init
    

class Int64(pycassa.Int64):
    __init__ = _pycassa_type_init


class IntString(pycassa.IntString):
    __init__ = _pycassa_type_init
    

class String(pycassa.String):    
    __init__ = _pycassa_type_init
    