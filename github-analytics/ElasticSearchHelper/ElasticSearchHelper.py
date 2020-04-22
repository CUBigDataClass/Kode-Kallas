import json
from elasticsearch import Elasticsearch
from ElasticSearchHelper import config as config
from ElasticSearchHelper import Utils as utils

class ElasticSearchHelper():
    def __init__(self):
        pass

    def getOrgData(self, orgname):
        es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        res = es.search(index='org1', body={"query": {"match": {"login":orgname}}, "_source": config.ELASTIC_ORG_DATA_FIELDS, 'size': 1000})
        # res = utils.getFromElastic(config.ELASTIC_ORG_URL, utils.getOrgQuery(orgname))
        return res

    def getRepoData(self, orgname):
        es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        res = es.search(index='repos', body={"query": {"match": {"owner.login": orgname}}, "_source": config.ELASTIC_REPO_DATA_FIELDS, 'size': 1000})
        # res = utils.getFromElastic(config.ELASTIC_REPO_URL, utils.getReposQuery(orgname))
        return res

    def getOrgSpecificRepoData(self, orgname, reponame):
        es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        res = es.search(index='repos', body={"query": {"match": {"owner.login": orgname}, "match": {"name": reponame}}, "_source": config.ELASTIC_REPO_DATA_FIELDS, 'size': 1000})
        # res = utils.getFromElastic(config.ELASTIC_REPO_URL, utils.getSingleRepoOrgQuery(orgname, reponame))
        return res

    def getCommitData(self, orgname, reponame):
        print(orgname,reponame)
        # res = utils.getFromElastic(config.ELASTIC_COMMIT_URL, utils.getCommitQuery(orgname, reponame))
        # return res
        es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        try:
            res = es.search(index='commit', body={"query": { "bool": {
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
            }}, "_source": config.ELASTIC_COMMIT_DATA_FIELDS, 'size': 1000})
        except:
            pass
        return res

    def getUserData(self, orgname):
        es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        res = es.search(index='users', body={"query": {"match": {"org_name": orgname}}, "_source": config.ELASTIC_USER_DATA_FIELDS, 'size': 1000})
        # res = utils.getFromElastic(config.ELASTIC_USER_URL, utils.getUsersQuery(orgname))
        return res

    def getUserDataByUsername(self, username):
        es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        res = es.search(index='users', body={"query": {"match": {"login": username}}, "_source": config.ELASTIC_USER_DATA_FIELDS, 'size': 1000})
        # res = utils.getFromElastic(config.ELASTIC_USER_URL, utils.getUserByUsernameQuery(username))
        return res

    # def getRepoSpecificUserData(self, orgname, reponame):
        # es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        # res = es.search(index='repos', body={"query": {"match": {"owner.login": orgname}, "match": {"name": reponame}}, "_source": config.ELASTIC_REPO_DATA_FIELDS, 'size': 1000})
        # return res