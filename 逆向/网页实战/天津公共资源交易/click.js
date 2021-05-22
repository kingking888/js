// $("a").bind('click', function() {
//     var hh = $(this).attr("href");
//     if (typeof (hh) == 'undefined' || hh == '#') {
//         hh = $(this).attr("url");
//         if (typeof (hh) == 'undefined' || hh == '#') {
//             return
//         }
//     }
//     var aa = hh.split("/");
//     var aaa = aa.length;
//     var bbb = aa[aaa - 1].split('.');
//     var ccc = bbb[0];
//     var cccc = bbb[1];
//     var r = /^\+?[1-9][0-9]*$/;
//     var ee = $(this).attr('target');
//     if (r.test(ccc) && cccc.indexOf('jhtml') != -1) {
//         var srcs = CryptoJS.enc.Utf8.parse(ccc);
//         var k = CryptoJS.enc.Utf8.parse(s);
//         var en = CryptoJS.AES.encrypt(srcs, k, {
//             mode: CryptoJS.mode.ECB,
//             padding: CryptoJS.pad.Pkcs7
//         });
//         var ddd = en.toString();
//         ddd = ddd.replace(/\//g, "^");
//         ddd = ddd.substring(0, ddd.length - 2);
//         var bbbb = ddd + '.' + bbb[1];
//         aa[aaa - 1] = bbbb;
//         var uuu = '';
//         for (i = 0; i < aaa; i++) {
//             uuu += aa[i] + '/'
//         }
//         uuu = uuu.substring(0, uuu.length - 1);
//         if (typeof (ee) == 'undefined') {
//             window.location = uuu
//         } else {
//             window.open(uuu)
//         }
//     } else {
//         if (typeof (ee) == 'undefined') {
//             window.location = hh
//         } else {
//             window.open(hh)
//         }
//     }
//     return false
// });



//思路:element选中相应加密地址,转到event listeners观察到有个a的click事件,其中加密逻辑就是上面代码


function get_url(url) {
    var hh = url;
    if (typeof (hh) == 'undefined' || hh == '#') {
        return
    }
    var aa = hh.split("/");
    var aaa = aa.length;
    var bbb = aa[aaa - 1].split('.');
    var ccc = bbb[0];
    var cccc = bbb[1];
    var r = /^\+?[1-9][0-9]*$/;
    var  CryptoJS = require('crypto-js');
    //jquery.min.js里固定值
    var s = "qnbyzzwmdgghmcnm";
    if (r.test(ccc) && cccc.indexOf('jhtml') != -1) {
        var srcs = CryptoJS.enc.Utf8.parse(ccc);
        var k = CryptoJS.enc.Utf8.parse(s);
        var en = CryptoJS.AES.encrypt(srcs, k, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        var ddd = en.toString();
        ddd = ddd.replace(/\//g, "^");
        ddd = ddd.substring(0, ddd.length - 2);
        var bbbb = ddd + '.' + bbb[1];
        aa[aaa - 1] = bbbb;
        var uuu = '';
        for (i = 0; i < aaa; i++) {
            uuu += aa[i] + '/'
        }
        uuu = uuu.substring(0, uuu.length - 1);
        return uuu
    }
}

console.log(get_url('http://ggzy.zwfwb.tj.gov.cn:80/jyxxcggg/961342.jhtml'));

