from cassandra.cqlengine import connection
from dao.config import CASSANDRA_HOSTS
from dao.models import Users, Data

ORG = "org"
TABLE = "table"
BODY = "body"
USERS = "users"


# TODO: Enable quorum
def insert(request):
    # TODO: Data Validation should be done?
    content = request.get_json()
    connection.setup(CASSANDRA_HOSTS, content[ORG])
    # if isinstance(body, Model):
    # TODO: Avoid using eval() because
    # TODO: this requires me to import all models
    obj = eval(content[TABLE]).create(**(content[BODY]))
    return obj

