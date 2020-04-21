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
    return orgQuery


def getCommitQuery(orgname, reponame):
    commitQuery = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "comments_url": orgname
                        }
                    },
                    {
                        "match": {
                            "comments_url": reponame
                        }
                    }
                ]
            }
        },
        "_source": config.ELASTIC_COMMIT_DATA_FIELDS,
        "size": 1000
    }
    return commitQuery