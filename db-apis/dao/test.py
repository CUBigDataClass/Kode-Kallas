import json

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.columns import *
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType
from cassandra.query import SimpleStatement

from dao.config import CASSANDRA_HOSTS


class address(UserType):
    street = Text()
    zipcode = Integer()

class Contrib(UserType):
    name = Text()
    contrib_id = Text()
    contributions = Integer()
    html_url = Text()

class users2(Model):
    name = Text(primary_key=True)
    addr = List(value_type=UserDefinedType(Contrib))

class users3(Model):
    name = Text(primary_key=True)
    addr = List(value_type=Map(key_type=Text(), value_type=Text()))


def create(session):
    x = '{"name":"Hehe17", "addr": [{ "contributions": 1, "html_url": "https://github.com/dmalan", "contrib_id": "788678", "name": "dmalan"}]}'

    # rows = session.execute('INSERT INTO users2 JSON\'{"name":"Haha", "addr": [{"street":"Easy St.", "zipcode":"99999"},
    # {"street":"Difficult St.", "zipcode":"99999"}]}\'')
    query = SimpleStatement("INSERT INTO users2 JSON \'" + str(x) + "\';")
    session.execute(query)
    session.shutdown()

connection.setup(CASSANDRA_HOSTS, "org1", protocol_version=3)
#sync_table(users2)
sync_table(users3)
connection.unregister_connection('default')

cluster = Cluster()
session = cluster.connect('org1')
x='{"name":"Hehe7", "addr": [{ "contributions": 1, "html_url": "https://github.com/dmalan", "contrib_id": "788678", "name": "dmalan"}]}'

#rows = session.execute('INSERT INTO users2 JSON\'{"name":"Haha", "addr": [{"street":"Easy St.", "zipcode":"99999"},
# {"street":"Difficult St.", "zipcode":"99999"}]}\'')
query = SimpleStatement(
        "INSERT INTO users2 JSON \'"+str(x)+"\';")
session.execute(query)
session.shutdown()
#rows = session.execute('INSERT INTO users2 JSON %s;'% (x,))

