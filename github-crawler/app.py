from flask import Flask
app = Flask(__name__)
import lib.helper as helpp

#constants below
OWNER = 'vishwakulkarni'
github_api = "https://api.github.com"

helper = helpp.Helper()

@app.route('/')
def home_page():
    return 'Hello guys nothing here! just submit your github organization name at "/org/<orgname>"!'


@app.route('/org/<orgname>')
def org_parser(orgname):
    print("setting UP!!!")
    helper.set_org_name(orgname)
    org_data = helper.get_org_information(OWNER,github_api)
    print("Got Org Info!!!")
    print("sending Org Info to elastic search!!!")
    helper.send_to_elasticInstance(org_data,'org1',org_data['id'])
    print("Getting Repos for "+orgname)
    repo_list = helper.get_repositories(OWNER,github_api)
    print("sending repo info to elasticsearch")
    for repo in repo_list:
        repo['license']="test"
        helper.send_to_elasticInstance(repo,'repos',repo['id'])
        print("repo sent "+ repo['name'] )
    print("Done!!!!!!!!!")
    return 'We got your org name ' + orgname + ' give us some time to process your request, please check server output for progress'

    
if __name__ == "__main__":
    app.run(debug=True)