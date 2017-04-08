# pinyin 4 IAI
#### 拼音输入法编程作业

----

## 算法
- 使用基于字的二元模型的Viterbi算法。
- 对低频组合采用了线性插值。
- 对多音字进行了额外的修正。

## 使用
- 本程序仅支持python3。
- 对windows平台进行了代码打包，直接使用bin/pinyin.exe即可，无须安装python3环境。
- 对于其他平台，直接使用src/pinyin.py。
- 具体用法：

        Usage : pinyin
            or: pinyin input_file output_file

  前者为从stdin逐行读入拼音串，向stdout输出汉字串；后者从input_file逐行读入拼音串，向output_file输出。
- 注意！本程序并没有对拼音串的合法性进行检查，因此当输入的拼音串不合法时会直接抛出异常使程序结束。

## 协议
- 本程序使用了MIT License。
