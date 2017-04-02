from codecvt import *
from functools import reduce
from math import log
import pickle

### model loading ###

with open("model.data","rb") as fin: model = pickle.load(fin)
with open("multi.data","rb") as fin: multi = pickle.load(fin)
multi_tc={}

def _add_val(_key,_dict,_delta=1):
    if _key in _dict: _dict[_key]+=_delta
    else:  _dict[_key]=_delta

def _update(_dict,_key,_value):
    if _key in _dict and _value[0]>_dict[_key][0] or not _key in _dict: _dict[_key]=_value

for a,b in multi.items():
    _add_val((a[0],char2num(extCharList[a[1]].split("_")[0])),multi_tc,b)

### model smoothing ###

def _model_smooth():
    pass

_model_smooth()

print("model loaded.")

### Viterbi algorithm ###
def _calc_res(lc,lr,cc,tc):
    if tc==-1: # NORMAL
        if lc==-1 or not len(extCharList[lc])>1:
            return (lr[0] + (float("-inf") if not (lc,cc) in model else log(model[lc,cc])-log(model[-2,lc])),lr[1]+charList[cc])
        else:
            _lc=charNum[extCharList[lc].split("_")[0]]
            return (lr[0] + (float("-inf") if not (_lc,cc) in model or not (lc,cc) in multi else log(model[_lc,cc])-log(model[-2,_lc])+log(multi[lc,cc])-log(multi_tc[lc,cc])),\
                    lr[1]+charList[cc])
    else: # with modification
        if lc==-1 or not len(extCharList[lc])>1:
            return (lr[0] + (float("-inf") if not (lc,cc) in model or not (lc,tc) in multi else log(model[lc,cc])-log(model[-2,cc])+log(multi[lc,tc])-log(multi_tc[lc,cc])),\
                    lr[1]+charList[cc])
        else:
            _lc=charNum[extCharList[lc].split("_")[0]]
            return (lr[0] + (float("-inf") if not (_lc,cc) in model or not (lc,tc) in multi else log(model[_lc,cc])-log(model[-2,_lc])+log(multi[lc,tc])-log(multi_tc[lc,cc])),\
                    lr[1]+charList[cc])

def _calc_res__(lc,lr,cc,tc):
    if lc!=-1 and len(extCharList[lc])>1: lc=charNum[extCharList[lc].split("_")[0]]
    return (lr[0] * (0 if not (lc,cc) in model else model[lc,cc]/model[-2,lc]),lr[1]+charList[cc])

def pinyin2str(sth):
    dp={-1:(0.,"")}
    for cp in sth.split():
        current={}
        for cc in pinyinMap[cp]:
            if isMulti(num2char(cc)): tc=extCharNum[num2char(cc)+"_"+cp]
            else: tc=-1
            for lc,lr in dp.items():
                tr=_calc_res(lc,lr,cc,tc)
                if tr[0]!=float("-inf"):
                    _update(current,max(tc,cc),tr)
        dp=current
    return reduce(lambda a,b: a if a[0]>b[0] else b,dp.values())

if __name__ == '__main__':
    while True:
        print(pinyin2str(input()))
