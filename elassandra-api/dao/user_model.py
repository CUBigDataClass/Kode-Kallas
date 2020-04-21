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
    name = Text(required=False)
    company = Text(required=False)
    blog = Text(required=False)
    location = Text(required=False)
    email = Text(required=False)
    hireable = Boolean(required=False)
    bio = Text(required=False)
    public_repos = Integer(required=False)
    public_gists = Integer(required=False)
    followers = Integer(required=False)
    following = Integer(required=False)
    created_at = Text(required=False)
    updated_at = Text(required=False)
    org_name = Text(required=False)


