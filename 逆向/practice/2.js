/*
 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
 * Digest Algorithm, as defined in RFC 1321.
 * Version 2.1 Copyright (C) Paul Johnston 1999 - 2002.
 * Other contributors: Greg Holt, Andrew Kepert, Ydnar, Lostinet
 * Distributed under the BSD License
 * See http://pajhome.org.uk/crypt/md5 for more info.
 */

/*
 * Configurable variables. You may need to tweak these to be compatible with
 * the server-side, but the defaults work in most cases.
 */



var hexcase = 0;  /* hex output format. 0 - lowercase; 1 - uppercase        */
var b64pad  = ""; /* base-64 pad character. "=" for strict RFC compliance   */
var chrsz   = 8;  /* bits per input character. 8 - ASCII; 16 - Unicode      */

/*
 * These are the functions you'll usually want to call
 * They take string arguments and return either hex or base-64 encoded strings
 */
function hex_md5(s){ return binl2hex(core_md5(str2binl(s), s.length * chrsz));}
function b64_md5(s){ return binl2b64(core_md5(str2binl(s), s.length * chrsz));}
function str_md5(s){ return binl2str(core_md5(str2binl(s), s.length * chrsz));}
function hex_hmac_md5(key, data) { return binl2hex(core_hmac_md5(key, data)); }
function b64_hmac_md5(key, data) { return binl2b64(core_hmac_md5(key, data)); }
function str_hmac_md5(key, data) { return binl2str(core_hmac_md5(key, data)); }

/*
 * Perform a simple self-test to see if the VM is working
 */
function md5_vm_test()
{
  return hex_md5("abc") == "900150983cd24fb0d6963f7d28e17f72";
}

/*
 * Calculate the MD5 of an array of little-endian words, and a bit length
 */
