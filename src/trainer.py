from codecvt import *
import pypinyin,json,time,multiprocessing,re
import os
import random,pickle

trainSetPath="train_set"

puncs = re.compile(r"\s\.|\(|\)|"+"|".join(["，","。","、","：","；","？","！","（","）","《","》",
                         "-","——","·","……","‘","’","“","”","/","\\[","\\]","【","】","\\|","℃"]))


def mapper(file_name):
    pairCount={(-1,-1):0}

    def analyse(context):
        for _pl in puncs.split(context):
            if len(_pl) <= 1: continue
            pl=list(_pl)
            if hasMulti(_pl) and random.uniform(0,1)<0.01:
                 ppl=pypinyin.lazy_pinyin(_pl,style=pypinyin.NORMAL,errors=lambda x : '*')
                 i,j=0,0
                 while True:
                     while i<len(pl) and not (pl[i] in charList): i+=1
                     while j<len(ppl) and not (ppl[j] in pinyinList): j+=1
                     if i>=len(pl) or j>=len(ppl): break
                     if isMulti(pl[i]):  pl[i]+="_"+ppl[j]
                     i+=1;j+=1
            last=[""]
            for c in pl:
                if c in extCharList:
                    if last!=[""]:
                        pairCount[(-1,-1)]+=len(last)
                        for _last in last:
                            t=(extCharNum[_last],extCharNum[c])
                            if t in pairCount: pairCount[t]+=1
                            else: pairCount[t]=1
                    if (-1,extCharNum[c]) in pairCount:
                        pairCount[(-1,extCharNum[c])]+=1
                    else: pairCount[(-1,extCharNum[c])]=1
                    last=[c]
                elif c in charList:
                    if last!=[""]:
                        pairCount[(-1,-1)]+=len(last)*len(charMap[c])
                        for _c in charMap[c]:
                            for _last in last:
                                t=(extCharNum[_last],extCharNum[c+"_"+_c])
                                if t in pairCount: pairCount[t]+=1
                                else: pairCount[t]=1
                    for _c in charMap[c]:
                        if (-1,extCharNum[c+"_"+_c]) in pairCount:
                            pairCount[(-1,extCharNum[c+"_"+_c])]+=1
                        else: pairCount[(-1,extCharNum[c+"_"+_c])]=1
                    last=[c+"_"+fn for fn in charMap[c]]
                else:last=[""]

    print("processing ",file_name,"... Start time: ", time.clock())
    with open(file_name,"r",encoding="utf-8") as fin:
        for line in fin:
            ld=json.loads(line)
            analyse(ld["title"])
            analyse(ld["html"])
    print(file_name," done. End time: ", time.clock())
    return pairCount

if __name__ == '__main__':
    try:
        fin=open("model.data","rb")
    except FileNotFoundError as e:
        pairCount={(-1,-1):0}
    else:
        pairCount=pickle.load(fin)
        fin.close()
    pairCountList=[]

    pool = multiprocessing.Pool()
    for fn in os.listdir(trainSetPath):
        pairCountList.append(pool.apply_async(\
                func=mapper,args=(trainSetPath+"/"+fn,)))
    pool.close()
    pool.join()

    for pc in pairCountList:
        for a,b in pc.get().items():
            if a in pairCount: pairCount[a]+=b
            else: pairCount[a]=b
    with open("model.data","wb") as fout: pickle.dump(pairCount,fout)
