"""Integration checks against the local Sites development server (not production)."""
import concurrent.futures, io, os, tarfile, uuid
import httpx
base=os.environ.get('AGENTFORGE_TEST_URL','http://localhost:5173')
assert base.startswith(('http://localhost:', 'http://127.0.0.1:')), 'Local test server required'
checks=0
def check(r,status):
 global checks
 assert r.status_code==status,(r.status_code,r.text[:300]); checks+=1; return r
with httpx.Client(base_url=base,timeout=30) as c:
 check(c.get('/api/workspace'),401)
 check(c.get('/api/workspace',headers={'oai-authenticated-user-id':'spoof','oai-authenticated-user-email':'spoof@example.test'}),401)
 check(c.get('/signin-with-chatgpt?return_to=%2F'),302)
 check(c.get('/api/workspace'),200)
 check(c.post('/api/projects',json={}),400)
 check(c.post('/api/projects',content='{'),400)
 check(c.post('/api/projects',json={},headers={'Origin':'https://evil.test'}),403)
 check(c.post('/api/projects',content='x'*20001),413)
 for template in ['inventory','crm','booking','projects']:
  pid=check(c.post('/api/projects',json={'name':'Regression '+template,'prompt':'Create a usable CRUD workspace for testing.','template':template}),201).json()['id']
  path='/api/projects/'+pid
  check(c.get(path+'/export'),404)
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   responses=list(pool.map(lambda _:c.post(path+'/build'),range(4)))
  assert all(r.status_code in [200,201] for r in responses),[r.text for r in responses]
  assert len({r.json()['id'] for r in responses})==1; checks+=2
  detail=check(c.get(path),200).json(); assert len(detail['builds'])==1
  bundle=check(c.get(path+'/export?format=json'),200).json()
  archive=check(c.get(path+'/export'),200)
  with tarfile.open(fileobj=io.BytesIO(archive.content)) as tar:
   assert tar.extractfile('main.py').read().decode()==bundle['files']['main.py']; checks+=1
  check(c.post(path+'/plan'),503)
  check(c.post(path+'/test'),503)
  check(c.patch(path,content='null',headers={'Content-Type':'application/json'}),400)
  check(c.patch(path,json={'status':'archived'}),200)
  check(c.post(path+'/build'),409)
  check(c.patch(path,json={'status':'draft'}),200)
  check(c.post(path+'/build'),200)
 check(c.get('/api/projects/'+str(uuid.uuid4())),404)
 check(c.get('/signout-with-chatgpt?return_to=%2F'),302)
 check(c.get(path),401)
print(f'{checks} workspace integration checks passed')
