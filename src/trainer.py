from codecvt import *
import pypinyin,json,time,multiprocessing,re
import os
import random,pickle
import tempfile

trainSetPath="train_set"

puncs = re.compile(r"\s|\.|\(|\)|"+"|".join(["，","。","、","：","；","？","！","（","）","《","》",
                         "-","——","·","……","‘","’","“","”","/","\\[","\\]","【","】","\\|","℃"]))

def pre_process():
    pass

def _add_val(_key,_dict,_delta=1):
    if _key in _dict: _dict[_key]+=_delta
    else:  _dict[_key]=_delta

def mapper(file_name,dump_dir):
    pairCount={(-2,-1):0,(-1,-1):0}
    dump_file=open(dump_dir+os.path.sep+file_name,"w",encoding="utf-8")

    def analyse(context):
        lc=list(puncs.split(context))
        tt="\n".join(filter(lambda x : len(x)>1 and random.uniform(0,1)<0.01 and hasMulti(x),lc))
        if tt!="": print(tt,file=dump_file)
        for cl in lc:
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

    print("processing ",file_name,"... Start time: ", time.clock())
    with open(trainSetPath+os.path.sep+file_name,"r",encoding="utf-8") as fin:
        for line in fin:
            ld=json.loads(line)
            analyse(ld["title"])
            analyse(ld["html"])
    print(file_name," done. End time: ", time.clock())
    dump_file.close()
    return pairCount

if __name__ == '__main__':
    pairCount,pairCountList={(-2,-1):0,(-1,-1):0},[]
    #with tempfile.TemporaryDirectory(dir=".") as tempdir:
    def main():
        tempdir="tmp_train"
        pool=multiprocessing.Pool()
        #for fn in os.listdir(trainSetPath):
        #    pairCountList.append(pool.apply_async(\
        #            func=mapper,args=(fn,tempdir)))
        fn = "2016-11.txt"
        pairCountList.append(pool.apply_async(func=mapper,args=(fn,tempdir)))
        pool.close()
        pool.join()

        for pc in pairCountList:
            for a,b in pc.get().items():
                _add_val(a,pairCount,b)
        with open("model.data","wb") as fout: pickle.dump(pairCount,fout)
    main()
