#coding = utf-8
import sys,os
import copy
charList,charCount,charNum,charMap=[],0,{},{}
__workdir = '.' if os.path.dirname(sys.argv[0])=="" else os.path.dirname(sys.argv[0])
with open(__workdir+os.path.sep+"一二级汉字表.txt","r",encoding="gbk") as fin:
    charList=list(fin.readline().strip());
    for c in charList:
        charNum[c]=charCount
        charCount+=1

pinyinList,pinyinCount,pinyinNum,pinyinMap=[],0,{},{}
with open(__workdir+os.path.sep+"拼音汉字表.txt","r",encoding="gbk") as fin:
    for line in fin:
        t=line.strip().split()
        pinyinList.append(t[0])
        pinyinNum[t[0]]=pinyinCount
        pinyinMap[t[0]]=list(map(lambda x : charNum[x],t[1:]))
        for c in t[1:]:
            if not (c in charMap): charMap[c]=[]
            charMap[c].append(t[0])
        pinyinCount+=1

def num2char(sth):
    """
    num2char(int) -> char
    num2char(tuple /* of int */) -> str
    convert numbers to corresponding Chinese characters.
    """
    if isinstance(sth,int):
        return charList[sth]
    else:
        return "".join(map(lambda x : charList[x],sth))

def char2num(sth):
    """
    char2num(char) -> int
    char2num(str) -> tuple
    convert a string of Chinese characters to corresponding numbers.
    """
    if len(sth)==1:
        return charNum[sth]
    else:
        return tuple(map(lambda x : charNum[x],sth))

def num2pinyin(sth):
    """
    num2pinyin(int) -> str
    num2pinyin(tuple /*of int*/) -> tuple /*of str*/
    convert numbers to corresponding Pinyin.
    """
    if isinstance(sth,int):
        return pinyinList[sth]
    else:
        return tuple(map(lambda x : pinyinList[x],sth))

def pinyin2num(sth):
    """
    pinyin2num(str)-> int
    pinyin2num(tuple /*of str*/) -> tuple /*of int*/
    convert Pinyin to corresponding numbers.
    """
    if isinstance(sth,str):
        return pinyinNum[sth]
    else:
        return tuple(map(lambda x : pinyinNum[x],sth))

def isMulti(sth):
    return sth in charMap and len(charMap[sth])>1

def hasMulti(sth):
    return list(filter(lambda x : x in charMap and len(charMap[x])>1,sth)) != []

extCharList,extCharCount,extCharNum=[],0,{}
extCharList=copy.deepcopy(charList)
for c in charList:
    if isMulti(c):
        pos = charNum[c]
        extCharList[pos]+="_"+charMap[c][0]
        for tpy in charMap[c][1:]:
            extCharList.append(c+"_"+tpy)
extCharCount=len(extCharList)
for c in range(extCharCount):
    extCharNum[extCharList[c]]=c
