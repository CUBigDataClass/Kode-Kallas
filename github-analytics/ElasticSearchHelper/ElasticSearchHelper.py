import json
from elasticsearch import Elasticsearch
from ElasticSearchHelper import config as config

es = Elasticsearch([{'host': config.ELASTIC_HOST, 'port': config.ELASTIC_PORT}])


class ElasticSearchHelper():
    def __init__(self):
        pass

    def getOrgData(self,orgname):
        res = es.search(index=orgname, body={"query": {"match_all": {}}})
        print(res)
        return json.dumps(res)

    def getUserData(self,username):
        res = es.search(index=username, body={"query": {"match_all": {}}})
        print(res)
        return json.dumps(res)

    def getRepoData(self,reponame):
        res = es.search(index=reponame, body={"query": {"match_all": {}}})
        print(res)
        return json.dumps(res)