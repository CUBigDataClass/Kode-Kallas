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
GITEA_TOKEN = 'aff8945f859b696bf05932045f0be7e1b8379ddb'
GITHUB_USERNAME = 'vishwakulkarni'
GITHUB_TOKEN = 'aff8945f859b696bf05932045f0be7e1b8379ddb'
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
        repos_list = []
        next = True
        i=1
        while next == True:
            url = api + '/orgs/{}/repos?page={}&per_page=20'.format(self.orgname,i)
            original_data = self.gh_session.get(url=url)
            repos = json.loads(original_data.content)
            for repo in repos:
                repos_list.append(repo)
            if 'Link' in original_data.headers:
                if 'rel="next"' not in original_data.headers['Link']:
                    print(i)
                    next = False
            i = i + 1
        return repos_list
    
    def get_org_users(self,owner,api):
        members_list = []
        next = True
        i=1
        while next == True:
            url = api + '/orgs/{}/members?page={}&per_page=100'.format(self.orgname,i)
            original_data = self.gh_session.get(url=url)
            members = json.loads(original_data.content)
            for member in members:
                members_list.append(member)
            if 'Link' in original_data.headers:
                if 'rel="next"' not in original_data.headers['Link']:
                    print(i)
                    next = False
            i = i + 1
        
        return members_list

    #save commits of repos as json
    def commits_of_repo_github(self,repo, owner, api):
        commits = []
        next = True
        i = 1
        while next == True:
            url = api + '/repos/{}/{}/commits?page={}&per_page=100'.format(owner, repo, i)
            commit_pg = self.gh_session.get(url = url)
            commit_tp = json.loads(commit_pg.content)
            for commit in commit_tp:
                commits.append(commit) 
                print(commit)
            if 'Link' in commit_pg.headers:
                if 'rel="next"' not in commit_pg.headers['Link']:
                    next = False
            i = i + 1
        return commits




#testing comment after use
h = Helper()
github_api = "https://api.github.com"
h.set_org_name("CUBigDataClass")
#print(h.get_org_information("vishwakulkarni",github_api))
k=h.get_repositories('vishwakulkarni',github_api)
commits = h.commits_of_repo_github('kode-kallas','cubigdataclass',github_api)
for commit in commits:
    h.send_to_elasticInstance(commit,'commit',commit['sha'])
#print(len(k))
for mem in k:
    print(mem['name'])
    #commits = h.commits_of_repo_github(mem['name'],'vishwakulkarni',github_api)