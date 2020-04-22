from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.staticfiles.storage import staticfiles_storage
import requests
import json
import datetime
import pprint
import math
import random

API_HOST = '10.0.0.172'
API_PORT = 4002

AK = 'AIzaSyBIwV5cs3QljMHkmRqVh9ogIeqesjXFlUk'

GITHUB_USERNAME = ''
GITHUB_PAT = ''


def index(request):
    context = {}
    return render(request, 'bdaProject/index.html', context)

def org(request, org):
    res = requests.get("http://"+API_HOST+":"+str(API_PORT)+"/repo/"+str(org))
    org_data = json.loads(res.text)
    
    # url = staticfiles_storage.path('mozilla.json')
    # with open(url) as f:
    #     org_data = json.load(f)
    
    req_sesh = requests.Session()
    req_sesh.auth = (GITHUB_USERNAME, GITHUB_PAT)
    
    num_org_repos = None
    if len(org_data) < 1000:
        num_org_repos = len(org_data)
    else:
        num_org_repos = str(len(org_data))+"+"

    languages_temp = set()
    contributor_ids = set()
    contributor_names = set()
    dict_repo_commits = {}
    dict_user_commits = {}
    list_repo_lang = []
    repo_lang_from = []
    repo_lang_to = []
    repo_lang_val = []

    i = 1
    for repo in org_data:
        for contributor in repo['contributors']:
            contributor_ids.add(contributor['id'])
            contributor_names.add(contributor['name'])
            
        langs = repo['languages']
        for k in langs.keys():
            languages_temp.add(k)

        dict_repo_commits[repo['name']] = len(repo['commits'])

        for commit in repo['commits']:
            try:
                dict_user_commits[commit['commiter_name']] += 1
            except:
                dict_user_commits[commit['commiter_name']] = 1

    for repo in org_data[:25]:
        langs = repo['languages']
        for lang, value in langs.items():
            try:
                repo_lang_from.append(repo['name'])
                repo_lang_to.append(lang)
                repo_lang_val.append(math.log(value))
            except:
                pass

    zipped = list(zip(repo_lang_from, repo_lang_to, repo_lang_val))
    zipped = sorted(zipped, key = lambda i: i[1])
    
    for i in zipped:
        repo_lang_dict = {}
        repo_lang_dict['from'] = i[0]
        repo_lang_dict['to'] = i[1]
        repo_lang_dict['value'] = i[2]
        list_repo_lang.append(repo_lang_dict)
    
    contributor_ids = list(contributor_ids)
    
    colors = ['red', 'yellow', 'green', 'blue', 'black', 'orange', \
              'pink', 'grey', 'purple', 'cyan', 'deep-purple', 'brown', \
              'teal', 'lime', 'white']
    
    languages = []
    
    for i, lang in enumerate(languages_temp):
        languages.append('<div class="chip"><i class="fa fa-circle ' \
                          +colors[(i%15)]+'-text"> </i> '+lang+'</div>')

    dict_repo_commits = sorted(dict_repo_commits.items(), key=lambda x: x[1], reverse=True)
    dict_user_commits = sorted(dict_user_commits.items(), key=lambda x: x[1], reverse=True)
     
    top_repos = []
    for repo in dict_repo_commits:
        top_repos.append(repo[0])
    
    top_users = []
    for contributor in contributor_names:
        if contributor != 'web-flow' and contributor != None:
            top_users.append(contributor)
            
    locations_src = []
    res = req_sesh.get("http://"+API_HOST+":"+str(API_PORT)+"/users/"+str(org))
    res = json.loads(res.text)
    
    for user in res:
        locations_src.append(user['location'])
    
    countries = set()
    for loc in locations_src:
        res = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+str(loc)+'&key='+AK)
        res = json.loads(res.text)
        
        if res['results']:
            for adr in res['results'][0]['address_components']:
                if adr['types'][0] == 'country':
                    countries.add(adr['short_name'])
    
    context = {
        'org_name' : org,
        'num_org_repos': num_org_repos,
        'num_org_contributors': len(contributor_ids),
        'languages': languages,
        'top_repos': top_repos,
        'top_users': top_users,
        'repo_lang_graph_data': list_repo_lang[:30],
        'countries': countries
    }
    return render(request, 'bdaProject/organization.html', context)

