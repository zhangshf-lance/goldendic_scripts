#coding: utf8
import hashlib, json, os, random, sys, urllib.parse, urllib.request

def translate(content):
    appid=os.environ.get('BAIDU_APPID','YOUR_BAIDU_APPID'); secret=os.environ.get('BAIDU_SECRET_KEY','YOUR_BAIDU_SECRET_KEY')
    if appid=='yourappid' or secret=='yourkey': print('请先设置 BAIDU_APPID 和 BAIDU_SECRET_KEY',file=sys.stderr); return
    salt=str(random.randint(32768,65536)); sign=hashlib.md5((appid+content+salt+secret).encode()).hexdigest()
    try:
        url='http://api.fanyi.baidu.com/api/trans/vip/translate?'+urllib.parse.urlencode({'appid':appid,'q':content,'from':'en','to':'zh','salt':salt,'sign':sign})
        with urllib.request.urlopen(url,timeout=15) as r: data=json.loads(r.read().decode())
        if 'error_code' in data: print('百度翻译错误 [{}]: {}'.format(data.get('error_code'),data.get('error_msg')),file=sys.stderr); return
        print(data['trans_result'][0]['dst'].replace('\\r\\n','\n'))
    except Exception as e: print('百度翻译请求失败: {}'.format(e),file=sys.stderr)

if __name__=='__main__':
    text=' '.join(sys.argv[1:]).strip()
    print('^_^') if not text else translate(text.replace('\n','\\r\\n'))