function core_md5(x, len)
{
  /* append padding */
  x[len >> 5] |= 0x80 << ((len) % 32);
  x[(((len + 64) >>> 9) << 4) + 14] = len;

  var a =  1732584193;
  var b = -271733879;
  var c = -1732584194;
  var d =  271733878;

  for(var i = 0; i < x.length; i += 16)
  {
    var olda = a;
    var oldb = b;
    var oldc = c;
    var oldd = d;

    a = md5_ff(a, b, c, d, x[i+ 0], 7 , -680876936);
    d = md5_ff(d, a, b, c, x[i+ 1], 12, -389564586);
    c = md5_ff(c, d, a, b, x[i+ 2], 17,  606105819);
    b = md5_ff(b, c, d, a, x[i+ 3], 22, -1044525330);
    a = md5_ff(a, b, c, d, x[i+ 4], 7 , -176418897);
    d = md5_ff(d, a, b, c, x[i+ 5], 12,  1200080426);
    c = md5_ff(c, d, a, b, x[i+ 6], 17, -1473231341);
    b = md5_ff(b, c, d, a, x[i+ 7], 22, -45705983);
    a = md5_ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
    d = md5_ff(d, a, b, c, x[i+ 9], 12, -1958414417);
    c = md5_ff(c, d, a, b, x[i+10], 17, -42063);
    b = md5_ff(b, c, d, a, x[i+11], 22, -1990404162);
    a = md5_ff(a, b, c, d, x[i+12], 7 ,  1804603682);
    d = md5_ff(d, a, b, c, x[i+13], 12, -40341101);
    c = md5_ff(c, d, a, b, x[i+14], 17, -1502002290);
    b = md5_ff(b, c, d, a, x[i+15], 22,  1236535329);

    a = md5_gg(a, b, c, d, x[i+ 1], 5 , -165796510);
    d = md5_gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
    c = md5_gg(c, d, a, b, x[i+11], 14,  643717713);
    b = md5_gg(b, c, d, a, x[i+ 0], 20, -373897302);
    a = md5_gg(a, b, c, d, x[i+ 5], 5 , -701558691);
    d = md5_gg(d, a, b, c, x[i+10], 9 ,  38016083);
    c = md5_gg(c, d, a, b, x[i+15], 14, -660478335);
    b = md5_gg(b, c, d, a, x[i+ 4], 20, -405537848);
    a = md5_gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
    d = md5_gg(d, a, b, c, x[i+14], 9 , -1019803690);
    c = md5_gg(c, d, a, b, x[i+ 3], 14, -187363961);
    b = md5_gg(b, c, d, a, x[i+ 8], 20,  1163531501);
    a = md5_gg(a, b, c, d, x[i+13], 5 , -1444681467);
    d = md5_gg(d, a, b, c, x[i+ 2], 9 , -51403784);
    c = md5_gg(c, d, a, b, x[i+ 7], 14,  1735328473);
    b = md5_gg(b, c, d, a, x[i+12], 20, -1926607734);

    a = md5_hh(a, b, c, d, x[i+ 5], 4 , -378558);
    d = md5_hh(d, a, b, c, x[i+ 8], 11, -2022574463);
    c = md5_hh(c, d, a, b, x[i+11], 16,  1839030562);
    b = md5_hh(b, c, d, a, x[i+14], 23, -35309556);
    a = md5_hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
    d = md5_hh(d, a, b, c, x[i+ 4], 11,  1272893353);
    c = md5_hh(c, d, a, b, x[i+ 7], 16, -155497632);
    b = md5_hh(b, c, d, a, x[i+10], 23, -1094730640);
    a = md5_hh(a, b, c, d, x[i+13], 4 ,  681279174);
    d = md5_hh(d, a, b, c, x[i+ 0], 11, -358537222);
    c = md5_hh(c, d, a, b, x[i+ 3], 16, -722521979);
    b = md5_hh(b, c, d, a, x[i+ 6], 23,  76029189);
    a = md5_hh(a, b, c, d, x[i+ 9], 4 , -640364487);
    d = md5_hh(d, a, b, c, x[i+12], 11, -421815835);
    c = md5_hh(c, d, a, b, x[i+15], 16,  530742520);
    b = md5_hh(b, c, d, a, x[i+ 2], 23, -995338651);

    a = md5_ii(a, b, c, d, x[i+ 0], 6 , -198630844);
    d = md5_ii(d, a, b, c, x[i+ 7], 10,  1126891415);
    c = md5_ii(c, d, a, b, x[i+14], 15, -1416354905);
    b = md5_ii(b, c, d, a, x[i+ 5], 21, -57434055);
    a = md5_ii(a, b, c, d, x[i+12], 6 ,  1700485571);
    d = md5_ii(d, a, b, c, x[i+ 3], 10, -1894986606);
    c = md5_ii(c, d, a, b, x[i+10], 15, -1051523);
    b = md5_ii(b, c, d, a, x[i+ 1], 21, -2054922799);
    a = md5_ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
    d = md5_ii(d, a, b, c, x[i+15], 10, -30611744);
    c = md5_ii(c, d, a, b, x[i+ 6], 15, -1560198380);
    b = md5_ii(b, c, d, a, x[i+13], 21,  1309151649);
    a = md5_ii(a, b, c, d, x[i+ 4], 6 , -145523070);
    d = md5_ii(d, a, b, c, x[i+11], 10, -1120210379);
    c = md5_ii(c, d, a, b, x[i+ 2], 15,  718787259);
    b = md5_ii(b, c, d, a, x[i+ 9], 21, -343485551);

    a = safe_add(a, olda);
    b = safe_add(b, oldb);
    c = safe_add(c, oldc);
    d = safe_add(d, oldd);
  }
  return Array(a, b, c, d);

}

/*
 * These functions implement the four basic operations the algorithm uses.
 */
function md5_cmn(q, a, b, x, s, t)
{
  return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s),b);
}
function md5_ff(a, b, c, d, x, s, t)
{
  return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t);
}
function md5_gg(a, b, c, d, x, s, t)
{
  return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t);
}
function md5_hh(a, b, c, d, x, s, t)
{
  return md5_cmn(b ^ c ^ d, a, b, x, s, t);
}
function md5_ii(a, b, c, d, x, s, t)
{
  return md5_cmn(c ^ (b | (~d)), a, b, x, s, t);
}

/*
 * Calculate the HMAC-MD5, of a key and some data
 */
function core_hmac_md5(key, data)
{
  var bkey = str2binl(key);
  if(bkey.length > 16) bkey = core_md5(bkey, key.length * chrsz);

  var ipad = Array(16), opad = Array(16);
  for(var i = 0; i < 16; i++)
  {
    ipad[i] = bkey[i] ^ 0x36363636;
    opad[i] = bkey[i] ^ 0x5C5C5C5C;
  }

  var hash = core_md5(ipad.concat(str2binl(data)), 512 + data.length * chrsz);
  return core_md5(opad.concat(hash), 512 + 128);
}

/*
 * Add integers, wrapping at 2^32. This uses 16-bit operations internally
 * to work around bugs in some JS interpreters.
 */
