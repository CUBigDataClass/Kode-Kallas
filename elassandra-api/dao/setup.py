from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.query import SimpleStatement

from dao.config import CASSANDRA_HOSTS
from .models import Repo
from .commit_model import Commit
from .user_model import Users


def get_session(keyspace=None):
    # TODO: Should enable ssl: for both inter cluster and app communication P1
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect(keyspace)
    return session


# TODO: Simple vs Prepared P2
def create_keyspace(orgname):
    session = get_session()
    # TODO: Replication strategy should be updated to 3
    query = SimpleStatement(
        "CREATE KEYSPACE %s WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'DC1': 1};" % (orgname,))
    session.execute(query)
    session.shutdown()
    create_tables(orgname)


def delete_keyspace(orgname):
    session = get_session()
    query = SimpleStatement(
        "DROP KEYSPACE %s;" % (orgname,))
    session.execute(query)
    session.shutdown()


# TODO: MAke sure sessions and connections are handled properly: probably read about that
def create_tables(orgname):
    connection.setup(CASSANDRA_HOSTS, orgname, protocol_version=3)
    # session = get_session(orgname)
    sync_table(Repo)
    sync_table(Commit)
    sync_table(Users)
    connection.unregister_connection('default')


# TODO: Delete below functions when everything is done
