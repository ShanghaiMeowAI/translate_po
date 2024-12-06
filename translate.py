import urllib.request
import execjs

class Yuguii():

    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 

        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 

        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 

    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)

def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def translate(content, tk):
    if len(content) > 4891:
        print("翻译文本超过限制！")
        return

    content = urllib.parse.quote(content)

    url = "http://translate.google.com/translate_a/single?client=t" \
          "&sl=en&tl=th&hl=th&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)


    result = open_url(url)

    end = result.find("\",")
    if end > 4:
        return result[4:end]
def fy(i):
    if i:  # 检查是否为非空的字符串
        try:
            tk = Yuguii().getTk(i)  # 获取翻译所需的 token
            translated_str = translate(i, tk)  # 进行翻译
            
            if translated_str is None:
                return '翻译错误'
            else:
                return translated_str
        except Exception as e:
            return f'发生错误'  # 捕获异常并返回错误信息
    else:
        return i  # 如果是空字符串，直接返回

def translate_list(list):
    li=[]
    for i in list:
        tk = Yuguii().getTk(i)
        string1=translate(i, tk)
        if string1.lower() != i.strip().lower():
            li.append(string1)
    return(li)

def translate_li(i):
    tk = Yuguii().getTk(i)
    string1=translate(i, tk)
    if string1.lower() != i.strip().lower():
        return string1
    else:
        return i