function safe_add(x, y)
{
  var lsw = (x & 0xFFFF) + (y & 0xFFFF);
  var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
  return (msw << 16) | (lsw & 0xFFFF);
}

/*
 * Bitwise rotate a 32-bit number to the left.
 */
function bit_rol(num, cnt)
{
  return (num << cnt) | (num >>> (32 - cnt));
}

/*
 * Convert a string to an array of little-endian words
 * If chrsz is ASCII, characters >255 have their hi-byte silently ignored.
 */
function str2binl(str)
{
  var bin = Array();
  var mask = (1 << chrsz) - 1;
  for(var i = 0; i < str.length * chrsz; i += chrsz)
    bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (i%32);
  return bin;
}

/*
 * Convert an array of little-endian words to a string
 */
function binl2str(bin)
{
  var str = "";
  var mask = (1 << chrsz) - 1;
  for(var i = 0; i < bin.length * 32; i += chrsz)
    str += String.fromCharCode((bin[i>>5] >>> (i % 32)) & mask);
  return str;
}
// window.url = '/api/match/15';
// fetch('/static/match/match15/main.wasm').then(response =>
//     response.arrayBuffer()
// ).then(bytes => WebAssembly.instantiate(bytes)).then(results => {
//     instance = results.instance;
//     window.q = instance.exports.encode;
//     window.m = function (){
//         t1 = Date.parse(new Date())/1000/2;
//         t2 = Date.parse(new Date())/1000/2 - Math.floor(Math.random() * (50) + 1);
//         return window.q(t1, t2).toString() + '|' + t1 + '|' + t2;
//     }
//     window.finish = true;
// }).catch(console.error);
/*
 * Convert an array of little-endian words to a hex string.
 */
function binl2hex(binarray)
{
  var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
  var str = "";
  for(var i = 0; i < binarray.length * 4; i++)
  {
    str += hex_tab.charAt((binarray[i>>2] >> ((i%4)*8+4)) & 0xF) +
           hex_tab.charAt((binarray[i>>2] >> ((i%4)*8  )) & 0xF);
  }
  return str;
}

/*
 * Convert an array of little-endian words to a base-64 string
 */
function binl2b64(binarray)
{
  var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  var str = "";
  for(var i = 0; i < binarray.length * 4; i += 3)
  {
    var triplet = (((binarray[i   >> 2] >> 8 * ( i   %4)) & 0xFF) << 16)
                | (((binarray[i+1 >> 2] >> 8 * ((i+1)%4)) & 0xFF) << 8 )
                |  ((binarray[i+2 >> 2] >> 8 * ((i+2)%4)) & 0xFF);
    for(var j = 0; j < 4; j++)
    {
      if(i * 8 + j * 6 > binarray.length * 32) str += b64pad;
      else str += tab.charAt((triplet >> 6*(3-j)) & 0x3F);
    }
  }
  return str;
}






