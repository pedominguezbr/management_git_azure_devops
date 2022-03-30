import requests
from requests.auth import HTTPBasicAuth
import json
import numpy as np
import pandas as pd

def get_git_pr(user,tokenDevops,url, fileNameResult="listarepos.txt"):
    dfRepo = pd.DataFrame(columns = ['repoName','url','createDate','createBy','title','description','sourceRefName','targetRefName','mergeStatus','isDraft','reviewers'])
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, auth = HTTPBasicAuth(user, tokenDevops), data=None, files=None, headers= headers)
    print(response)    
    if response.status_code == 200: # recibido
        print("respondio ok get_git_pr")
        #dataObtenida = json.loads(response.text)
        dataObtenida = response.json()
        print(dataObtenida)
        for repo in dataObtenida["value"]:
            arrayreviewer=[]
            urlRepo=f"https://dev.azure.com/{user}/{repo['repository']['project']['name']}/_git/{repo['repository']['name']}/pullrequest/{repo['pullRequestId']}"         

            print(f"repo: {repo['pullRequestId']}, {repo['repository']['name']}, {urlRepo}")
            #Get reviewers
            for review in repo['reviewers']:
                print(review['displayName'])
                arrayreviewer.append(review['displayName'])

            #joiner str
            reviewer_str = "\n".join(arrayreviewer)
            #Add repo al DataFrame            
            df2 = pd.DataFrame({'repoName':[repo['repository']['name']],'url':[urlRepo], 'createDate':[repo['creationDate']], 'createBy':[repo['createdBy']['uniqueName']],'title':[repo['title']],'description':['null'],'sourceRefName':[repo['sourceRefName']],'targetRefName':[repo['targetRefName']],'mergeStatus':[repo['mergeStatus']],'isDraft':[repo['isDraft']],'reviewers':[reviewer_str]})
            dfRepo = pd.concat([dfRepo, df2], ignore_index = True)
    
    return dfRepo


def Procesar():
    user="devopsazure"
    tokenDevops="0000fdsfd212fdf00000011111111"
    projectName="myproject"

    nameFileGenerate="List_Pr.xlsx"

    urlPr=f"https://dev.azure.com/{user}/{projectName}/_apis/git/pullrequests?api-version=6.0"
    dfPrs = get_git_pr(user,tokenDevops,urlPr)
    print(dfPrs)

    print(f"creando archivo: {nameFileGenerate}")
    dfPrs.to_excel(nameFileGenerate)

Procesar()