from flask import Flask
app = Flask(__name__)
import lib.helper as helpp
import csv

#constants below
OWNER = 'vishwakulkarni'
github_api = "https://api.github.com"

helper = helpp.Helper()

@app.route('/')
def home_page():
    return 'Hello guys nothing here! just submit your github organization name at "/org/<orgname>"!'


@app.route('/org/<orgname>')
def org_parser(orgname):
    csvwriter = csv.writer(open('lib/data/balancedData4.csv', 'w'))
    print("setting UP!!!")
    helper.set_org_name(orgname)
    org_data = helper.get_org_information(OWNER,github_api)
    print("Got Org Info!!!")
    print("sending Org Info to elastic search!!!")
    print(org_data)
    helper.send_to_elasticInstance(org_data,'org1',org_data['id'])
    print("Getting Repos for "+orgname)
    repo_list = helper.get_repositories(OWNER,github_api)
    print("sending repo info to elasticsearch")
    for repo in repo_list:
        repo['license']="test"
        helper.send_to_elasticInstance(repo,'repos',repo['id'])
        print("repo sent "+ repo['name'] )
    print("Getting Org Members for "+orgname)
    member_list = helper.get_org_users(OWNER,github_api)
    print("sending user info to elasticsearch")
    for member in member_list:
        user = helper.get_single_user(member['url'],orgname,github_api)
        user['org_name']=orgname
        helper.send_to_elasticInstance(user,'users',user['id'])
    print("Getting Commits from each repository")
    for repo in repo_list:
        commits = helper.commits_of_repo_github(repo['name'],orgname,github_api)
        print("sending to ES commits of",repo['name'])
        for commit in commits:
            helper.send_to_elasticInstance(commit,'commit',commit['sha'])
            # try:
            #     ls_line = [repo['name'], commit['author']['login'], 1, commit['author']['login'], commit["commit"]['author']['date'], commit["stats"]['additions'], commit["stats"]['deletions'], commit['stats']['total'], commit['commit']['message'], commit['committer']['html_url'], repo['url']]
            # except:
            #     print(repo['name'])
            #     ls_line = ""
            # if ls_line!="":
            #     csvwriter.writerow(ls_line)
    print("Done!!!!!!!!!")
    return 'We got your org name ' + orgname + ' give us some time to process your request, please check server output for progress'

    
if __name__ == "__main__":
    app.run(debug=True)