# coding=utf-8

charsetFile=open("一二级汉字表.txt","r")
charCount = {}

for line in charsetFile:
    for c in line:
        charCount[c]=0

fileList = ["2016-"+i for i in ["01","02","03","04","05","06","07","08","09","10","11"]]
#fileList = ["2016-11"]
for fn in fileList:
    print(fn)
    with open("without_number/"+fn+"_all.txt","r",encoding="utf-8") as ppFile:
        for line in ppFile:
            for c in line:
                if c in charCount:charCount[c]+=1

charList = [(i,j) for i,j in charCount.items()]
charList.sort(key = lambda x : -x[1])

with open("stat.txt","w") as statFile:
    for a in charList:
        print(a[0],a[1],file=statFile)
