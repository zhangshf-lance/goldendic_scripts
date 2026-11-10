# -*- coding: utf-8 -*-
"""MyMemory 翻译脚本，GoldenDict 用法：python mymemory_translate.py "hello""" 
import json
import sys
import urllib.parse
import urllib.request
import urllib.error

# 如需提高免费额度，可填写自己的邮箱（每天约 50000 字符）；留空使用匿名额度
EMAIL = "YOUR_EMAIL"


def translate(text):
    params = {
        "q": text,
        "langpair": "en|zh-CN",
        "mt": "1",
    }
    if EMAIL:
        params["de"] = EMAIL
    url = "https://api.mymemory.translated.net/get?" + urllib.parse.urlencode(params)
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "GoldenDict-MyMemory/1.0"})
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        if data.get("responseStatus") != 200:
            print("MyMemory 翻译错误: {}".format(data.get("responseDetails", "未知错误")), file=sys.stderr)
            return
        result = data.get("responseData", {}).get("translatedText", "")
        if result:
            print(result.replace("\\r\\n", "\n"))
        else:
            print("MyMemory 未返回译文", file=sys.stderr)
    except urllib.error.HTTPError as error:
        print("MyMemory HTTP {}: {}".format(error.code, error.read().decode("utf-8", "replace")), file=sys.stderr)
    except Exception as error:
        print("MyMemory 请求失败: {}".format(error), file=sys.stderr)


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]).strip()
    if text:
        translate(text)
    else:
        print("^_^")


