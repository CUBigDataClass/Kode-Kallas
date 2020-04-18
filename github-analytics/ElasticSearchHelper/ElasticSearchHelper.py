import json
from elasticsearch import Elasticsearch
from ElasticSearchHelper import config as config

es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}])


class ElasticSearchHelper():
    def __init__(self):
        pass

    def getOrgData(self, orgname):
        res = es.search(index='org1', body={"query": {"match": {"login":orgname}}, "_source": config.ELASTIC_ORG_DATA_FIELDS, 'size': 1000})
        return res

    def getUserData(self, username):
        res = es.search(index=username, body={"query": {"match_all": {}}})
        return res

    def getRepoData(self, orgname):
        res = es.search(index='repos', body={"query": {"match": {"owner.login": orgname}}, "_source": config.ELASTIC_REPO_DATA_FIELDS, 'size': 1000})
        return res

