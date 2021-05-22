# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/4/10
# @File     : yhz566.py
# @Software : PyCharm
"""
登录过程:访问页面html获取参数vvccookie,输入验证码code为MD5加密,
var public_key = "B0AAFA4C9D388208E9F55B14DF04C8603D0CD81B7B65BBD669FA893096C985E33682FE7DEEE6500E1C4C6722C9855B6DD2E130F3672BEBA446B72D8DFFF2DD1F4E23D6BD728E267A9DC2C544C6680712884926D67AF74B74E5AD8298034D8C16FE8E5A37706EF5E447E423E69CA7FD3E47BBF7A9B137EF9B0310E2560E13D3C1";
var public_length = "10001";
function rsa_encrypt(str) {
    var BLOCK_SIZE = public_key.length / 2 - 11;
    var ret = '';
    while (str.length > 0) {
        var i = BLOCK_SIZE;
        if (str.length < i)
            i = str.length;
        str_1 = str.substr(0, i);
        str = str.substr(i, str.length - i);
        ret += rsa_encrypt1(str_1) + ' ';
    }
    return (ret);
}
function rsa_encrypt1(str) {
    var rsa = new RSAKey();
    rsa.setPublic(public_key, public_length);
    var res = rsa.encrypt(str);
    res = hex2b64(res);
    return (res);
}

"""
import hashlib

url = 'http://yhz566.com/'


def hl_md5(imei):
    new_md5 = hashlib.md5()
    new_md5.update(imei.encode(encoding='utf-8'))
    return new_md5.hexdigest()





