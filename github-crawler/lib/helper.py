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
GITEA_TOKEN = 'a3020c009c6d46783158b5ffb0d1a7c55735bcc4'
GITHUB_USERNAME = 'karthiks1995'
GITHUB_TOKEN = 'a5a8eeee34f3879255448c77d9324ef49fd01f0b'
SQL_ALCHEMY_STRING = ''

import requests

# url = "http://34.66.21.21:5000/insert"

# payload = "{\n    \"org\": \"org\",\n    \"table\": \"repo\",\n    \"body\": [\n        {\n            \"id\": 16750294,\n            \"node_id\": \"MDEwOlJlcG9zaXRvcnkxNjc1MDI5NA==\",\n            \"name\": \"Twitter-EmotiMap\",\n            \"full_name\": \"CUBigDataClass/Twitter-EmotiMap\",\n            \"private\": false,\n            \"owner\": {\n                \"login\": \"CUBigDataClass\",\n                \"id\": 6345918,\n                \"node_id\": \"MDEyOk9yZ2FuaXphdGlvbjYzNDU5MTg=\",\n                \"avatar_url\": \"https://avatars0.githubusercontent.com/u/6345918?v=4\",\n                \"gravatar_id\": \"\",\n                \"url\": \"https://api.github.com/users/CUBigDataClass\",\n                \"html_url\": \"https://github.com/CUBigDataClass\",\n                \"followers_url\": \"https://api.github.com/users/CUBigDataClass/followers\",\n                \"following_url\": \"https://api.github.com/users/CUBigDataClass/following{/other_user}\",\n                \"gists_url\": \"https://api.github.com/users/CUBigDataClass/gists{/gist_id}\",\n                \"starred_url\": \"https://api.github.com/users/CUBigDataClass/starred{/owner}{/repo}\",\n                \"subscriptions_url\": \"https://api.github.com/users/CUBigDataClass/subscriptions\",\n                \"organizations_url\": \"https://api.github.com/users/CUBigDataClass/orgs\",\n                \"repos_url\": \"https://api.github.com/users/CUBigDataClass/repos\",\n                \"events_url\": \"https://api.github.com/users/CUBigDataClass/events{/privacy}\",\n                \"received_events_url\": \"https://api.github.com/users/CUBigDataClass/received_events\",\n                \"type\": \"Organization\",\n                \"site_admin\": false\n            },\n            \"html_url\": \"https://github.com/CUBigDataClass/Twitter-EmotiMap\",\n            \"description\": \"Twitter feed mining with geographical emotional trend analysis.\",\n            \"fork\": false,\n            \"url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap\",\n            \"forks_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/forks\",\n            \"keys_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/keys{/key_id}\",\n            \"collaborators_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/collaborators{/collaborator}\",\n            \"teams_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/teams\",\n            \"hooks_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/hooks\",\n            \"issue_events_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/issues/events{/number}\",\n            \"events_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/events\",\n            \"assignees_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/assignees{/user}\",\n            \"branches_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/branches{/branch}\",\n            \"tags_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/tags\",\n            \"blobs_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/git/blobs{/sha}\",\n            \"git_tags_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/git/tags{/sha}\",\n            \"git_refs_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/git/refs{/sha}\",\n            \"trees_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/git/trees{/sha}\",\n            \"statuses_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/statuses/{sha}\",\n            \"languages_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/languages\",\n            \"stargazers_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/stargazers\",\n            \"contributors_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/contributors\",\n            \"subscribers_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/subscribers\",\n            \"subscription_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/subscription\",\n            \"commits_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/commits{/sha}\",\n            \"git_commits_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/git/commits{/sha}\",\n            \"comments_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/comments{/number}\",\n            \"issue_comment_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/issues/comments{/number}\",\n            \"contents_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/contents/{+path}\",\n            \"compare_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/compare/{base}...{head}\",\n            \"merges_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/merges\",\n            \"archive_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/{archive_format}{/ref}\",\n            \"downloads_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/downloads\",\n            \"issues_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/issues{/number}\",\n            \"pulls_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/pulls{/number}\",\n            \"milestones_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/milestones{/number}\",\n            \"notifications_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/notifications{?since,all,participating}\",\n            \"labels_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/labels{/name}\",\n            \"releases_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/releases{/id}\",\n            \"deployments_url\": \"https://api.github.com/repos/CUBigDataClass/Twitter-EmotiMap/deployments\",\n            \"created_at\": \"2014-02-12T00:05:56Z\",\n            \"updated_at\": \"2016-04-04T16:36:01Z\",\n            \"pushed_at\": \"2014-05-16T14:32:48Z\",\n            \"git_url\": \"git://github.com/CUBigDataClass/Twitter-EmotiMap.git\",\n            \"ssh_url\": \"git@github.com:CUBigDataClass/Twitter-EmotiMap.git\",\n            \"clone_url\": \"https://github.com/CUBigDataClass/Twitter-EmotiMap.git\",\n            \"svn_url\": \"https://github.com/CUBigDataClass/Twitter-EmotiMap\",\n            \"homepage\": \"http://www.mattkgross.com/TwitterMap\",\n            \"size\": 99797,\n            \"stargazers_count\": 0,\n            \"watchers_count\": 0,\n            \"language\": \"Python\",\n            \"has_issues\": true,\n            \"has_projects\": true,\n            \"has_downloads\": true,\n            \"has_wiki\": true,\n            \"has_pages\": false,\n            \"forks_count\": 0,\n            \"mirror_url\": null,\n            \"archived\": false,\n            \"disabled\": false,\n            \"open_issues_count\": 0,\n            \"license\": null,\n            \"forks\": 0,\n            \"open_issues\": 0,\n            \"watchers\": 0,\n            \"default_branch\": \"master\",\n            \"permissions\": {\n                \"admin\": false,\n                \"push\": false,\n                \"pull\": true\n            }\n        }\n    ]\n}"
# headers = {
#     'content-type': "application/json",
#     'cache-control': "no-cache",
#     'postman-token': "12e57a3e-e251-8cd6-3844-e94e41c04245"
#     }

