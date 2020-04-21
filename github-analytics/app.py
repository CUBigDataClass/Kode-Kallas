from flask import Flask
from flask import jsonify

from config import config
from ElasticSearchHelper import ElasticSearchHelper as esh
from CassandraHelper import CassandraHelper as ch
from CassandraHelper import CassandraOrgData as cod
from CassandraHelper import CassandraRepoData as crd
from CassandraHelper import CassandraUserData as cud
from CassandraHelper import Utils as utils
import json

app = Flask(__name__)

elasticSearchHelper = esh.ElasticSearchHelper()
cassandraHelper = ch.CassandraHelper()


@app.route('/')
def home():
    return 'Github Analytics - Use APIs to process data. /org/{organization_name}'


@app.route('/org/<orgname>')
def orgRetrieve(orgname):
    elasticOrgData = elasticSearchHelper.getOrgData(orgname)
    # return elasticOrgData
    cassandraOrgData = cod.CassandraOrgData(elasticOrgData)
    return cassandraOrgData.data
    # return cassandraHelper.insertOrgData(cassandraOrgData.data)


@app.route('/repo/<orgname>')
def repoRetrieve(orgname):
    elasticRepoData = elasticSearchHelper.getRepoData(orgname)
    # return elasticRepoData
    cassandraRepoData = crd.CassandraRepoData(elasticRepoData)
    print("Done Done!")
    return jsonify(cassandraRepoData.data)

@app.route('/repo/<orgname>/<reponame>')
def repoRetrieveSingleOrg(orgname, reponame):
    elasticRepoData = elasticSearchHelper.getOrgSpecificRepoData(orgname,reponame)
    # return jsonify(utils.processCommitData(elasticRepoData))
    cassandraRepoData = crd.CassandraRepoData(elasticRepoData)
    print("Done Done!")
    return jsonify(cassandraRepoData.data)

@app.route('/users/<orgname>')
def userRetrieve(orgname):
    elasticUserData = elasticSearchHelper.getUserData(orgname)
    # return elasticUserData
    cassandraUserData = cud.CassandraUserData(elasticUserData)
    print("Done Done!")
    return jsonify(cassandraUserData.data)

@app.route('/users/<orgname>/<reponame>')
def userRetrieveSingleOrg(orgname, reponame):
    elasticUserData = elasticSearchHelper.getUserData(orgname, reponame)
    # return elasticUserData
    cassandraUserData = cud.CassandraUserData(elasticUserData)
    print("Done Done!")
    return jsonify(cassandraUserData.data)

@app.route('/username/<username>')
def userRetrieveByUsername(username):
    elasticUserData = elasticSearchHelper.getUserDataByUsername(username)
    # return elasticUserData
    cassandraUserData = cud.CassandraUserData(elasticUserData)
    print("Done Done!")
    return jsonify(cassandraUserData.data)

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=True)
