from flask import Flask

from config import config
from ElasticSearchHelper import ElasticSearchHelper as esh
from CassandraHelper import CassandraHelper as ch

app = Flask(__name__)

elasticSearchHelper = esh.ElasticSearchHelper()
cassandraHelper = ch.CassandraHelper()

@app.route('/')
def home():
    return 'Github Analytics - Use APIs to process data'


@app.route('/org/<orgname>')
def org_retrive(orgname):
    return elasticSearchHelper.getOrgName(orgname)

@app.route('/repo/<reponame>')
def repo_retrive(reponame):
    return reponame

@app.route('/user/<username>')
def user_retrive(username):
    return username


if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=True)
