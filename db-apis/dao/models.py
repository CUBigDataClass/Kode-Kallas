import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class URL():

    def __init__(self, url):
        self.url = url

class Users(Model):
    uid = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(primary_key=True, required=True)
    repos = columns.List(value_type=columns.Text, required=False)


class Data(Model):
    gitid = columns.Text(required=True)
    name = columns.Text(primary_key=True,required=True)
    repo = columns.Text(primary_key=True,required=True)
    commit_num = columns.Integer(required=False, default=0)


class Repos(Model):
    uid = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(primary_key=True, required=True)
    users = columns.List(value_type=columns.Text, required=False)
