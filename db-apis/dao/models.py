import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.columns import UserDefinedType
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType


class Users(Model):
    uid = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(primary_key=True, required=True)
    id = columns.Text(primary_key=True, required=True)
    repos = columns.List(value_type=columns.Text, required=False)


class Data(Model):
    gitid = columns.Text(required=True)
    name = columns.Text(primary_key=True, required=True)
    repo = columns.Text(primary_key=True, required=True)
    commit_num = columns.Integer(required=False, default=0)

class Commit(UserType):
    committer_id = columns.Integer()
    committer_name = columns.Text()
    date = columns.DateTime()
    message = columns.Text()
    additions = columns.Integer()
    deletions = columns.Integer()
    total = columns.Integer()


class Contrib(UserType):
    name = columns.Text()
    id = columns.Text()
    contributions = columns.Integer()
    html_url = columns.Text()



class Repos(Model):
    uid = columns.UUID(primary_key=True, default=uuid.uuid4)
    id = columns.Text(primary_key=True, required=True)
    full_name = columns.Text(primary_key=True, required=True)
    name = columns.Text(required=False)
    html_url = columns.Text(required=False)
    languages = columns.Map(key_type=columns.Text, value_type=columns.Integer)
    #commits = columns.List(value_type=UserDefinedType(Commit), required=False)
    #contributors = columns.List(value_type=UserDefinedType(Contrib), required=False)
    contributors =  columns.List(value_type=columns.Map(key_type=columns.Text(), value_type=columns.Text()))
    commits = columns.List(value_type=columns.Map(key_type=columns.Text(), value_type=columns.Text()))
    created_at = columns.Text(required=False)
    description = columns.Text(required=False)
    forks_count = columns.Integer(required=False)
    forks_url = columns.Text(required=False)
    open_issues_count = columns.Integer(required=False)

