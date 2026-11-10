# -*- coding: utf-8 -*-
"""腾讯云机器翻译 GoldenDict 脚本。用法：python tencent_translate.py "hello""" 
import hashlib, hmac, json, sys, datetime, urllib.request, urllib.parse

SECRET_ID = "YOUR_TENCENT_SECRET_ID"
SECRET_KEY = "YOUR_TENCENT_SECRET_KEY"
SERVICE = "tmt"
HOST = "tmt.tencentcloudapi.com"
ENDPOINT = "https://" + HOST
REGION = "ap-beijing"

def sha256hex(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def sign(key, msg): return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def translate(text):
    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    date = datetime.datetime.fromtimestamp(now, datetime.timezone.utc).strftime("%Y-%m-%d")
    payload = json.dumps({"Source":"en", "Target":"zh", "ProjectId":0, "SourceText":text}, separators=(",",":"), ensure_ascii=False)
    ct = "application/json; charset=utf-8"
    headers = {"Content-Type":ct, "Host":HOST, "X-TC-Action":"TextTranslate", "X-TC-Version":"2018-03-21", "X-TC-Region":REGION, "X-TC-Timestamp":str(now)}
    signed = "content-type;host;x-tc-action;x-tc-timestamp"
    canonical = "POST\n/\n\ncontent-type:"+ct+"\nhost:"+HOST+"\nx-tc-action:texttranslate\nx-tc-timestamp:"+str(now)+"\n\n"+signed+"\n"+sha256hex(payload)
    credential = SECRET_ID + "/" + date + "/" + SERVICE + "/tc3_request"
    sts = "TC3-HMAC-SHA256\n"+str(now)+"\n"+date+"/"+SERVICE+"/tc3_request\n"+sha256hex(canonical)
    key_date = sign(("TC3"+SECRET_KEY).encode(), date)
    key_service = sign(key_date, SERVICE); key_sign = sign(key_service, "tc3_request")
    authorization = "TC3-HMAC-SHA256 Credential="+credential+", SignedHeaders="+signed+", Signature="+hmac.new(key_sign, sts.encode(), hashlib.sha256).hexdigest()
    headers["Authorization"] = authorization
    try:
        req = urllib.request.Request(ENDPOINT, data=payload.encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp: data=json.loads(resp.read().decode("utf-8"))
        err=data.get("Response",{}).get("Error")
        if err: print("腾讯翻译错误 [{}]: {}".format(err.get("Code"),err.get("Message")), file=sys.stderr); return
        print(data["Response"]["TargetText"])
    except Exception as e: print("腾讯翻译请求失败: {}".format(e), file=sys.stderr)

if __name__ == "__main__":
    text=" ".join(sys.argv[1:]).strip()
    if text: translate(text)
    else: print("^_^")



