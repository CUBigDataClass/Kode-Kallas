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
        return res

    def getUserData(self, username):
        es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        res = es.search(index=username, body={"query": {"match_all": {}}})
        return res

    def getRepoData(self, orgname):
        query = utils.getOrgQuery(orgname)
        res = utils.getFromElastic(config.ELASTIC_REPO_URL, query)
        return res

    def getOrgSpecificRepoData(self, orgname, reponame):
        es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}], timeout=30)
        res = es.search(index='repos', body={"query": {"match": {"owner.login": orgname}, "match": {"name": reponame}}, "_source": config.ELASTIC_REPO_DATA_FIELDS, 'size': 1000})
        return res

    def getCommitData(self, orgname, reponame):
        print(orgname,reponame)
        query = utils.getCommitQuery(orgname, reponame)
        res = utils.getFromElastic(config.ELASTIC_REPO_URL, query)
        return res
        # try:
        #     res = es.search(index='commit', body={"query": { "bool": {
        #         "must": [
        #                     {
        #                       "match": {
        #                         "comments_url": orgname
        #                       }
        #                     },
        #                     {
        #                       "match": {
        #                         "comments_url": reponame
        #                       }
        #                     }
        #                   ]
        #     }}, "_source": config.ELASTIC_COMMIT_DATA_FIELDS, 'size': 1000})
        # except:
        #     pass
        # return res