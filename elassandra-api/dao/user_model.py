import uuid
from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType

class Users(Model):
    login = Text(primary_key=True, required=False)
    id = Integer(primary_key=True, required=False)
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
