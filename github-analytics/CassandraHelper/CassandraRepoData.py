from CassandraHelper import Utils as utils

class CassandraRepoData():
    def __init__(self, elasticOrgData):
        dataList = elasticOrgData['hits']['hits']
        self.data = list()
        for i in range(len(dataList)):
            repoDataItem = dataList[i]['_source']
            repoData = {
                "contributors": utils.get(utils.getContributorsList, repoDataItem['contributors_url']),
                "name": repoDataItem['name'],
                "commits_url": repoDataItem['commits_url'],
                "created_at": repoDataItem['created_at'],
                "issues_url": repoDataItem['issues_url'],
                "id": repoDataItem['id'],
                "watchers_count": repoDataItem['watchers_count'],
                "description": repoDataItem['description'],
                "forks_count": repoDataItem['forks_count'],
                "forks_url": repoDataItem['forks_url'],
                "full_name": repoDataItem['full_name'],
                "html_url": repoDataItem['html_url'],
                "languages_url": repoDataItem['languages_url'],
                "owner":{
                    "login": repoDataItem['owner']['login'],
                    "avatar_url": repoDataItem['owner']['avatar_url'],
                    "html_url": repoDataItem['owner']['html_url'],
                    "id": repoDataItem['owner']['id'],
                    "organizations_url": repoDataItem['owner']['organizations_url']
                },
                "open_issues_count": repoDataItem['open_issues_count'],
                "tags_url": repoDataItem['tags_url'],
                "updated_at": repoDataItem['updated_at']
            }
            self.data.append(repoData)