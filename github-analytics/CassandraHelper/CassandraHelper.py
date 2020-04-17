import requests
from CassandraHelper import config as config

class CassandraHelper():
    def __init__(self):
        pass
    
    def insertOrgData(self,orgdata):
        r = requests.post(config.CASSANDRA_URL_INSERT, json = orgdata)
        return r.status_code

    def insertUserData(self,userdata):
        r = requests.post(config.CASSANDRA_URL_INSERT, json = userdata)
        return r.status_code

    def insertRepoData(self,repodata):
        r = requests.post(config.CASSANDRA_URL_INSERT, json = repodata)
        return r.status_code