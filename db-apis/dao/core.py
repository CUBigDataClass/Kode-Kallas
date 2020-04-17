from cassandra.cqlengine import connection
from dao.config import CASSANDRA_HOSTS
from dao.models import Users, Data
from flask import jsonify


ORG = "org"
TABLE = "table"
BODY = "body"
START_ID = "start_id"
END_ID = "end_id"
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


def get_data(request):
    content = request.get_json()
    connection.setup(CASSANDRA_HOSTS, content[ORG])
    obj = eval(content[TABLE]).objects.filter(**(content[BODY])).allow_filtering()
    obj_list = []
    for o in obj:
        obj_list.append(dict(o))
    return jsonify(obj_list)


def get_all_data(request):
    content = request.get_json()
    connection.setup(CASSANDRA_HOSTS, content[ORG])
    obj = eval(content[TABLE]).objects.all()
    obj_list = []
    for o in obj:
        obj_list.append(dict(o))
    if content[START_ID]:
        return jsonify(obj_list[int(content[START_ID]):int(content[END_ID])])
    return jsonify(obj_list)
