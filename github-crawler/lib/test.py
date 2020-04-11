#!/usr/bin/env python
# coding: utf-8

# In order to extract data from Github, we are going to leverage the Github REST API v3, that can be found in this link https://developer.github.com/v3/.
# In `config.py` file we need to define the following configuration variables, that are going to be accessed by the current notebook:
# - `GITHUB_USERNAME`
# - `GITHUB_TOKEN`
# - `SQL_ALCHEMY_STRING` (only if we want to save our Github results in a relational database)

import json
import requests
from pandas.io.json import json_normalize
from sqlalchemy import create_engine, engine, text, types, MetaData, Table, String
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import numpy as np
from datetime import datetime


import config
import os

#elasticsearch
from elasticsearch import Elasticsearch


#set config working
res = requests.get('http://localhost:9200')
#print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])


# function that converts all object columns to strings, in order to store them efficiently into the database
def objects_to_strings(table):
    measurer = np.vectorize(len)
    df_object = table.select_dtypes(include=[object])
    string_columns = dict(zip(df_object, measurer(
        df_object.values.astype(str)).max(axis=0)))
    string_columns = {key: String(length=value) if value > 0 else String(length=1)
                      for key, value in string_columns.items() }
    return string_columns


github_api = "https://api.github.com"
gh_session = requests.Session()
gh_session.auth = (config.GITHUB_USERNAME, config.GITHUB_TOKEN)


def branches_of_repo(repo, owner, api):
    branches = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/branches?page={}&per_page=100'.format(owner, repo, i)
        branch_pg = gh_session.get(url = url)
        branch_pg_list = [dict(item, **{'repo_name':'{}'.format(repo)}) for item in branch_pg.json()]    
        branch_pg_list = [dict(item, **{'owner':'{}'.format(owner)}) for item in branch_pg_list]
        branches = branches + branch_pg_list
        if 'Link' in branch_pg.headers:
            if 'rel="next"' not in branch_pg.headers['Link']:
                next = False
        i = i + 1
    return branches


#branches = json_normalize(branches_of_repo('Social-media-impact-cryptocurrency', 'vishwakulkarni', github_api))


#branches.to_csv('data/branches.csv')


def get_repositories_itterative(org_name,owner,api):
    repos = []
    next = True
    i = 1
    while next == True:
        url = api + '/orgs/{}/repos??page={}&per_page=100'.format(org_name,i)
        repos_pg = gh_session.get(url = url)
        #print(repos_pg.json())
        repos_pg_list = [dict(item, **{'repo_name':'{}'.format(org_name)}) for item in repos_pg.json()]    
        repos_pg_list = [dict(item, **{'owner':'{}'.format(owner)}) for item in repos_pg_list]
        print(repos_pg_list)
        repos = repos + repos_pg_list
        if 'Link' in repos_pg.headers:
            if 'rel="next"' not in repos_pg.headers['Link']:
                next = False
        i = i + 1
        break
    return repos
#org repo fetcher
#orgs = json_normalize(get_repositories_itterative('CUBigDataClass', 'vishwakulkarni', github_api))
#orgs.to_csv('data/org.csv')

def get_org_information(org_name,owner,api):
    url = api + '/orgs/{}'.format(org_name)
    org_data = gh_session.get(url = url)
    org_data=json.loads(org_data.content)
    return org_data

def send_to_elasticInstance(data,index_name,id_val):
    es.index(index=index_name, doc_type='_doc',id=id_val, body=data)


#getting org info
#org_data = get_org_information('duckduckgo', 'vishwakulkarni', github_api)
#send_to_elasticInstance(org_data,'org1',org_data['id'])

#how to get documents
'''
doc = {
        'size' : 10000,
        'query': {
            'match_all' : {}
       }
   }
res = es.search(index='org1', doc_type='_doc', body=doc,scroll='1m')
print(res)'''


#get Repositorries and send to es

def get_repositories(org_name,owner,api):
    url = api + '/orgs/{}/repos'.format(org_name)
    org_repos_data = gh_session.get(url = url)
    org_repos_data=json.loads(org_repos_data.content)
    return org_repos_data

#uncomment below after testing
'''
#get repos and push it to elasticsearch
org_repos = get_repositories('CUBigDataClass', 'vishwakulkarni',github_api)

for repo in org_repos:
    repo['license']="test"
    send_to_elasticInstance(repo,'repos',repo['id'])
    #commits_of_repo_github()


#write repo list to repos_list
#with open("data/repos_list.json", "w") as outfile: 
#    outfile.write(json.dumps(org_repos,indent=4)) 
'''

#save commits of repos as json
def commits_of_repo_github(repo, owner, api):
    commits = []
    next = True
    i = 1
    while next == True:
        url = api + '/repos/{}/{}/commits?page={}&per_page=100'.format(owner, repo, i)
        commit_pg = gh_session.get(url = url)
        commit_tp = json.loads(commit_pg.content)
        for commit in commit_tp:
            commits.append(commit) 
        if 'Link' in commit_pg.headers:
            if 'rel="next"' not in commit_pg.headers['Link']:
                next = False
        i = i + 1
    return commits

commits = commits_of_repo_github('hard-decisions','CUBigDataClass',github_api)

def add_commits_to_elasticsearch(commits):
    for commit in commits:
        es.index(index='commits', doc_type='_doc',id=commit['sha'], body=commit)

add_commits_to_elasticsearch(commits)

with open("data/commits.json", "w") as outfile: 
    outfile.write(json.dumps(commits,indent=4)) 
