import uuid
from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType


class author_model(UserType):
    login = Text(required=False)
    id = Integer(required=False)
    node_id = Text(required=False)
    avatar_url = Text(required=False)
    gravatar_id = Text(required=False)
    url = Text(required=False)
    html_url = Text(required=False)
    followers_url = Text(required=False)
    following_url = Text(required=False)
    gists_url = Text(required=False)
    starred_url = Text(required=False)
    subscriptions_url = Text(required=False)
    organizations_url = Text(required=False)
    repos_url = Text(required=False)
    events_url = Text(required=False)
    received_events_url = Text(required=False)
    type = Text(required=False)
    site_admin = Boolean(required=False)


class parent_model(UserType):
    sha = Text(required=False)
    url = Text(required=False)
    html_url = Text(required=False)


class stats_model(UserType):
    total = Integer(required=False)
    additions = Integer(required=False)
    deletions = Integer(required=False)


class files_model(UserType):
    sha = Text(required=False)
    filename = Text(required=False)
    status = Text(required=False)
    additions = Integer(required=False)
    deletions = Integer(required=False)
    changes = Integer(required=False)
    blob_url = Text(required=False)
    raw_url = Text(required=False)
    contents_url = Text(required=False)


class Commit(Model):
    sha = Text(primary_key=True, required=False)
    node_id = Text(required=False)
    url = Text(required=False)
    html_url = Text(required=False)
    comments_url = Text(required=False)
    committer = UserDefinedType(author_model)
    author = UserDefinedType(author_model)
    parents = List(value_type=UserDefinedType(parent_model))
    #files = List(value_type=UserDefinedType(files_model))
    stats = UserDefinedType(stats_model)



