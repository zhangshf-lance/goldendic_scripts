# -*- coding: utf-8 -*-
import json,sys,urllib.parse,urllib.request
APIKEY='YOUR_NIUTRANS_APIKEY'
if __name__=='__main__':
 text=' '.join(sys.argv[1:]).strip()
 if not text: print('^_^')
 else:
  try:
   q=urllib.parse.urlencode({'apikey':APIKEY,'from':'en','to':'zh','src_text':text})
   with urllib.request.urlopen('https://api.niutrans.com/NiuTransServer/translation?'+q,timeout=15) as r:
    d=json.loads(r.read().decode()); print(d.get('tgt_text') or d.get('target') or d.get('error_msg','小牛翻译返回异常'))
  except Exception as e: print('小牛翻译请求失败: {}'.format(e),file=sys.stderr)

