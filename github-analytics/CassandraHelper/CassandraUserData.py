from CassandraHelper import Utils as utils
from CassandraHelper import config
from multiprocessing import Pool
from ElasticSearchHelper import ElasticSearchHelper as esh

class CassandraUserData():
    def __init__(self, elasticUserData):
        dataList = elasticUserData['hits']['hits']
        self.data = list()
        threadPool = Pool(config.THREAD_COUNT)
        self.data = threadPool.map(self.processDataList, dataList)
        print("Done CassandraRepoData")
        # for i in range(len(dataList)):
        #     self.data.append(self.processDataList(dataList[i]))

    def processDataList(self, userDataItem):
        return userDataItem['_source']
        # return userDataItem
        # elasticSearchHelper = esh.ElasticSearchHelper()
        # repoData = {
        #     "contributors": utils.get(utils.getContributorsList, userDataItem['contributors_url']),
        #     "name": userDataItem['name'],
        #     "commits": utils.processCommitData(elasticSearchHelper.getCommitData(userDataItem['owner']['login'], userDataItem['name'])), #utils.get(utils.getCommitsList, repoDataItem['commits_url'][:-6]),
        #     "created_at": userDataItem['created_at'],
        #     "issues": utils.get(utils.getIssuesList, userDataItem['issues_url'][:-9]),
        #     "id": userDataItem['id'],
        #     "watchers_count": userDataItem['watchers_count'],
        #     "description": userDataItem['description'],
        #     "forks_count": userDataItem['forks_count'],
        #     "forks_url": userDataItem['forks_url'],
        #     "full_name": userDataItem['full_name'],
        #     "html_url": userDataItem['html_url'],
        #     "languages": utils.get(utils.getLanguages, userDataItem['languages_url'], False),
        #     "owner": {
        #         "name": userDataItem['owner']['login'],
        #         "avatar_url": userDataItem['owner']['avatar_url'],
        #         "html_url": userDataItem['owner']['html_url'],
        #         "id": userDataItem['owner']['id'],
        #         "organizations_url": userDataItem['owner']['organizations_url']
        #     },
        #     "open_issues_count": userDataItem['open_issues_count'],
        #     "tags_url": userDataItem['tags_url'],
        #     "updated_at": userDataItem['updated_at']
        # }
        # return repoData