def repo(request, org, repoName):
    res = requests.get("http://"+API_HOST+":"+str(API_PORT)+"/repo/"+str(org)+"/"+str(repoName))
    org_data = json.loads(res.text)
    
    # url = staticfiles_storage.path('mozilla.json')
    # with open(url) as f:
    #     org_data = json.load(f)
    
    for repo in org_data:
        if repo['name'] == repoName:
            current_repo = repo
    current_repo = json.loads(res.text)[0]
            
    # repo_desc = current_repo['description']
    
    contributors = []
    for contributor in current_repo['contributors']:
        if contributor['name'] != 'web-flow':
            contributors.append(contributor['name'])
    
    languages = []
    for lang in current_repo['languages'].keys():
        languages.append(lang)

    forks_count = current_repo['forks_count']
    watchers_count = current_repo['watchers_count']
    
    repo_link = current_repo['html_url']
    repo_created_date = datetime.datetime.strptime(current_repo['created_at'], \
                        "%Y-%m-%dT%H:%M:%SZ").strftime('%d %b %Y')

    commits_time = []
    for commit in current_repo['commits']:
        c = {}
        # c['sha'] = commit['sha']
        c['date'] = datetime.datetime.strptime(commit['date'],"%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d')

        if len(c) != 0:
            commits_time.append(c)
    
    commits = []

    for i, commit in enumerate(reversed(current_repo['commits'])):
        commit_temp = {}
        commit_temp['number'] = i+1
        commit_temp['commiter_name'] = commit['commiter_name']
        commit_temp['body'] = commit['message']
        commit_temp['additions'] = commit['stats']['additions']
        commit_temp['deletions'] = commit['stats']['deletions']
        commit_temp['commited_at'] = datetime.datetime.strptime(commit['date'],"%Y-%m-%dT%H:%M:%SZ").strftime('%b %d %Y')
        commits.append(commit_temp)

    commits.reverse()

    quarters = {}
    commit_graph_labels = []
    commit_graph_values = []
    commits_time = sorted(commits_time, key = lambda i:i['date'])
    if commits_time:
        commit_graph_status = 1
        starting_year = datetime.datetime.strptime(commits_time[0]['date'], "%Y-%m-%d").year
        ending_year = datetime.datetime.strptime(commits_time[-1]['date'], "%Y-%m-%d").year
        
        for i in range(starting_year, ending_year+1):
            for j in range(4):
                quarters[str(i)+"-Q"+str(j+1)] = 0
        
        for date in commits_time:
            year = datetime.datetime.strptime(date['date'], "%Y-%m-%d").year
            month = datetime.datetime.strptime(date['date'], "%Y-%m-%d").month
            if month == 1 or month == 2 or month == 3:
                quarters[str(year)+"-Q1"] += 1
            elif month == 4 or month == 5 or month == 6:
                quarters[str(year)+"-Q2"] += 1
            elif month == 7 or month == 8 or month == 9:
                quarters[str(year)+"-Q3"] += 1
            elif month == 10 or month == 11 or month == 12:
                quarters[str(year)+"-Q4"] += 1

        for k,v in quarters.items():
            commit_graph_labels.append(k)
            commit_graph_values.append(v)
    else:
        commit_graph_status = None

    
    colors = ['red', 'yellow', 'green', 'blue', 'black', 'orange', \
              'pink', 'grey', 'purple', 'cyan', 'deep-purple', 'brown', \
              'teal', 'lime', 'white']
    
    languages = []
    languages_temp = []
    for lang in current_repo['languages'].keys():
        languages_temp.append(lang)
    
    for i, lang in enumerate(languages_temp):
        languages.append('<div class="chip"><i class="fa fa-circle ' \
                          +colors[(i%15)]+'-text"> </i> '+lang+'</div>')
        
    random.seed(1)
    
    issues_list = []
    for issue in current_repo['issues']:
        issue_temp = {}
        issue_temp['number'] = issue['number']
        issue_temp['title'] = issue['title']
        issue_temp['created_on'] = datetime.datetime.strptime(issue['created_at'],"%Y-%m-%dT%H:%M:%SZ").strftime('%b %d %Y')
        if issue['state'] == 'open':
            issue_temp['state'] = "<i class='fa fa-exclamation-circle red-text'> Open</i>"
        elif issue['state'] == 'closed':
            issue_temp['state'] = "<i class='fa fa-check-circle green-text'> Closed</i>"
        issue_temp['body'] = issue['body']
        if len(contributors) != 0:
            issue_temp['resolver'] = contributors[random.randint(0, len(contributors)-1)]
        else:
            issue_temp['resolver'] = ""
            
        issues_list.append(issue_temp)
    
    contributor_commits = {}

    for contributor in current_repo['contributors']:
        try:
            contributor_commits[contributor['name']] = contributor['contributions']
        except:
            contributor_commits[contributor['name']] = 0
            
    cpc_graph_title = "Commits per Contributor"
    cpc_graph_labels = []
    cpc_graph_values = []
    
    for k,v in contributor_commits.items():
        cpc_graph_labels.append(k)
        cpc_graph_values.append(v)
    
    
    context = {
        'org_name' : org,
        'repo_name' : repoName,
        # 'repo_desc': repo_desc,
        'forks_count': forks_count,
        'languages': languages,
        'repo_link': repo_link,
        'repo_created_date': repo_created_date,
        'watchers_count': watchers_count,
        'commits': commits,
        'commit_graph_status': commit_graph_status,
        'commit_graph_labels': commit_graph_labels,
        'commit_graph_values': commit_graph_values,
        'issues_list': issues_list[:50],
        'cpc_graph_title': cpc_graph_title,
        'cpc_graph_labels': cpc_graph_labels[:10],
        'cpc_graph_values': cpc_graph_values[:10],
        'contributors': contributors,
        
    }
    return render(request, 'bdaProject/repo.html', context)

def user(request, userId):
    pp = pprint.PrettyPrinter(indent=4)        
    req_sesh = requests.Session()
    req_sesh.auth = (GITHUB_USERNAME, GITHUB_PAT)
    
    req = req_sesh.get("https://api.github.com/users/"+str(userId))
    res = json.loads(req.text)
    
    user = {}
    user['user_id'] = userId
    user['user_img'] = res['avatar_url']
    user['user_name'] = res['name']
    user['user_pub_repos'] = res['public_repos']
    user['user_company'] = res['company']
    user['user_location'] = res['location']
    user['user_link'] = res['html_url']
    date = datetime.datetime.strptime(res['created_at'],"%Y-%m-%dT%H:%M:%SZ")
    user['user_join_date'] = date.strftime('%d %b %Y')
    
    req2 = req_sesh.get("https://api.github.com/users/"+str(userId)+"/repos?per_page=100")    
    res2 = json.loads(req2.text)
    
    repos_temp = []
    
    for repo in res2:
        repo_info = {}
        repo_info['name'] = repo['name']
        repo_info['commits_link'] = repo['commits_url'].replace("{/sha}", '')
        repo_info['language'] = repo['language']
        repos_temp.append(repo_info)
    
    repos = []
    
    for repo in repos_temp:
        req3 = req_sesh.get(repo['commits_link'])    
        res3 = json.loads(req3.text)
        commit_count = 0
        commits_temp = []
        try:   
            if res3['message']:
                commit_count = 0
        except:
            for commit in res3:
                c = {}
                if commit['author'] != None:
                    if commit['author']['login'] == userId:
                        commit_count += 1
                        c['sha'] = commit['sha']
                        c['date'] = commit['commit']['author']['date']
                
                if len(c) != 0:
                    commits_temp.append(c)
                    
        rc = {}
        rc['repo'] = repo['name']
        rc['repo_lang'] = repo['language']
        rc['commits'] = commits_temp
        rc['commit_count'] = commit_count
        repos.append(rc)

    commit_dates = []
    for i in repos:
        if i['commits'] != None:
            for j in i['commits']:
                date = datetime.datetime.strptime(j['date'],"%Y-%m-%dT%H:%M:%SZ")
                cd = date.strftime('%d-%m-%Y')
                commit_dates.append(cd)
        
    commit_dates.sort(key=lambda date: datetime.datetime.strptime(date, "%d-%m-%Y"))

    starting_year = datetime.datetime.strptime(commit_dates[0], "%d-%m-%Y").year
    ending_year = datetime.datetime.strptime(commit_dates[-1], "%d-%m-%Y").year

    quarters = {}
    for i in range(starting_year, ending_year+1):
        for j in range(4):
            quarters[str(i)+"-Q"+str(j+1)] = 0

    for date in commit_dates:
        year = datetime.datetime.strptime(date, "%d-%m-%Y").year
        month = datetime.datetime.strptime(date, "%d-%m-%Y").month
        if month == 1 or month == 2 or month == 3:
            quarters[str(year)+"-Q1"] += 1
        elif month == 4 or month == 5 or month == 6:
            quarters[str(year)+"-Q2"] += 1
        elif month == 7 or month == 8 or month == 9:
            quarters[str(year)+"-Q3"] += 1
        elif month == 10 or month == 11 or month == 12:
            quarters[str(year)+"-Q4"] += 1    
            
    commit_graph_labels = []
    commit_graph_values = []

    for k,v in quarters.items():
        commit_graph_labels.append(k)
        commit_graph_values.append(v)
        
    languages = set()
    repos_per_lang = {}
    commits_per_repo = {}
    commits_per_lang = {}

    for repo in repos:
        if repo['repo_lang'] != None:
            languages.add(repo['repo_lang'])
            repos_per_lang[repo['repo_lang']] = 0
            commits_per_lang[repo['repo_lang']] = 0
        commits_per_repo[repo['repo']] = repo['commit_count']

    for repo in repos:
        if repo['repo_lang'] != None:
            repos_per_lang[repo['repo_lang']] += 1
            commits_per_lang[repo['repo_lang']] += repo['commit_count']

    repos_per_lang = sorted(repos_per_lang.items(), key=lambda x: x[1], reverse=True)
    commits_per_repo = sorted(commits_per_repo.items(), key=lambda x: x[1], reverse=True)
    commits_per_lang = sorted(commits_per_lang.items(), key=lambda x: x[1], reverse=True)
    
    rpl_labels = []
    rpl_values = []

    cpr_labels = []
    cpr_values = []
    
    cpl_labels = []
    cpl_values = []

    for repo in repos_per_lang[:10]:
        rpl_labels.append(repo[0])
        rpl_values.append(repo[1])

    for commit in commits_per_repo[:10]:
        cpr_labels.append(commit[0])
        cpr_values.append(commit[1])
        
    for commit in commits_per_lang[:10]:
        cpl_labels.append(commit[0])
        cpl_values.append(commit[1])
    
        
    rpl_title = ""
    if len(rpl_labels) == 10:
        rpl_title = "Repos per Language (Top 10)"
    else:
        rpl_title = "Repos per Language"

    cpr_title = ""
    if len(cpr_labels) == 10:
        cpr_title = "Commits per Repo (Top 10)"
    else:
        cpr_title = "Commits per Repo"
    
    cpl_title = ""
    if len(cpl_labels) == 10:
        cpl_title = "Commits per Language (Top 10)"
    else:
        cpl_title = "Commits per Language"
        
    languages_temp = list(languages)
    languages = []
    
    colors = ['red', 'yellow', 'green', 'blue', 'black', 'orange', \
              'pink', 'grey', 'purple', 'cyan', 'deep-purple', 'brown', \
              'teal', 'lime', 'white']
    
    for i, lang in enumerate(languages_temp):
        languages.append('<div class="chip"><i class="fa fa-circle ' \
                          +colors[(i%15)]+'-text"> </i> '+lang+'</div>')
        
    context = {
        'user' : user,
        'languages': languages,
        'commit_graph_labels': commit_graph_labels,
        'commit_graph_values': commit_graph_values,
        'rpl_graph_title': rpl_title,
        'rpl_graph_labels': rpl_labels,
        'rpl_graph_values': rpl_values,
        'cpr_graph_title': cpr_title,
        'cpr_graph_labels': cpr_labels,
        'cpr_graph_values': cpr_values,
        'cpl_graph_title': cpl_title,
        'cpl_graph_labels': cpl_labels,
        'cpl_graph_values': cpl_values,
        'languages_list': languages_temp
    }
    return render(request, 'bdaProject/user.html', context)