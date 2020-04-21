import requests
from requests.auth import HTTPBasicAuth
from CassandraHelper import config
import json

# Http get request with callback
def get(function, url, isOutputlist=True):
    try:
        r = requests.get(url, auth=HTTPBasicAuth(config.GITHUB_USER, config.GITHUB_TOKEN))
        return function(r.json())
    except:
        if(not isOutputlist):
            return {}
        return []

def getContributorsList(data):
    contributorsList = list()
    for i in range(len(data)):
        contributor = dict()
        contributor['name'] = data[i]['login']
        contributor['id'] = data[i]['id']
        contributor['avatar_url'] = data[i]['avatar_url']
        contributor['html_url'] = data[i]['html_url']
        contributor['contributions'] = data[i]['contributions']
        contributorsList.append(contributor)
    return contributorsList

def getLanguages(data):
    return data

def getCommitsList(data):
    commitsList = list()
    for i in range(len(data)):
        commit = dict()
        commit['sha'] = data[i]['sha']
        commit['message'] = data[i]['commit']['message']
        commit['date'] = data[i]['commit']['committer']['date']
        commit['commiter_name'] = data[i]['committer']['login']
        commit['commiter_id'] = data[i]['committer']['id']
        commitsList.append(commit)
    return commitsList

def getIssuesList(data):
    issuesList = list()
    for i in range(len(data)):
        issue = dict()
        issue['id'] = data[i]['id']
        issue['number'] = data[i]['number']
        issue['title'] = data[i]['title']
        issue['body'] = data[i]['body']
        issue['state'] = data[i]['state']
        issue['created_at'] = data[i]['created_at']
        issue['updated_at'] = data[i]['updated_at']
        issue['closed_at'] = data[i]['closed_at']
        issue['labels'] = data[i]['labels']
        issuesList.append(issue)
    return issuesList

def processCommitData(data):
    data = data['hits']['hits']
    commitsList = list()
    for i in range(len(data)):
        commitData = data[i]['_source']
        commit = dict()
        commit['message'] = commitData['commit']['message']
        try:
            commit['date'] = commitData['commit']['committer']['date']
        except:
            commit['date'] = None
        try:
            commit['commiter_name'] = commitData['committer']['login']
        except:
            commit['commiter_name'] = None
        commit['stats'] = {
            "additions": commitData['stats']['additions'],
            "deletions": commitData['stats']['deletions'],
            "total": commitData['stats']['total']
        }
        try:
            commit['commiter_id'] = commitData['committer']['id']
        except:
            commit['commiter_id'] = None
        commitsList.append(commit)
    return commitsList