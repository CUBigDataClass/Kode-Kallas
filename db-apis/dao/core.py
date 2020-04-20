from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.query import SimpleStatement

from dao.config import CASSANDRA_HOSTS
from dao.models import Users, Data, Repos
from flask import jsonify
from dao.test import create, users2, users3

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
    # if content[TABLE] == "Repos":
    # insert_repos(content)
    # return
    connection.setup(CASSANDRA_HOSTS, content[ORG])
    # if isinstance(body, Model):
    # TODO: Avoid using eval() because
    # TODO: this requires me to import all models
    obj_list = content[BODY]

    for obj in obj_list:
        for committer in obj['commits']:
            for key in committer.keys():
                if not isinstance(committer[key], str):
                    committer[key] = str(committer[key])

        for contributor in obj['contributors']:
            for key in contributor.keys():
                if not isinstance(contributor[key], str):
                    contributor[key] = str(contributor[key])

    for obj in obj_list:
        # Repos.create(**(obj))
        eval(content[TABLE]).create(**(obj))
    return True


def insert_repos(request):
    content = request.get_json()
    # obj_list = content[BODY]
    # cluster = Cluster()
    # session = cluster.connect('org1')
    x = '{"name":"Hehe16666", "addr": [{ "contributions": 1, "html_url": "https://github.com/dmalan", "contrib_id": "788678", "name": "dmalan"}]}'
    # for obj in obj_list:
    # haha = jsonify(obj)
    # lol = str(haha)
    # query = SimpleStatement("INSERT INTO users2 JSON \'" + str(jsonify(obj)) + "\';")
    # Users.create(**(obj))
    # query = SimpleStatement("INSERT INTO users2 JSON \'" + str(x) + "\';")
    # session.execute(query)
    string = jsonify(request.get_json())
    # query = SimpleStatement("INSERT INTO users2 JSON \'" + str(request.get_json()) + "\';")
    # query = SimpleStatement("INSERT INTO users2 JSON \'" + str(x) + "\';")
    # session.execute(query)
    # create(session)

    connection.setup(CASSANDRA_HOSTS, 'org1')
    users3.create(**(content[BODY]))

def filter(response_object, content):
    for obj in response_object:
        for keys in list(obj):
            if keys not in content["key"]:
                del obj[keys]


def get_data(request):
    content = request.get_json()
    connection.setup(CASSANDRA_HOSTS, content[ORG])
    obj = eval(content[TABLE]).objects.filter(**(content[BODY])).allow_filtering()
    obj_list = []
    for o in obj:
        obj_list.append(dict(o))

    if "key" in content:
        filter(obj_list, content)
    return jsonify(obj_list)


def get_all_data(request):
    content = request.get_json()
    connection.setup(CASSANDRA_HOSTS, content[ORG])
    obj = eval(content[TABLE]).objects.all()
    obj_list = []
    response_obj = None
    for o in obj:
        obj_list.append(dict(o))
    if START_ID in content:
        response_obj = obj_list[int(content[START_ID]):int(content[END_ID])]
    else:
        response_obj = obj_list

    if "key" in content:
        filter(response_obj, content)

    return jsonify(response_obj)
