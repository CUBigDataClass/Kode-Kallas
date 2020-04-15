import json
import requests
from pandas.io.json import json_normalize
from sqlalchemy import create_engine, engine, text, types, MetaData, Table, String
from datetime import datetime


import config
import os

#elasticsearch
from elasticsearch import Elasticsearch

GITEA_APP_URL = 'YOUR_GITEA_API'
GITEA_TOKEN = 'f75b46df7511241ab8481caf80994d4aab7afb68'
GITHUB_USERNAME = 'vishwakulkarni'
GITHUB_TOKEN = 'f75b46df7511241ab8481caf80994d4aab7afb68'
SQL_ALCHEMY_STRING = ''



class Helper():
    def __init__(self):
        self.orgname = ""
        #set config working
        self.res = requests.get('http://localhost:9200')
        self.es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        #below setup for github
        self.github_api = "https://api.github.com"
        self.gh_session = requests.Session()
        self.gh_session.auth = (GITHUB_USERNAME, GITHUB_TOKEN)
    
    def set_org_name(self,orgname):
        self.orgname = orgname
        return

    def get_org_information(self,owner,api):
        url = api + '/orgs/{}'.format(self.orgname)
        org_data = self.gh_session.get(url = url)
        org_data=json.loads(org_data.content)
        return org_data

    def send_to_elasticInstance(self,data,index_name,id_val):
        self.es.index(index=index_name, doc_type='_doc',id=id_val, body=data)
    
    def get_repositories(self,owner,api):
        url = api + '/orgs/{}/repos'.format(self.orgname)
        org_repos_data = self.gh_session.get(url = url)
        org_repos_data=json.loads(org_repos_data.content)
        return org_repos_data


#testing comment after use
'''h = Helper()
github_api = "https://api.github.com"
h.set_org_name("mozilla")
print(h.get_org_information("vishwakulkarni",github_api))'''