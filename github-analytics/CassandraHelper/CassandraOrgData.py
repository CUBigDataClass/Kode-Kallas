class CassandraOrgData():
    def __init__(self, elasticOrgData):
        data = elasticOrgData['hits']['hits'][0]['_source']
        self.data = data
        # self.data = {
        #     "avatar_url": data['avatar_url'],
        #     "description": data['description'],
        #     "email": data['email'],
        #     "followers": data['followers'],
        #     "following": data['following'],
        #     "html_url": data['html_url'],
        #     "id": data['id'],
        #     "issues_url": data['issues_url'],
        #     "location": data['location'],
        #     "login": data['login'],
        #     "members_url": data['members_url'],
        #     "name": data['name'],
        #     "node_id": data['node_id'],
        #     "public_members_url": data['public_members_url'],
        #     "public_repos": data['public_repos'],
        #     "repos_url": data['repos_url'],
        #     "type": data['type'],
        #     "updated_at": data['updated_at'],
        #     "url": data['url']
        # }