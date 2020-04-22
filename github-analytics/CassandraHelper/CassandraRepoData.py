from CassandraHelper import Utils as utils
from CassandraHelper import config
from multiprocessing import Pool
from ElasticSearchHelper import ElasticSearchHelper as esh

class CassandraRepoData():
    def __init__(self, elasticOrgData):
        dataList = elasticOrgData['hits']['hits']
        self.data = list()
        threadPool = Pool(config.THREAD_COUNT)
        self.data = threadPool.map(self.processDataList, dataList)
        print("Done CassandraRepoData")
        # for i in range(len(dataList)):
        #     self.data.append(self.processDataList(dataList[i]))

    def processDataList(self, repoDataItem):
        repoDataItem = repoDataItem['_source']
        print(repoDataItem)
        elasticSearchHelper = esh.ElasticSearchHelper()
        repoData = {
            "contributors": utils.get(utils.getContributorsList, repoDataItem['contributors_url']),
            "name": repoDataItem['name'],
            "commits": utils.processCommitData(elasticSearchHelper.getCommitData(repoDataItem['owner']['login'], repoDataItem['name'])), #utils.get(utils.getCommitsList, repoDataItem['commits_url'][:-6]),
            "created_at": repoDataItem['created_at'],
            "issues": utils.get(utils.getIssuesList, repoDataItem['issues_url'][:-9]),
            "id": repoDataItem['id'],
            "watchers_count": repoDataItem['watchers_count'],
            # "description": repoDataItem['description'],
            "forks_count": repoDataItem['forks_count'],
            "forks_url": repoDataItem['forks_url'],
            "full_name": repoDataItem['full_name'],
            "html_url": repoDataItem['html_url'],
            "languages": utils.get(utils.getLanguages, repoDataItem['languages_url'], False),
            "owner": {
                "name": repoDataItem['owner']['login'],
                "avatar_url": repoDataItem['owner']['avatar_url'],
                "html_url": repoDataItem['owner']['html_url'],
                "id": repoDataItem['owner']['id'],
                "organizations_url": repoDataItem['owner']['organizations_url']
            },
            "open_issues_count": repoDataItem['open_issues_count'],
            "tags_url": repoDataItem['tags_url'],
            "updated_at": repoDataItem['updated_at']
        }
        return repoData