# response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)

class Helper():
    def __init__(self):
        self.orgname = ""
        #set config working
        self.res = requests.get('http://localhost:9200')
        self.es = Elasticsearch([{'host': '104.198.255.128', 'port': '9200'}])
        #below setup for github
        self.github_api = "https://api.github.com"
        self.gh_session = requests.Session()
        self.gh_session.auth = (GITHUB_USERNAME, GITHUB_TOKEN)
        self.ellasandra_api = "http://34.66.21.21:5000"
        #self.ellasandra_api = "http://localhost:5000"
        self.headers = {
                    'content-type': "application/json",
                    'cache-control': "no-cache",
                    'postman-token': "12e57a3e-e251-8cd6-3844-e94e41c04245"
                }
    
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
    
    def send_org_data_to_ellasandra(self,payload):
        data = {}
        data['table']='org'
        data['body'] = []
        data['body'].append(payload)
        url = self.ellasandra_api + '/insert'
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.status_code
    
    def send_repo_data_to_ellasandra(self,payload):
        data = {}
        data['org']=self.orgname
        data['body'] = payload
        data['table'] = 'repo'
        url = self.ellasandra_api + '/insert'
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.status_code
    
    def send_users_to_ellasandra(self,payload):
        data = {}
        data['org']=self.orgname
        data['body'] = payload
        data['table'] = 'users'
        url = self.ellasandra_api + '/insert'
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.status_code
    
    def send_commits_to_ellasandra(self,payload):
        data = {}
        for i in range(len(payload)):
            del payload[i]['files']
            del payload[i]['commit']['tree']
            del payload[i]['commit']['verification']
            url = payload[i]['url'].split('/')
            payload[i]["org_name"] = url[4]
            payload[i]["repo_name"] = url[5]

        data['org']=self.orgname
        data['body'] = payload
        data['table'] = 'commit'
        url = self.ellasandra_api + '/insert'
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.status_code

    def get_repositories(self,owner,api):
        repos_list = []
        next = True
        i=1
        while next == True:
            url = api + '/orgs/{}/repos?page={}&per_page=300'.format(self.orgname,i)
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
            url = api + '/orgs/{}/members?page={}&per_page=1000'.format(self.orgname,i)
            original_data = self.gh_session.get(url=url)
            members = json.loads(original_data.content)
            for member in members:
                members_list.append(member)
            if 'Link' in original_data.headers:
                if 'rel="next"' not in original_data.headers['Link']:
                    print(i)
                    next = False
            i = i + 1
        with open("users_microsoft.json", "w") as outfile: 
            outfile.write(json.dumps(members_list,indent=4)) 
        
        return members_list

    def get_single_user(self,url,owner,api):
        original_data = self.gh_session.get(url=url)
        user = json.loads(original_data.content)
        return user

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
                try:
                    url = commit['url']
                    single_commit = self.gh_session.get(url = url)
                    single_commit = json.loads(single_commit.content)
                    commits.append(single_commit)
                except:
                    print("issue with",commit)
                    return commits

                #print(commit)
            if 'Link' in commit_pg.headers:
                if 'rel="next"' not in commit_pg.headers['Link']:
                    next = False
            i = i + 1
        return commits

'''
import csv

#testing comment after use
h = Helper()
github_api = "https://api.github.com"
h.set_org_name("games50")
userInfo = h.get_single_user("https://api.github.com/users/vishwakulkarni","vishwakulkarni",github_api)
#users = h.get_org_users('CUBigDataClass',github_api)
test = []
repo_list = h.get_repositories('vishwakulkarni',github_api)
for repo in repo_list:
    repo['license']="test"
    test.append(repo)
#print(test)
data = {}
data['org']="CUBigDataClass"
data['table'] = "repo"
data['body'] = test
#print(json.dumps(data))
h.send_to_ellasandra(data)

users = h.get_org_users('CUBigDataClass',github_api)
ls = {}
for user in users:
    #print(user)
    url = user['url']
    usr = h.get_single_user(url,'vishwakulkarni',github_api)
    print(usr['name'],usr['location'])
    usr['orgname'] = 'CUBigDataClass'
    print(usr)
    break

print(ls)

csvwriter = csv.writer(open('data/balancedData4.csv', 'w'))
#print(h.get_org_information("vishwakulkarni",github_api))
k=h.get_repositories('vishwakulkarni',github_api)
commits = h.commits_of_repo_github('kode-kallas','cubigdataclass',github_api)
#with open("commits.json", "w") as outfile: 
#    outfile.write(json.dumps(commits,indent=4)) 
#print(commits[0]['stat'])
for commit in commits:
    print(commit)
    h.send_to_elasticInstance(commit,'commit',commit['sha'])
    try:
        ls_line = ['Kode-Kallas', commit['author']['login'], 1, commit["commit"]['author']['name'], commit["commit"]['author']['date'], commit["stats"]['additions'], commit["stats"]['deletions'], commit['stats']['total'], commit['commit']['message'], commit['committer']['html_url'], 'url']
    except:
        ls_line = ""
    if ls_line!="":
        csvwriter.writerow(ls_line)
#print(len(k))
for mem in k:
    print(mem['name'])
    #commits = h.commits_of_repo_github(mem['name'],'vishwakulkarni',github_api)'''