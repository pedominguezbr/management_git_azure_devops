import git
import os
#import numpy as np
import pandas as pd

user="devopsazure"
projectName="myproject"
pathlistarepos = "C:\git-replace-deployment\python-delete-all-branch\listarepos.txt"
pathProcesaRepo = "C:\procesarepo"
reposList =[]

with open(pathlistarepos,'r') as f:
    reposListMas = f.readlines()
    for line in reposListMas:
        reposList.append(line.replace("\n",""))
        #print(line, end="")

#print(reposList)

dflote = pd.DataFrame({'Repositorio': reposList,'Url':'','Branchs':''})
dfRepo = pd.DataFrame(columns = ['Repositorio','Url','Branch'])
print(dflote)
print(dfRepo)
#Recorrer lista de repos
for index,row in dflote.iterrows():
    repoName = row["Repositorio"]
    print(f"{index} Procesando repoName: {repoName}")
    if (repoName!=''):
        repo=None
        pathrepo=f"{pathProcesaRepo}\{repoName}"

        print(f"Procesando Repo: {pathrepo}")
        repoUrl =f"https://{user}@dev.azure.com/{user}/{projectName}/_git/{repoName}"
        
        dflote.loc[index,"Url"] = repoUrl
        if not (os.path.exists(pathrepo)): 
            print("Directory is empty, Colando repo")
            repo = git.Repo.clone_from(repoUrl, pathrepo)
        else:        
            repo = git.Repo.init(pathrepo)

        # List remotes branch
        remote = repo.remote().fetch('-v')
        branchListDelete=[]

        #Set branch to lista 
        dflote.loc[index,"Branchs"] = remote
        for remote in remote:
            print(remote)
            #Add new Row Pandas            
            dfRepo = dfRepo.append({'Repositorio':repoName, 'Url':repoUrl, 'Branch':str(remote)},ignore_index=True)

            if str(remote)!='origin/develop' and str(remote)!='origin/test' and str(remote)!='origin/master':
                branchListDelete.append(str(remote).replace("origin/",""))
                #branchListDelete.append(str(remote))


        print(f"Lista de Branch a eliminar: {branchListDelete}")
        # Delete Remote Branch
        for remote in branchListDelete:
            print(f"Eliminando Branch: {remote}")
            repo.remotes.origin.push(refspec=(":%s" % remote))

print(dfRepo)
dfRepo.to_csv("branch_eliminados.csv")
#dflote.to_excel("output.xlsx",engine='xlsxwriter')
