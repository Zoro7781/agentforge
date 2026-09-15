import os, tempfile
os.environ['APP_API_KEY']='test-only-application-key-0123456789'
os.environ['DATABASE_PATH']=os.path.join(tempfile.mkdtemp(),'test.db')
from fastapi.testclient import TestClient
from main import app, ENTITIES
H={'X-API-Key':os.environ['APP_API_KEY']}

def test_unauthorized():
    with TestClient(app) as c: assert c.get('/api/collections').status_code==401

def test_validation_and_unknown_collection():
    with TestClient(app) as c:
        assert c.post('/api/'+ENTITIES[0],headers=H,json={'name':''}).status_code==422
        assert c.get('/api/not-a-collection',headers=H).status_code==404

def test_crud_search_update_delete():
    with TestClient(app) as c:
        base='/api/'+ENTITIES[0]
        r=c.post(base,headers=H,json={'name':'Regression item','description':'test'})
        assert r.status_code==201
        row=r.json(); url=base+'/'+row['id']
        assert any(x['id']==row['id'] for x in c.get(base+'?q=Regression',headers=H).json())
        assert c.put(url,headers=H,json={'name':'Updated','status':'inactive'}).json()['status']=='inactive'
        assert c.delete(url,headers=H).status_code==204
        assert c.delete(url,headers=H).status_code==404
        assert c.put(url,headers=H,json={'name':'Gone'}).status_code==404

def test_health_and_collection_boundary():
    with TestClient(app) as c:
        assert c.get('/health').json()['status']=='ok'
        r=c.post('/api/'+ENTITIES[0],headers=H,json={'name':'Isolated'}).json()
        if len(ENTITIES)>1:
            assert c.delete('/api/'+ENTITIES[1]+'/'+r['id'],headers=H).status_code==404
        assert c.delete('/api/'+ENTITIES[0]+'/'+r['id'],headers=H).status_code==204
