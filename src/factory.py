# coding=utf-8
import threading, time
import multiprocessing
import queue

charsetFile=open("一二级汉字表.txt","r",encoding="gbk")
charMap, charCount = {}, 0

for line in charsetFile:
    for c in line:
        charMap[c]=charCount
        charCount+=1

charsetFile.close()

fileList = ["2016-"+i for i in ["01","02","03","04","05","06","07","08","09","10","11"]]
pairCountList = []
#fileList = ["2016-11"]

### multi-thread processing ###

def mapper(file_name):
    pairCount={(-1,-1):0}
    print("processing ",file_name,"... Start time: ", time.clock())
    with open(file_name,"r",encoding="utf-8") as fin:
        for line in fin:
            last=-1
            for c in line:
                if not c in charMap:
                    last=-1
                    continue
                if last!=-1:
                    t=charMap[c]
                    if (last,t) in pairCount: pairCount[(last,t)]+=1
                    else: pairCount[(last,t)]=1
                    pairCount[(-1,-1)]+=1
                last=charMap[c]
    print(file_name," done. End time: ", time.clock())
    return pairCount

pairCount = {(-1,-1):0}

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    for fn in range(11):
        pairCountList.append(pool.apply_async(func=mapper,args=("without_number/"+fileList[fn]+"_all.txt",)))
    pool.close()
    pool.join()


    for pc in pairCountList:
        for a,b in pc.get().items():
            if a in pairCount: pairCount[a]+=b
            else: pairCount[a]=b
    print(pairCount[(-1,-1)])
    with open("p_res.txt","w",encoding="utf-8") as fout:
        for a,b in pairCount.items():
            print(a[0],a[1],b,file = fout)
