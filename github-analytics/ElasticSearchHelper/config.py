ELASTIC_HOST = 'http://localhost'
ELASTIC_PORT = 9200

ELASTIC_ORG_DATA_FIELDS = ["_id","avatar_url","description","email","followers","following","html_url","id","issues_url","location","members_url","name","node_id","login","url","updated_at","repos_url","public_repos","public_members_url","type"]

ELASTIC_REPO_DATA_FIELDS = ["contributors_url","name","owner.login","owner.organizations_url","commits_url","created_at","issues_url","id","watchers_count","description","forks_count","forks_url","full_name","html_url","languages_url","open_issues_count","owner.avatar_url","owner.html_url","owner.id","tags_url","updated_at"]

ELASTIC_COMMIT_DATA_FIELDS = ["stats.additions","stats.deletions","stats.total","commit.committer.date","committer.id","committer.login","commit.message"]

ELASTIC_USER_DATA_FIELDS = ["stats.additions","stats.deletions","stats.total","commit.committer.date","committer.id","committer.login","commit.message"]


ELASTIC_ORG_URL = ELASTIC_HOST + ":" + str(ELASTIC_PORT) + "/org/_search"

ELASTIC_REPO_URL = ELASTIC_HOST + ":" + str(ELASTIC_PORT) + "/repo/_search"

ELASTIC_COMMIT_URL = ELASTIC_HOST + ":" + str(ELASTIC_PORT) + "/commit/_search"

ELASTIC_USER_URL = ELASTIC_HOST + ":" + str(ELASTIC_PORT) + "/users/_search"

