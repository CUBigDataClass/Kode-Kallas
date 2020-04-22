import requests
from ElasticSearchHelper import config
from flask import jsonify
import json

# Elastic search utils

# post request for Elastic
def getFromElastic(url, query):
    # try:
    r = requests.post(url, json=query)
    return r.json()
    # except:
    #     pass
        # return {'error': 'Error retrieving data from Elastic'}

def getOrgQuery(orgname):
    orgQuery = {
        "query": {
            "match": {
                "login": "games50"
            }
          },
        # "_source": config.ELASTIC_ORG_DATA_FIELDS,
        "size": 1000
    }
    return orgQuery

def getReposQuery(orgname):
    repoQuery = {
        "query": {
            "nested": {
                "path": "owner",
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"owner.login": orgname}}
                        ]
                    }
                }
            }
        },
        "_source": config.ELASTIC_REPO_DATA_FIELDS,
        "size": 1000
    }
    return repoQuery

def getSingleRepoOrgQuery(orgname, reponame):
    orgQuery = {
        "query": {
            "dis_max": {
              "queries": [
                { "match": { "owner.login": orgname } },
                { "match": { "name": reponame } }
              ],
              "tie_breaker": 0.3
            }
          }
        ,
        "_source": config.ELASTIC_REPO_DATA_FIELDS,
        "size": 1000
    }
    return orgQuery

def getCommitQuery(orgname, reponame):
    commitQuery = {
        "query": {
            "dis_max": {
              "queries": [
                { "match": { "org_name": orgname } },
                { "match": { "repo_name": reponame } }
              ],
              "tie_breaker": 0.3
            }
          }
        ,
        "_source": config.ELASTIC_COMMIT_DATA_FIELDS,
        "size": 1000
    }
    return commitQuery

def getUsersQuery(orgname):
    usersQuery = {
        "query":
            {"match": {"org_name": orgname} }
        ,
        "_source": config.ELASTIC_USER_DATA_FIELDS,
        "size": 1000
    }
    return usersQuery

def getUserByUsernameQuery(username):
    usersQuery = {
        "query":
            {"match": {"login": username} }
        ,
        "_source": config.ELASTIC_USER_DATA_FIELDS,
        "size": 1000
    }
    return usersQuery