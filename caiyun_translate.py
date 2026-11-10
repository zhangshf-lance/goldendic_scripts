# -*- coding: utf-8 -*-
import json, sys, urllib.request, urllib.error
TOKEN='YOUR_CAIYUN_TOKEN'
if __name__=='__main__':
    text=' '.join(sys.argv[1:]).strip()
    if not text:
        print('^_^')
    else:
        try:
            body=json.dumps({'source':text,'trans_type':'en2zh','request_id':'goldendict','detect':'true'}).encode()
            req=urllib.request.Request('https://api.interpreter.caiyunai.com/v1/translator',data=body,headers={'Content-Type':'application/json','X-Authorization':'token '+TOKEN},method='POST')
            with urllib.request.urlopen(req,timeout=15) as r:
                data=json.loads(r.read().decode('utf-8'))
            print(data.get('target',''))
        except urllib.error.HTTPError as e:
            print('彩云翻译 HTTP {}: {}'.format(e.code,e.read().decode('utf-8','replace')),file=sys.stderr)
        except Exception as e:
            print('彩云翻译请求失败: {}'.format(e),file=sys.stderr)

