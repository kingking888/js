webpack = function (x) {
    function t(yy) {
        x[yy].apply(arguments)   //调用第几个方法
    }

    t(1)
}([function (x1, x2) {
    console.log('aaa')
}, function () {
    console.log('bbb')
}])  //方法列表