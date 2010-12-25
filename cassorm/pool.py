from django.conf import settings
import pycassa

CASSANDRA_POOL = pycassa.connect(settings.CASSANDRA_KEYSPACE, settings.CASSANDRA_SERVERS)