var _$oa = ['eEJqWFE=', 'QmlBYk0=', 'YWxlU1Q=', 'eUpyYlU=', 'blR3TmE=', 'anlMSmY=', 'bFNxUEM=', 'cE5uUlU=', 'QndhZHQ=', 'WlFpVEk=', 'YWN0aW9u', 'alByQ3M=', 'YlJUbWM=', 'ZHFyblE=', 'cm91bmQ=', 'aW5wdXQ=', 'Z0ZLclk=', 'U1VHd1c=', 'SndGQU0=', 'dk9pWXY=', 'SFNxZHQ=', 'bGdUaVo=', 'WHd0VVk=', 'WWVMRXg=', 'Y2FsbA==', 'aVpWT0Y=', 'SXJRcGg=', 'VVNpQ0I=', 'bFB6clA=', 'YnRvYQ==', 'bXFxWmw=', 'Z2dlcg==', '5q2k572R6aG15Y+X44CQ54ix6ZSt5LqR55u+IFYxLjAg5Yqo5oCB54mI44CR5L+d5oqk', 'dmhGU2E=', 'Vld0aGw=', 'Y2hhaW4=', 'QlBxcng=', 'TVlIWm8=', 'OyBwYXRoPS8=', 'WEppTmU=', 'T1Z4WkI=', 'aEFPVXQ=', 'dEVSRUU=', 'RGtFSFU=', 'bElkS1A=', 'c3RhdGVPYmplY3Q=', 'UFloT28=', 'ZGVidQ==', 'WXpram8=', 'a2lDVEE=', 'YXBwbHk=', 'RmpYVWo=', 'UUVwYlA=', 'QVJHQ1I=', 'ckRXbnY=', 'Y291bnRlcg==', 'bHpVUGs=', 'XCtcKyAqKD86W2EtekEtWl8kXVswLTlhLXpBLVpfJF0qKQ==', 'ZnVuY3Rpb24gKlwoICpcKQ==', 'UXh0RW8=', 'WldaYW8=', 'QlpQWm4=', 'UlNPQkQ=', 'd1dqQm8=', 'Y0dTSGY=', 'c0lFZk8=', 'ZWtiUGo=', 'b2VMTnk=', 'VGJhUVg=', 'VWZDZVk=', 'VEhiZ24=', 'Y29uc3RydWN0b3I=', 'QldBZkc=', 'bndrTXY=', 'RklDWlY=', 'ckVNUmM=', 'aW5pdA==', 'c3RyaW5n', 'bG9n', 'd1dtZkI=', 'V1hMbUs=', 'TmlTYXg=', 'dGVzdA==', 'SHJXZkc=', 'b2lpa0M=', 'SGtqWHg=', 'YnNDZlc=', 'cmVsb2Fk', 'Y29va2ll', 'VXlDZWU='];
(function (a, b) {
    var c = function (f) {
        while (--f) {
            a['push'](a['shift']());
        }
    };
    c(++b);
}(_$oa, 0x16e));
var _$ob = function (a, b) {
    a = a - 0x0;
    var c = _$oa[a];
    if (_$ob['aaAsFd'] === undefined) {
        (function () {
            var f;
            try {
                var h = Function('return\x20(function()\x20' + '{}.constructor(\x22return\x20this\x22)(\x20)' + ');');
                f = h();
            } catch (i) {
                f = window;
            }
            var g = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
            f['atob'] || (f['atob'] = function (j) {
                    var k = String(j)['replace'](/=+$/, '');
                    var l = '';
                    for (var m = 0x0, n, o, p = 0x0; o = k['charAt'](p++); ~o && (n = m % 0x4 ? n * 0x40 + o : o,
                    m++ % 0x4) ? l += String['fromCharCode'](0xff & n >> (-0x2 * m & 0x6)) : 0x0) {
                        o = g['indexOf'](o);
                    }
                    return l;
                }
            );
        }());
        _$ob['ZUYcvb'] = function (e) {
            var f = atob(e);
            var g = [];
            for (var h = 0x0, j = f['length']; h < j; h++) {
                g += '%' + ('00' + f['charCodeAt'](h)['toString'](0x10))['slice'](-0x2);
            }
            return decodeURIComponent(g);
        }
        ;
        _$ob['NHmghc'] = {};
        _$ob['aaAsFd'] = !![];
    }
    var d = _$ob['NHmghc'][a];
    if (d === undefined) {
        c = _$ob['ZUYcvb'](c);
        _$ob['NHmghc'][a] = c;
    } else {
        c = d;
    }
    return c;
};
(function () {
    var a = {
        'IrQph': function (d, e) {
            return d(e);
        },
        'bRTmc': function (d, e) {
            return d === e;
        },
        'SeMFr': 'sVKuZ',
        'wWmfB': _$ob('0x3f'),
        'ekbPj': function (d, e) {
            return d + e;
        },
        'QxtEo': _$ob('0x29'),
        'tEREE': 'gger',
        'rEMRc': _$ob('0x4'),
        'pNnRU': _$ob('0x34'),
        'VWthl': _$ob('0x33'),
        'lgTiZ': function (d, e) {
            return d(e);
        },
        'XJiNe': _$ob('0x46'),
        'bbImu': _$ob('0x1d'),
        'XwtUY': _$ob('0x9'),
        'cGSHf': function (d, e) {
            return d === e;
        },
        'oeLNy': _$ob('0x59'),
        'DkEHU': 'NMBhQ',
        'SUGwW': function (d) {
            return d();
        },
        'kiCTA': function (d, e) {
            return d !== e;
        },
        'yJrbU': 'IMnys',
        'UyCee': _$ob('0x55'),
        'tTLzz': function (d, e, f) {
            return d(e, f);
        },
        'MYHZo': _$ob('0x1a'),
        'aleST': 'aiding_win',
        'QEpbP': function (d, e) {
            return d(e);
        },
        'lzUPk': function (d, e) {
            return d(e);
        },
        'WjLRx': function (d, e) {
            return d / e;
        },
        'WXLmK': function (d, e) {
            return d + e;
        },
        'RAzZo': function (d, e) {
            return d + e;
        },
        'sIEfO': function (d, e) {
            return d + e;
        },
        'hAOUt': function (d, e) {
            return d + e;
        },
        'ZQiTI': function (d, e) {
            return d + e;
        },
        'xBjXQ': function (d, e) {
            return d + e;
        },
        'PYhOo': 'sign=',
        'qHjVM': function (d, e) {
            return d / e;
        },
        'BWAfG': _$ob('0x20')
    };
    var b = function () {
        var d = {
            'cMHaB': function (f, g) {
                return a[_$ob('0x3c')](f, g);
            },
            'NiSax': a[_$ob('0x35')],
            'jPrCs': a[_$ob('0x24')],
            'Bwadt': a[_$ob('0x45')]
        };
        var e = !![];
        return function (f, g) {
            var h = {
                'vjcjt': function (j, k) {
                    return a[_$ob('0x14')](j, k);
                },
                'NmBtF': function (j, k) {
                    return a['bRTmc'](j, k);
                },
                'mqqZl': a['SeMFr']
            };
            if (a[_$ob('0x6')](a['wWmfB'], a[_$ob('0x49')])) {
                var i = e ? function () {
                        if (h['NmBtF'](h['mqqZl'], h[_$ob('0x18')])) {
                            if (g) {
                                var j = g['apply'](f, arguments);
                                g = null;
                                return j;
                            }
                        } else {
                            UNIjpx['vjcjt'](debuggerProtection, 0x0);
                        }
                    }
                    : function () {
                    }
                ;
                e = ![];
                return i;
            } else {
                (function () {
                    return !![];
                }
                    [_$ob('0x41')](YcrGcE['cMHaB'](YcrGcE[_$ob('0x4b')], YcrGcE[_$ob('0x5')]))['call'](YcrGcE[_$ob('0x2')]));
            }
        }
            ;
    }();
    (function () {
        if (a[_$ob('0x2b')](a[_$ob('0x57')], a[_$ob('0x53')])) {
            a['tTLzz'](b, this, function () {
                var d = new RegExp(a[_$ob('0x1')]);
                var e = new RegExp(a[_$ob('0x1c')], 'i');
                var f = a['lgTiZ'](_$oc, a[_$ob('0x21')]);
                if (!d[_$ob('0x4c')](a[_$ob('0x3c')](f, a['bbImu'])) || !e['test'](a[_$ob('0x3c')](f, a[_$ob('0x10')]))) {
                    if (a[_$ob('0x3a')](a[_$ob('0x3d')], a[_$ob('0x25')])) {
                        if (fn) {
                            var h = fn[_$ob('0x2c')](context, arguments);
                            fn = null;
                            return h;
                        }
                    } else {
                        a['lgTiZ'](f, '0');
                    }
                } else {
                    a[_$ob('0xb')](_$oc);
                }
            })();
        } else {
            return !![];
        }
    }());
    // console[_$ob('0x48')](a[_$ob('0x1f')]);
    console.log(_$ob('0x17'));  //btoa
    console.log(a[_$ob('0x3c')]);  //[Function: ekbPj]
    console.log(a[_$ob('0x56')]);  //aiding_win
    console.log(a[_$ob('0xf')]);   //[Function: lgTiZ]
    var c = new Date()['valueOf']();
    console.log(c)
    // token = window['btoa'](a[_$ob('0x3c')](a[_$ob('0x56')], a[_$ob('0xf')](String, '1587102734000')));
    // md = a[_$ob('0x2e')](hex_md5, window['btoa'](a[_$ob('0x3c')](a[_$ob('0x56')], a[_$ob('0x32')](String, Math[_$ob('0x8')](a['WjLRx'](c, 0x3e8))))));
    // document[_$ob('0x52')] = a[_$ob('0x4a')](a['RAzZo'](a[_$ob('0x3b')](a[_$ob('0x23')](a[_$ob('0x3')](a[_$ob('0x54')](a[_$ob('0x28')], Math[_$ob('0x8')](a['qHjVM'](c, 0x3e8))), '~'), token), '|'), md), a[_$ob('0x42')]);
    // location[_$ob('0x51')]();
}());

