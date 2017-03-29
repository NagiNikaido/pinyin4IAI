import json
import re

fileList = ["2016-"+i for i in ["01","02","03","04","05","06","07","08","09","10","11"]]
#fileList=["2016-01"]
if False:
    for fn in fileList:
        print(fn)
        with open(fn+".txt","r",encoding="utf-8") as rawFile, open("pr/"+fn+"_pr.txt","w",encoding="utf-8") as proFile:
            for line in rawFile:
                d1=json.loads(line)
                print(d1["title"],file=proFile)
                print(d1["html"],file=proFile)

puncs = re.compile(r"\s|[A-Za-z0-9]|\.|\(|\)|"+"|".join(["，","。","、","：","；","？","！","（","）","《","》",
                         "-","——","·","……","‘","’","“","”","/","\\[","\\]","【","】","\\|","℃"]))

for fn in fileList:
    print(fn)
    with open("pr/"+fn+"_pr.txt","r",encoding="utf-8") as proFile, open("pr/"+fn+"_all.txt","w",encoding="utf-8") as ppFile:
         for line in proFile:
             for pl in puncs.split(line):
                 if len(pl)>=4:
                    print(pl,file=ppFile)
