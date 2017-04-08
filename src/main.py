import sys
from pinyin import pinyin2str

if len(sys.argv)==1:
    while True:
        try: s=input()
        except: break
        else: print(pinyin2str(s))
elif len(sys.argv)==3:
    with open(sys.argv[1],"r") as fin , open(sys.argv[2],"w") as fout:
        for line in fin:
            print(pinyin2str(line),file=fout)
else:
    print("Usage : pinyin")
    print("    or: pinyin input_file output_file")
