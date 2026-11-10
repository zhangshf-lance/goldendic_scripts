#coding: utf8
import os,sys,uuid,requests
if __name__=='__main__':
    text=' '.join(sys.argv[1:]).strip(); key=os.environ.get('AZURE_TRANSLATOR_KEY','yourkey'); endpoint=os.environ.get('AZURE_TRANSLATOR_ENDPOINT','yourendpoint').rstrip('/'); region=os.environ.get('AZURE_TRANSLATOR_REGION','yourlocation')
    if not text: print('^_^')
    elif key=='yourkey' or endpoint=='yourendpoint': print('请设置 AZURE_TRANSLATOR_KEY、AZURE_TRANSLATOR_ENDPOINT、AZURE_TRANSLATOR_REGION',file=sys.stderr)
    else:
        try:
            h={'Ocp-Apim-Subscription-Key':key,'Ocp-Apim-Subscription-Region':region,'Content-Type':'application/json','X-ClientTraceId':str(uuid.uuid4())}; r=requests.post(endpoint+'/translate?api-version=3.0&from=en&to=zh-Hans',headers=h,json=[{'text':text}],timeout=15); r.raise_for_status(); print(r.json()[0]['translations'][0]['text'])
        except Exception as e: print('微软翻译请求失败: {}'.format(e),file=sys.stderr)


