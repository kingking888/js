var j4n = {};
var od8V = 8;
var bdr4v = function (hr6l, cs4w) {
    return hr6l << cs4w | hr6l >>> 32 - cs4w
};
var VC2x = function () {
    var bZO2x = "0123456789abcdef"
        , IL8D = function (i) {
        return i % 4
    }
        , IM8E = function (i) {
        return 3 - i % 4
    };
    return function (iO7H, IN8F) {
        var bu4y = []
            , mF8x = IN8F ? IL8D : IM8E;
        for (var i = 0, l = iO7H.length * 4; i < l; i++) {
            bu4y.push(bZO2x.charAt(iO7H[i >> 2] >> mF8x(i) * 8 + 4 & 15) + bZO2x.charAt(iO7H[i >> 2] >> mF8x(i) * 8 & 15))
        }
        return bu4y.join("")
    }
}();
var mE8w = function (x, y) {
    var bZm2x = (x & 65535) + (y & 65535)
        , cEB7u = (x >> 16) + (y >> 16) + (bZm2x >> 16);
    return cEB7u << 16 | bZm2x & 65535
};
var bdn4r = function (q, a, b, x, s, t) {
    return mE8w(bdr4v(mE8w(mE8w(a, q), mE8w(x, t)), s), b)
};
var pX9O = function (a, b, c, d, x, s, t) {
    return bdn4r(b & d | c & ~d, a, b, x, s, t)
};
var pH9y = function (a, b, c, d, x, s, t) {
    return bdn4r(b ^ c ^ d, a, b, x, s, t)
};
var qa9R = function (a, b, c, d, x, s, t) {
    return bdn4r(b & c | ~b & d, a, b, x, s, t)
};
var pA9r = function (a, b, c, d, x, s, t) {
    return bdn4r(c ^ (b | ~d), a, b, x, s, t)
};
var LV9M = function (x, y) {
    x[y >> 5] |= 128 << y % 32;
    x[(y + 64 >>> 9 << 4) + 14] = y;
    var a = 1732584193
        , b = -271733879
        , c = -1732584194
        , d = 271733878;
    for (var i = 0, l = x.length, cac2x, cad2x, cag2x, cam2x; i < l; i += 16) {
        cac2x = a;
        cad2x = b;
        cag2x = c;
        cam2x = d;
        a = qa9R(a, b, c, d, x[i + 0], 7, -680876936);
        d = qa9R(d, a, b, c, x[i + 1], 12, -389564586);
        c = qa9R(c, d, a, b, x[i + 2], 17, 606105819);
        b = qa9R(b, c, d, a, x[i + 3], 22, -1044525330);
        a = qa9R(a, b, c, d, x[i + 4], 7, -176418897);
        d = qa9R(d, a, b, c, x[i + 5], 12, 1200080426);
        c = qa9R(c, d, a, b, x[i + 6], 17, -1473231341);
        b = qa9R(b, c, d, a, x[i + 7], 22, -45705983);
        a = qa9R(a, b, c, d, x[i + 8], 7, 1770035416);
        d = qa9R(d, a, b, c, x[i + 9], 12, -1958414417);
        c = qa9R(c, d, a, b, x[i + 10], 17, -42063);
        b = qa9R(b, c, d, a, x[i + 11], 22, -1990404162);
        a = qa9R(a, b, c, d, x[i + 12], 7, 1804603682);
        d = qa9R(d, a, b, c, x[i + 13], 12, -40341101);
        c = qa9R(c, d, a, b, x[i + 14], 17, -1502002290);
        b = qa9R(b, c, d, a, x[i + 15], 22, 1236535329);
        a = pX9O(a, b, c, d, x[i + 1], 5, -165796510);
        d = pX9O(d, a, b, c, x[i + 6], 9, -1069501632);
        c = pX9O(c, d, a, b, x[i + 11], 14, 643717713);
        b = pX9O(b, c, d, a, x[i + 0], 20, -373897302);
        a = pX9O(a, b, c, d, x[i + 5], 5, -701558691);
        d = pX9O(d, a, b, c, x[i + 10], 9, 38016083);
        c = pX9O(c, d, a, b, x[i + 15], 14, -660478335);
        b = pX9O(b, c, d, a, x[i + 4], 20, -405537848);
        a = pX9O(a, b, c, d, x[i + 9], 5, 568446438);
        d = pX9O(d, a, b, c, x[i + 14], 9, -1019803690);
        c = pX9O(c, d, a, b, x[i + 3], 14, -187363961);
        b = pX9O(b, c, d, a, x[i + 8], 20, 1163531501);
        a = pX9O(a, b, c, d, x[i + 13], 5, -1444681467);
        d = pX9O(d, a, b, c, x[i + 2], 9, -51403784);
        c = pX9O(c, d, a, b, x[i + 7], 14, 1735328473);
        b = pX9O(b, c, d, a, x[i + 12], 20, -1926607734);
        a = pH9y(a, b, c, d, x[i + 5], 4, -378558);
        d = pH9y(d, a, b, c, x[i + 8], 11, -2022574463);
        c = pH9y(c, d, a, b, x[i + 11], 16, 1839030562);
        b = pH9y(b, c, d, a, x[i + 14], 23, -35309556);
        a = pH9y(a, b, c, d, x[i + 1], 4, -1530992060);
        d = pH9y(d, a, b, c, x[i + 4], 11, 1272893353);
        c = pH9y(c, d, a, b, x[i + 7], 16, -155497632);
        b = pH9y(b, c, d, a, x[i + 10], 23, -1094730640);
        a = pH9y(a, b, c, d, x[i + 13], 4, 681279174);
        d = pH9y(d, a, b, c, x[i + 0], 11, -358537222);
        c = pH9y(c, d, a, b, x[i + 3], 16, -722521979);
        b = pH9y(b, c, d, a, x[i + 6], 23, 76029189);
        a = pH9y(a, b, c, d, x[i + 9], 4, -640364487);
        d = pH9y(d, a, b, c, x[i + 12], 11, -421815835);
        c = pH9y(c, d, a, b, x[i + 15], 16, 530742520);
        b = pH9y(b, c, d, a, x[i + 2], 23, -995338651);
        a = pA9r(a, b, c, d, x[i + 0], 6, -198630844);
        d = pA9r(d, a, b, c, x[i + 7], 10, 1126891415);
        c = pA9r(c, d, a, b, x[i + 14], 15, -1416354905);
        b = pA9r(b, c, d, a, x[i + 5], 21, -57434055);
        a = pA9r(a, b, c, d, x[i + 12], 6, 1700485571);
        d = pA9r(d, a, b, c, x[i + 3], 10, -1894986606);
        c = pA9r(c, d, a, b, x[i + 10], 15, -1051523);
        b = pA9r(b, c, d, a, x[i + 1], 21, -2054922799);
        a = pA9r(a, b, c, d, x[i + 8], 6, 1873313359);
        d = pA9r(d, a, b, c, x[i + 15], 10, -30611744);
        c = pA9r(c, d, a, b, x[i + 6], 15, -1560198380);
        b = pA9r(b, c, d, a, x[i + 13], 21, 1309151649);
        a = pA9r(a, b, c, d, x[i + 4], 6, -145523070);
        d = pA9r(d, a, b, c, x[i + 11], 10, -1120210379);
        c = pA9r(c, d, a, b, x[i + 2], 15, 718787259);
        b = pA9r(b, c, d, a, x[i + 9], 21, -343485551);
        a = mE8w(a, cac2x);
        b = mE8w(b, cad2x);
        c = mE8w(c, cag2x);
        d = mE8w(d, cam2x)
    }
    return [a, b, c, d]
};
var wo4s = function () {
    var IL8D = function (i) {
        return i % 32
    }
        , IM8E = function (i) {
        return 32 - od8V - i % 32
    };
    return function (cS4W, IN8F) {
        var VA2x = []
            , lZ8R = (1 << od8V) - 1
            , mF8x = IN8F ? IL8D : IM8E;
        for (var i = 0, l = cS4W.length * od8V; i < l; i += od8V)
            VA2x[i >> 5] |= (cS4W.charCodeAt(i / od8V) & lZ8R) << mF8x(i);
        return VA2x
    }
}();
j4n.kE7x = function (i4m) {
    return VC2x(LV9M(wo4s(i4m, !0), i4m.length * od8V), !0)
};
var gC6w = {
    username: '123456@163.com',
    password: '123456',
};
var i4m = {
    username: gC6w.username,
    password: j4n.kE7x(gC6w.password),
};

console.log(i4m);