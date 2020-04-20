import json

from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.query import SimpleStatement

from .config import CASSANDRA_HOSTS
from flask import jsonify


ORG = "org"
TABLE = "table"
BODY = "body"
START_ID = "start_id"
END_ID = "end_id"
USERS = "users"



# TODO: Enable quorum
def insert_repo(request):
    # TODO: Data Validation should be done?
    content = request.get_json()
    #connection.setup(CASSANDRA_HOSTS, content[ORG])
    # if isinstance(body, Model):
    # TODO: Avoid using eval() because
    # TODO: this requires me to import all models
    obj_list = content[BODY]
    for obj in obj_list:
        #obj["permissions"] = json.loads(perm(admin=obj["permissions"]["admin"], push=obj["permissions"]["push"], pull=obj["permissions"]["pull"]))
        #obj["permissions"] = jsonify(**obj["permissions"])
        cluster = Cluster()
        session = cluster.connect('org')
        ans = json.dumps(obj)
        query = SimpleStatement("INSERT INTO JSON \'" + ans + "\';")
        session.execute(query)
        session.shutdown()
        #Repo.create(obj)
    return obj

def insert_commit(request):
    # TODO: Data Validation should be done?
    content = request.get_json()
    #connection.setup(CASSANDRA_HOSTS, content[ORG])
    # if isinstance(body, Model):
    # TODO: Avoid using eval() because
    # TODO: this requires me to import all models
    obj_list = content[BODY]
    for obj in obj_list:
        #obj["permissions"] = json.loads(perm(admin=obj["permissions"]["admin"], push=obj["permissions"]["push"], pull=obj["permissions"]["pull"]))
        #obj["permissions"] = jsonify(**obj["permissions"])
        cluster = Cluster()
        session = cluster.connect(content[ORG])
        ans = json.dumps(obj)
        query = SimpleStatement("INSERT INTO " + content[TABLE] + " JSON \'" + ans + "\';")
        session.execute(query)
        session.shutdown()
        #Repo.create(obj)
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
