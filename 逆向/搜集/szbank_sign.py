# -*- coding: UTF-8 -*-
# @author: zhulw
# @file: szbank_sign
# @time: 2021-01-11
# @desc: rc4

from urllib.parse import quote


def rc4Encript(text, key):
    srcString = quote(quote(text, safe=":,"), safe=":,").replace("+", "%2B")
    refDataArray = rc4(strToOrd(srcString), strToOrd(key))
    return arrayToHex(refDataArray)


def rc4(refDataArray, keyArray):
    s, k = [], []
    for i in range(256):
        s.append(i)
        k.append(keyArray[i % len(keyArray)])
    j = 0
    for i in range(256):
        j = (j + s[i] + k[i]) % 256
        swap = s[i]
        s[i] = s[j]
        s[j] = swap
    i, j = 0, 0
    for x in range(len(refDataArray)):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        swap = s[i]
        s[i] = s[j]
        s[j] = swap
        xor = (s[i] + s[j]) % 256
        refDataArray[x] ^= s[xor]
    return refDataArray


def strToOrd(text: str) -> list:
    return [ord(x) for x in text]


def arrayToHex(array: list) -> str:
    resultStr = ""
    for i in array:
        resultStr += "0" + format(i, "x") if len(format(i, "x")) < 2 else format(i, "x")
    return resultStr


if __name__ == '__main__':
    tt = '{"format":"JSON","submitTimestamp":1610350796229,"language":"ZH_CN","Math":0.07119711193147626}'
    kk = "f8Pnc21Av25X-8kAN4P-rMGBcz8a5BgFir-PyBblIxE"
    result = rc4Encript(tt, kk)
    print(result)
