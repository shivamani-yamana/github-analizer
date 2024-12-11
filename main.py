import requests
import csv


GITHUB_ACCESS_TOKEN = ""

def getRepos(username):
    url = f'https://api.github.com/users/{user}/repos'
    response = None
    if(len(GITHUB_ACCESS_TOKEN)>0) :
        headers = {'Authorization': 'token ' + GITHUB_ACCESS_TOKEN}
        response = requests.get(url,headers=headers)
    else:
        response = requests.get(url)
    if(response.status_code != 200):
        return None
    return response.json()
users = []
with open("users.txt") as file:
    for line in file:
        users.append(line.rstrip("\n"))
users_data = []

for user in users:
    data = getRepos(user)
    if(data == None) :
        print(f"Error Fetching data for {user}")
    else:
        for detail in data:
            repoRecord = {}
            repoRecord["Username"]=user
            repoRecord["Repository Name"]=detail["name"]
            repoRecord["Stars"]=detail["stargazers_count"]
            repoRecord["Forks"]=detail["forks"]
            repoRecord["Open Issues"]=detail["open_issues"]
            repoRecord["Last Commit Date"]=detail["updated_at"].split("T")[0]
            users_data.append(repoRecord)
    
        
with open('user_records.csv','w',newline='') as csvFile:
    fieldNames = ["Username","Repository Name","Stars","Forks","Open Issues","Last Commit Date"]
    writer = csv.DictWriter(csvFile,fieldnames=fieldNames)
    writer.writeheader()
    writer.writerows(users_data)