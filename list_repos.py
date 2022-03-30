import requests
from requests.auth import HTTPBasicAuth
import json
import numpy as np
import pandas as pd


def save_file(namefile,dataArray):
    new_array = np.array(dataArray)

    with open(namefile, "w") as txt_file:
        #txt_file.write(str(new_array))
        for line in dataArray:
            print(line)
            txt_file.write(line+ "\n")

def get_git_repos(user,tokenDevops,url, fileNameResult="listarepos.txt"):
    dfRepo = pd.DataFrame(columns = ['id','Repositorio','Url'])
    headers = {'Content-Type': 'application/json'}   

    response = requests.get(url, auth = HTTPBasicAuth(user, tokenDevops), data=None, files=None, headers= headers)
    print(response)
    reposList= []
    if response.status_code == 200: # recibido
        print("respondio ok get_git_repos")
        #dataObtenida = json.loads(response.text)
        dataObtenida = response.json()
        #print(dataObtenida)
        for repo in dataObtenida["value"]:
            print(f"repo: {repo['name']}, {repo['url']}")
            #Add repo a Array
            reposList.append(repo['name'])
            #Add repo al DataFrame            
            df2 = pd.DataFrame({'id':[repo['id']],'Repositorio':[repo['name']], 'Url':[repo['url']]})
            dfRepo = pd.concat([dfRepo, df2], ignore_index = True)

    save_file(fileNameResult,reposList)
    return dfRepo

def get_git_ref(dfRepo,user,tokenDevops,projectName):
    headers = {'Content-Type': 'application/json'}
    defRepoBranch = pd.DataFrame(columns = ['Repositorio','Url','Branch'])
    for index,row in dfRepo.iterrows():
        idRepo = row["id"]
        repoName = row["Repositorio"]
        repoUrlid = row["Url"]
        print(f"index: {index}, idRepo: {idRepo}")
        repoUrl =f"https://{user}@dev.azure.com/{user}/{projectName}/_git/{repoName}"
        
        urlref =f"{repoUrlid}/refs?api-version=6.0"
        response = requests.get(urlref, auth = HTTPBasicAuth(user, tokenDevops), data=None, files=None, headers= headers)
        #print(response)
        if response.status_code == 200: # recibido
            #print("respondio ok")            
            dataObtenida = response.json()
            #print(dataObtenida)
            for branch in dataObtenida["value"]:
                print(f"branch: {branch['name']}")                
                df2 = pd.DataFrame({'Repositorio':[repoName], 'Url':[repoUrl], 'Branch':[branch['name']]})
                defRepoBranch = pd.concat([defRepoBranch, df2], ignore_index = True)
    return defRepoBranch

def Procesar():
    user="devopsazure"
    tokenDevops="0000fdsfd212fdf00000011111111"
    projectName="myproject"

    urlRepos=f"https://dev.azure.com/{user}/{projectName}/_apis/git/repositories?api-version=6.0"
    dfRepo = get_git_repos(user,tokenDevops,urlRepos,fileNameResult="listarepos.txt")
    print(dfRepo)
    dfRepo.to_excel("Repos.xlsx")

    defRepoBranch = get_git_ref(dfRepo,user,tokenDevops,projectName)
    print(defRepoBranch)

    defRepoBranch.to_excel("Repos_branchs.xlsx")

Procesar()