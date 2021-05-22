function generateSignature(userId) {
    //添加userAgent
    this.navigator = {
        userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    };
    //添加canvas
    document = {
        createElement: function () {
            return canvas
        }
    };
    canvas = {
        getContext: function getContext() {
            return CanvasRenderingContext2D
        },
        toDataURL: function toDataURL() {
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAQCAYAAABQrvyxAAAD2klEQVRIS8XWfazXcxQH8Ncvt9mtrLaoJIpZD9bubcMwTB4i+cPTSsgmumbLSB5HIxbaNEMyT5Uh8rQxhTyOElPmoTJGSyO5ktHzjXuvna9zt2+/ruYP5bN999v3+/t8zjnvc97nfT4VO65adMBYbMMzaMEFqMMbpe1/YkHV+T35OhQNlSqPDbgezyeQCPwudMKF+Ly0fyFm7caI5+DUKvubcHB+OxdTygD2w50YgpWI/w7BZ1iCI0vGjsBDeHg3Aqg2Hcm9aVcA4sDhuAq/5+kueDrpcx4+KVm9DT/tQQCzkwVN6bMG31VT6Azcjldz0/HZBwFkBN4vBRzU2p7vR+GxfC7CjXgL++Bd7I+T8VXp/AlJz3qsQwQ4Bc3tJKUPvsRZeOefKBTfA8AdeDM3HYMnswfOxnsl441JoWjyb/ECIvhHcBn64kqciL3xOu7O80HHVzARr2EQ5qbvalp2xEtp45SS/516IP4LZ8OSa8emg+n4HlPxY6pSKFWrVhP1NsQ6S7VarLkQgMW5P5r+CQTw8VHuzHD4CZUbh4vxTQYVeyKBUem21TMFpRcimZHcsBtrJwp1TWfhMIIOKs3HF9iAa3AfRmOVjrZoMFez/uaZqsU0jeq1FCBHZXUux0lJrTKACOC5pNQtGdBpWaGQ6x6I7wE0KhcVXV9FrZ0qEHx9FCuwDJOxFG8jeiF+I/iQsopOmnS1TV/d9dbNh/rYaqzfiip8jDMxDfPaATAw93THHxlY0ONeDEZ8fzCfMm3LGEJiJ5SbOEr4QO6IwKPJQlKjycJY2xpTAKzTVaMbjLDeLI9jOX5VEfq9JUt+WEG1vxu8rQIzEMFuTfttdssAyoFGRa7LJMY8iiZfTeFnRrUKRZY/zXIFH6PRYtpempkfgDVq/GKQDb42yVNmGunFpMMGlWJ6R/YnlOZEGcAHWd1bcVwp0vYA9EsW3JxqGFSOmCOxkdSF1QA+yutCdH4Yj+4POQxZjAwP08Ey3W2yr4E2O9Rq92NRkeFKkdVQk5DMgzLLEWMZwEwMz4kfWdxVBc7PuXR0Ff/jdSQm7QrA6SlxIZeh88vVGK6bFXqot1Kda80xpQg4eibo056Gt+P7X386ICsQ1I6BuiYlPWT4HjxbDWC6Gj+o1azWJtsNUGOJvbTobLvO+umrl8XG6W+jq80wqrg3rUWTSsH3/3rF3eeK7IFQp8151YnqVQFoVTFLF5eIyRuyGgDj1hm/tc4xygLjDbXI/GJgxWSNrGxVKW6te3ztWIFWHRxotCYNemvVw0YtmjXqaZXBellrjAUme7mYBfz8fwYf2foL39kKNV4oN9YAAAAASUVORK5CYII="
        },
    };
    CanvasRenderingContext2D = {
        arc: function arc() {
        },
        stroke: function stroke() {
        },
        fillText: function fillText() {
        },
    };

    var e = {}

    var r = (function () {
        function e(e, a, r) {
            return (b[e] || (b[e] = t("x,y", "return x " + e + " y")))(r, a)
        }

        function a(e, a, r) {
            return (k[r] || (k[r] = t("x,y", "return new x[y](" + Array(r + 1).join(",x[++y]").substr(1) + ")")))(e, a)
        }

        function r(e, a, r) {
            var n, t, s = {}, b = s.d = r ? r.d + 1 : 0;
            for (s["$" + b] = s, t = 0; t < b; t++) s[n = "$" + t] = r[n];
            for (t = 0, b = s.length = a.length; t < b; t++) s[t] = a[t];
            return c(e, 0, s)
        }

        function c(t, b, k) {
            function u(e) {
                v[x++] = e
            }

            function f() {
                return g = t.charCodeAt(b++) - 32, t.substring(b, b += g)
            }

            function l() {
                try {
                    y = c(t, b, k)
                } catch (e) {
                    h = e, y = l
                }
            }

            for (var h, y, d, g, v = [], x = 0; ;) switch (g = t.charCodeAt(b++) - 32) {
                case 1:
                    u(!v[--x]);
                    break;
                case 4:
                    v[x++] = f();
                    break;
                case 5:
                    u(function (e) {
                        var a = 0, r = e.length;
                        return function () {
                            var c = a < r;
                            return c && u(e[a++]), c
                        }
                    }(v[--x]));
                    break;
                case 6:
                    y = v[--x], u(v[--x](y));
                    break;
                case 8:
                    if (g = t.charCodeAt(b++) - 32, l(), b += g, g = t.charCodeAt(b++) - 32, y === c) b += g; else if (y !== l) return y;
                    break;
                case 9:
                    v[x++] = c;
                    break;
                case 10:
                    u(s(v[--x]));
                    break;
                case 11:
                    y = v[--x], u(v[--x] + y);
                    break;
                case 12:
                    for (y = f(), d = [], g = 0; g < y.length; g++) d[g] = y.charCodeAt(g) ^ g + y.length;
                    u(String.fromCharCode.apply(null, d));
                    break;
                case 13:
                    y = v[--x], h = delete v[--x][y];
                    break;
                case 14:
                    v[x++] = t.charCodeAt(b++) - 32;
                    break;
                case 59:
                    u((g = t.charCodeAt(b++) - 32) ? (y = x, v.slice(x -= g, y)) : []);
                    break;
                case 61:
                    u(v[--x][t.charCodeAt(b++) - 32]);
                    break;
                case 62:
                    g = v[--x], k[0] = 65599 * k[0] + k[1].charCodeAt(g) >>> 0;
                    break;
                case 65:
                    h = v[--x], y = v[--x], v[--x][y] = h;
                    break;
                case 66:
                    u(e(t[b++], v[--x], v[--x]));
                    break;
                case 67:
                    y = v[--x], d = v[--x], u((g = v[--x]).x === c ? r(g.y, y, k) : g.apply(d, y));
                    break;
                case 68:
                    u(e((g = t[b++]) < "<" ? (b--, f()) : g + g, v[--x], v[--x]));
                    break;
                case 70:
                    u(!1);
                    break;
                case 71:
                    v[x++] = n;
                    break;
                case 72:
                    v[x++] = +f();
                    break;
                case 73:
                    u(parseInt(f(), 36));
                    break;
                case 75:
                    if (v[--x]) {
                        b++;
                        break
                    }
                case 74:
                    g = t.charCodeAt(b++) - 32 << 16 >> 16, b += g;
                    break;
                case 76:
                    u(k[t.charCodeAt(b++) - 32]);
                    break;
                case 77:
                    y = v[--x], u(v[--x][y]);
                    break;
                case 78:
                    g = t.charCodeAt(b++) - 32, u(a(v, x -= g + 1, g));
                    break;
                case 79:
                    g = t.charCodeAt(b++) - 32, u(k["$" + g]);
                    break;
                case 81:
                    h = v[--x], v[--x][f()] = h;
                    break;
                case 82:
                    u(v[--x][f()]);
                    break;
                case 83:
                    h = v[--x], k[t.charCodeAt(b++) - 32] = h;
                    break;
                case 84:
                    v[x++] = !0;
                    break;
                case 85:
                    v[x++] = void 0;
                    break;
                case 86:
                    u(v[x - 1]);
                    break;
                case 88:
                    h = v[--x], y = v[--x], v[x++] = h, v[x++] = y;
                    break;
                case 89:
                    u(function () {
                        function e() {
                            return r(e.y, arguments, k)
                        }

                        return e.y = f(), e.x = c, e
                    }());
                    break;
                case 90:
                    v[x++] = null;
                    break;
                case 91:
                    v[x++] = h;
                    break;
                case 93:
                    h = v[--x];
                    break;
                case 0:
                    return v[--x];
                default:
                    u((g << 16 >> 16) - 16)
            }
        }

        var n = this, t = n.Function, s = Object.keys || function (e) {
            var a = {}, r = 0;
            for (var c in e) a[r++] = c;
            return a.length = r, a
        }, b = {}, k = {};
        return r
    })()
        //    调用函数r传入两个参数
        ('gr$Daten Иb/s!l y͒yĹg,(lfi~ah`{mv,-n|jqewVxp{rvmmx,&effkx[!cs"l".Pq%widthl"@q&heightl"vr*getContextx$"2d[!cs#l#,*;?|u.|uc{uq$fontl#vr(fillTextx$$龘ฑภ경2<[#c}l#2q*shadowBlurl#1q-shadowOffsetXl#$$limeq+shadowColorl#vr#arcx88802[%c}l#vr&strokex[ c}l"v,)}eOmyoZB]mx[ cs!0s$l$Pb<k7l l!r&lengthb%^l$1+s$jl  s#i$1ek1s$gr#tack4)zgr#tac$! +0o![#cj?o ]!l$b%s"o ]!l"l$b*b^0d#>>>s!0s%yA0s"l"l!r&lengthb<k+l"^l"1+s"jl  s&l&z0l!$ +["cs\'(0l#i\'1ps9wxb&s() &{s)/s(gr&Stringr,fromCharCodes)0s*yWl ._b&s o!])l l Jb<k$.aj;l .Tb<k$.gj/l .^b<k&i"-4j!+& s+yPo!]+s!l!l Hd>&l!l Bd>&+l!l <d>&+l!l 6d>&+l!l &+ s,y=o!o!]/q"13o!l q"10o!],l 2d>& s.{s-yMo!o!]0q"13o!]*Ld<l 4d#>>>b|s!o!l q"10o!],l!& s/yIo!o!].q"13o!],o!]*Jd<l 6d#>>>b|&o!]+l &+ s0l-l!&l-l!i\'1z141z4b/@d<l"b|&+l-l(l!b^&+l-l&zl\'g,)gk}ejo{cm,)|yn~Lij~em["cl$b%@d<l&zl\'l $ +["cl$b%b|&+l-l%8d<@b|l!b^&+ q$sign ', [e])
    return (0, e.sign)(userId);
}

// var _ = process.argv.splice(2)
//
// console.log(generateSignature(_[0]))

console.log(generateSignature('110567353301'))