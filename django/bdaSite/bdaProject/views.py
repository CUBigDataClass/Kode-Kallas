from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.staticfiles.storage import staticfiles_storage
import requests
import json
import datetime
import pprint
import math

def index(request):
    context = {}
    return render(request, 'bdaProject/index.html', context)

def org(request, org):
    url = staticfiles_storage.path('sampleJson.json')
    org_data = None
    with open(url) as f:
        org_data = json.load(f)
    
    num_org_repos = len(org_data)
    print("Num Repositories: " + str(num_org_repos))

    languages_temp = set()
    contributor_ids = set()
    dict_repo_commits = {}
    dict_user_commits = {}
    list_repo_lang = []
    repo_lang_from = []
    repo_lang_to = []
    repo_lang_val = []

    for repo in org_data:
        for contributor in repo['contributors']:
            contributor_ids.add(contributor['id'])

        langs = repo['languages']
        for k in langs.keys():
            languages_temp.add(k)

        dict_repo_commits[repo['name']] = len(repo['commits'])

        for commit in repo['commits']:
            try:
                dict_user_commits[commit['commiter-name']] += 1
            except:
                dict_user_commits[commit['commiter-name']] = 1

        langs = repo['languages']
        for lang, value in langs.items():
            repo_lang_from.append(repo['name'])
            repo_lang_to.append(lang)
            repo_lang_val.append(math.log(value))

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
                          +colors[i]+'-text"> </i> '+lang+'</div>')

    dict_repo_commits = sorted(dict_repo_commits.items(), key=lambda x: x[1], reverse=True)
    dict_user_commits = sorted(dict_user_commits.items(), key=lambda x: x[1], reverse=True)
    
    top_repos = []
    for repo in dict_repo_commits:
        top_repos.append(repo[0])
    
    top_users = []
    for repo in dict_user_commits:
        top_users.append(repo[0])
    
    context = {
        'org_name' : org,
        'num_org_repos': num_org_repos,
        'num_org_contributors': len(contributor_ids),
        'languages': languages,
        'top_repos': top_repos,
        'top_users': top_users,
        'repo_lang_graph_data': list_repo_lang
    }
    return render(request, 'bdaProject/organization.html', context)

def repo(request, org, repoName):
    url = staticfiles_storage.path('sampleJson.json')
    org_data = None
    with open(url) as f:
        org_data = json.load(f)
    
    for repo in org_data:
        if repo['name'] == 'pong':
            current_repo = repo
            break
            
    repo_desc = current_repo['description']
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
        c['sha'] = commit['sha']
        c['date'] = datetime.datetime.strptime(commit['date'],"%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d')

        if len(c) != 0:
            commits_time.append(c)

    commits_time = sorted(commits_time, key = lambda i:i['date'])
    starting_year = datetime.datetime.strptime(commits_time[0]['date'], "%Y-%m-%d").year
    ending_year = datetime.datetime.strptime(commits_time[-1]['date'], "%Y-%m-%d").year

    quarters = {}
    for i in range(starting_year, ending_year+1):
        for j in range(4):
            quarters[str(i)+"-Q"+str(j+1)] = 0
    
    colors = ['red', 'yellow', 'green', 'blue', 'black', 'orange', \
              'pink', 'grey', 'purple', 'cyan', 'deep-purple', 'brown', \
              'teal', 'lime', 'white']
    
    languages = []
    languages_temp = []
    for lang in current_repo['languages'].keys():
        languages_temp.append(lang)
    
    for i, lang in enumerate(languages_temp):
        languages.append('<div class="chip"><i class="fa fa-circle ' \
                          +colors[i]+'-text"> </i> '+lang+'</div>')

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

    commit_graph_labels = []
    commit_graph_values = []

    for k,v in quarters.items():
        commit_graph_labels.append(k)
        commit_graph_values.append(v)
    
    context = {
        'org_name' : org,
        'repo_name' : repoName,
        'repo_desc': repo_desc,
        'forks_count': forks_count,
        'languages': languages,
        'repo_link': repo_link,
        'repo_created_date': repo_created_date,
        'watchers_count': watchers_count,
        'commit_graph_labels': commit_graph_labels,
        'commit_graph_values': commit_graph_values,
    }
    return render(request, 'bdaProject/repo.html', context)

def user(request, userId):
    pp = pprint.PrettyPrinter(indent=4)        
    req_sesh = requests.Session()
    req_sesh.auth = ('', '')
    
    
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
                          +colors[i]+'-text"> </i> '+lang+'</div>')
        
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
    }
    return render(request, 'bdaProject/user.html', context)