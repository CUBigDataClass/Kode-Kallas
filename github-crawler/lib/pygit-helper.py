from github import Github

# using username and password
#g = Github("user", "password")

# or using an access token
g = Github("f75b46df7511241ab8481caf80994d4aab7afb68")

org = g.get_organization("CUBigDataClass")
print(org.login)
names = org.get_members()
repos = org.get_repos()
members = org.get_members()
#
#for name in names:
#    print(name)

i=0
for repo in repos:
    i=i+1
    #print(i,repo.name)

for mem in members:
    print(mem.name)