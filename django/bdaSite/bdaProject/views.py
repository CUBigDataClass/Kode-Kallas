from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import json
import datetime
import pprint


def index(request):
    context = {}
    return render(request, 'bdaProject/index.html', context)

def org(request, org):
    context = {
        'org_name' : org
    }
    return render(request, 'bdaProject/organization.html', context)

def user(request, userId):
    pp = pprint.PrettyPrinter(indent=4)        
    req_sesh = requests.Session()
    req_sesh.auth = ('Pkanugov', '21a196f1b4849ffceaa070c7012b1baa422f54e6')
    
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