function _$oc(a) {
    var b = {
        'vhFSa': 'function\x20*\x5c(\x20*\x5c)',
        'lIdKP': _$ob('0x33'),
        'vOiYv': function (d, e) {
            return d(e);
        },
        'HrWfG': _$ob('0x46'),
        'hOdzq': function (d, e) {
            return d + e;
        },
        'aKUfx': _$ob('0x1d'),
        'ExLkb': _$ob('0x9'),
        'RSOBD': function (d) {
            return d();
        },
        'AWuqB': function (d, e) {
            return d === e;
        },
        'nTwNa': _$ob('0x47'),
        'QHqzA': 'while\x20(true)\x20{}',
        'USiCB': _$ob('0x31'),
        'ZWZao': function (d, e) {
            return d === e;
        },
        'BZPZn': _$ob('0x40'),
        'YeLEx': function (d, e) {
            return d !== e;
        },
        'kQMCT': function (d, e) {
            return d / e;
        },
        'ARGCR': 'length',
        'JwFAM': function (d, e) {
            return d % e;
        },
        'HSqdt': function (d, e) {
            return d + e;
        },
        'lSqPC': _$ob('0x29'),
        'rDWnv': _$ob('0x19'),
        'TbaQX': _$ob('0x4'),
        'Yzkjo': function (d, e) {
            return d + e;
        },
        'lPzrP': _$ob('0x27'),
        'iZVOF': function (d, e) {
            return d(e);
        },
        'HkjXx': function (d, e) {
            return d(e);
        },
        'vYHYy': 'pEEnH',
        'FICZV': function (d, e) {
            return d === e;
        },
        'bsCfW': _$ob('0xa')
    };

    function c(d) {
        var e = {
            'nwkMv': b[_$ob('0x1b')],
            'oiikC': b[_$ob('0x26')],
            'FjXUj': function (f, g) {
                return b[_$ob('0xd')](f, g);
            },
            'hiPPR': b[_$ob('0x4d')],
            'BPqrx': function (f, g) {
                return b['hOdzq'](f, g);
            },
            'BVBOk': b['aKUfx'],
            'dqrnQ': b['ExLkb'],
            'wWjBo': function (f, g) {
                return b[_$ob('0xd')](f, g);
            },
            'OVxZB': function (f) {
                return b[_$ob('0x38')](f);
            }
        };
        if (b['AWuqB'](typeof d, b[_$ob('0x58')])) {
            return function (f) {
            }
                ['constructor'](b['QHqzA'])[_$ob('0x2c')](b[_$ob('0x15')]);
        } else {
            if (b[_$ob('0x36')](b[_$ob('0x37')], b['BZPZn'])) {
                if (b[_$ob('0x11')](b['hOdzq']('', b['kQMCT'](d, d))[b[_$ob('0x2f')]], 0x1) || b[_$ob('0x36')](b[_$ob('0xc')](d, 0x14), 0x0)) {
                    (function () {
                        return !![];
                    }
                        [_$ob('0x41')](b[_$ob('0xe')](b[_$ob('0x0')], b[_$ob('0x30')]))[_$ob('0x12')](b[_$ob('0x3e')]));
                } else {
                    (function () {
                        return ![];
                    }
                        ['constructor'](b[_$ob('0x2a')](b[_$ob('0x0')], b[_$ob('0x30')]))['apply'](b[_$ob('0x16')]));
                }
            } else {
                var g = new RegExp(e[_$ob('0x43')]);
                var h = new RegExp(e[_$ob('0x4e')], 'i');
                var i = e[_$ob('0x2d')](_$oc, e['hiPPR']);
                if (!g[_$ob('0x4c')](e[_$ob('0x1e')](i, e['BVBOk'])) || !h[_$ob('0x4c')](e[_$ob('0x1e')](i, e[_$ob('0x7')]))) {
                    e[_$ob('0x39')](i, '0');
                } else {
                    e[_$ob('0x22')](_$oc);
                }
            }
        }
        b[_$ob('0x13')](c, ++d);
    }

    try {
        if (b[_$ob('0x36')](b['vYHYy'], b['vYHYy'])) {
            if (a) {
                return c;
            } else {
                if (b[_$ob('0x44')](b['bsCfW'], b[_$ob('0x50')])) {
                    b[_$ob('0x4f')](c, 0x0);
                } else {
                    b[_$ob('0x4f')](result, '0');
                }
            }
        } else {
            if (a) {
                return c;
            } else {
                b[_$ob('0x4f')](c, 0x0);
            }
        }
    } catch (f) {
    }
}

