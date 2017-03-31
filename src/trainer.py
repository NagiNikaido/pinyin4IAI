from codecvt import *
import pypinyin,json,time,multiprocessing,re
import os,tempfile
import random,pickle

trainSetPath="train_set"

puncs = re.compile(r"\s|\.|\(|\)|"+"|".join(["，","。","、","：","；","？","！","（","）","《","》",
                         "-","——","·","……","‘","’","“","”","/","\\[","\\]","【","】","\\|","℃"]))

def _add_val(_key,_dict,_delta=1):
    if _key in _dict: _dict[_key]+=_delta
    else:  _dict[_key]=_delta

def mapper(file_name,dump_pipe):
    pairCount={(-2,-1):0,(-1,-1):0}

    def analyse(context):
        lc=list(puncs.split(context))
        for cl in lc:
            if len(cl)<=1: continue
            if random.uniform(0,1)<0.01 and hasMulti(cl):
#                print(cl)
                dump_pipe.send(cl)
            last=""
            for ll in cl:
                if not ll in charList: last=""
                else:
                    _add_val((-2,-1),pairCount)
                    _add_val((-2,charNum[ll]),pairCount)
                    if last!="":
                        _add_val((-1,-1),pairCount)
                        _add_val((-1,charNum[ll]),pairCount)
                        _add_val((charNum[last],charNum[ll]),pairCount)
                    last=ll

    print("processing ",file_name,"... Start time: ", time.clock())
    with open(trainSetPath+os.path.sep+file_name,"r",encoding="utf-8") as fin:
        for line in fin:
            if line.strip()=="":continue
            ld=json.loads(line)
            analyse(ld["title"])
            analyse(ld["html"])
    print(file_name," done. End time: ", time.clock())
    dump_pipe.send("***STOP***")
    dump_pipe.close()
    return pairCount

def post_mapper(recv_pipe):
    pairCount={}
    print(time.clock())
    while True:
        try: line=recv_pipe.recv()
        except EOFError: break
        if line == "***STOP***":break
        pl,ppl=list(line),pypinyin.lazy_pinyin(line,style=pypinyin.NORMAL,errors=lambda x : '*')
        i,j=0,0
        while True:
            while i<len(pl) and not (pl[i] in charList): i+=1
            while j<len(ppl) and not (ppl[j] in pinyinList): j+=1
            if i>=len(pl) or j>=len(ppl): break
            if isMulti(pl[i]):  pl[i]+="_"+ppl[j]
            i+=1;j+=1
        last=""
        for c in pl:
            if not c in extCharList: last=""
            else:
                if last!="" and (len(c)>1 or len(last)>1):
                    _add_val((extCharNum[last],extCharNum[c]),pairCount)
                last=c
    recv_pipe.close()
    print(time.clock())
    return pairCount

if __name__ == '__main__':
    pairCount,pairCountList={(-2,-1):0,(-1,-1):0},[]
    extPairCount,extPairCountList={},[]
    pool=multiprocessing.Pool(processes=8)
    for fn in os.listdir(trainSetPath):
        rp,sp=multiprocessing.Pipe(False)
        pairCountList.append(pool.apply_async(func=mapper,args=(fn,sp)))
        extPairCountList.append(pool.apply_async(func=post_mapper,args=(rp,)))
    pool.close();pool.join()

    for pc in pairCountList:
        for a,b in pc.get().items():
            _add_val(a,pairCount,b)
    with open("model.data","wb") as fout: pickle.dump(pairCount,fout)

    for pc in extPairCountList:
        for a,b in pc.get().items():
            _add_val(a,extPairCount,b)
    with open("multi.data","wb") as fout: pickle.dump(extPairCount,fout)
