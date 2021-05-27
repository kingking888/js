# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/5/26
# @File     : shanghairanking.py
# @Software : PyCharm
# SHA256

import hashlib

import ctypes


def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def unsigned_right_shift(n, i):
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    # print(n)
    return int_overflow(n >> i)


def _parse(string_code: str):
    i = 0
    n = {}
    while i < len(string_code):
        if not n.get(unsigned_right_shift(i, 2)):
            n[unsigned_right_shift(i, 2)] = 0
        n[unsigned_right_shift(i, 2)] |= (255 & ord(string_code[i])) << 24 - i % 4 * 8
        i += 1
    return n, n.values(), len(string_code)


def _x(t, i):
    _index = unsigned_right_shift(i, 2)
    try:
        val = t[_index]
    except:
        val = 0
    finally_val = unsigned_right_shift(val, 24 - i % 4 * 8)
    return finally_val


def stringify(string_code: str):
    t, _t, n = _parse(string_code)
    _map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    r = []
    i = 0
    while i < n:
        c = 0
        while c < 4 and i + 0.75 * c < n:
            o = (_x(t, i) & 255) << 16 | (_x(t, i + 1) & 255) << 8 | _x(t, i + 2) & 255
            r.append(_map[unsigned_right_shift(o, 6 * (3 - c)) & 63])
            c += 1
        i += 3
    l = _map[64]
    if l:
        r.append(l)
    return "".join(r)


if __name__ == "__main__":
    s = hashlib.sha256()  # Get the hash algorithm.
    s.update(
        "3#67611e7d-9144-4893-a737-0ca577012646#GET /v2010/user_ident #1621938561740".encode("utf8"))  # Hash the data.
    b = s.hexdigest()  # Get he hash value.
    # print(b)
    print(stringify("3:51d67f75787cea608105bca60c915a1311db25eba7c9edec126ce2bc585482d1:1621938561740"))

"51d67f75787cea608105bca60c915a1311db25eba7c9edec126ce2bc585482d1"

"3:51d67f75787cea608105bca60c915a1311db25eba7c9edec126ce2bc585482d1:1621938561740"
