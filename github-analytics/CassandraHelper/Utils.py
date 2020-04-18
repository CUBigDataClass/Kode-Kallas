import requests
from requests.auth import HTTPBasicAuth
from CassandraHelper import config
import json

# Http get request with callback
def get(function, url):
    try:
        r = requests.get(url, auth=HTTPBasicAuth(config.GITHUB_USER, config.GITHUB_TOKEN))
        return function(r.json())
    except:
        return []

def getContributorsList(data):
    contributorsList = list()
    for i in range(len(data)):
        # print("99999999999999999", data, "\n\n\n")
        contributor = dict()
        contributor['login'] = data[i]['login']
        contributor['id'] = data[i]['id']
        contributor['avatar_url'] = data[i]['avatar_url']
        contributor['html_url'] = data[i]['html_url']
        contributor['contributions'] = data[i]['contributions']
        contributorsList.append(contributor)
    return contributorsList