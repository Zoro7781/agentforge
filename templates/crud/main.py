import os, secrets, sqlite3, json
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

ENTITIES = __ENTITIES__
DB_PATH = os.getenv('DATABASE_PATH', '/data/application.db')

def connection():
    c = sqlite3.connect(DB_PATH, timeout=10)
    c.row_factory = sqlite3.Row
    return c

@asynccontextmanager
async def lifespan(app):
    if not os.getenv('APP_API_KEY') or len(os.environ['APP_API_KEY']) < 24:
        raise RuntimeError('Set APP_API_KEY to a random secret of at least 24 characters.')
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    with connection() as c:
        c.execute('CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, entity TEXT NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL, updated TEXT NOT NULL)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_records_entity_created ON records(entity,created)')
    yield

app = FastAPI(title=__TITLE__, lifespan=lifespan)

def authorize(x_api_key: str = Header(default='')):
    key = os.getenv('APP_API_KEY', '')
    if not key or not secrets.compare_digest(x_api_key, key):
        raise HTTPException(401, 'Invalid application key')

def entity_check(entity):
    if entity not in ENTITIES:
        raise HTTPException(404, 'Unknown collection')

class RecordInput(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default='', max_length=4000)
    status: str = Field(default='active', pattern='^(active|inactive|archived)$')

@app.get('/health')
def health():
    with connection() as c: c.execute('SELECT 1')
    return {'status':'ok'}

@app.get('/')
def home(): return FileResponse('index.html')

@app.get('/api/collections', dependencies=[Depends(authorize)])
def collections(): return ENTITIES

@app.get('/api/{entity}', dependencies=[Depends(authorize)])
def list_records(entity: str, q: str = Query(default='', max_length=160), limit: int = Query(default=50, ge=1, le=100), offset: int = Query(default=0, ge=0)):
    entity_check(entity)
    with connection() as c:
        rows=c.execute('SELECT * FROM records WHERE entity=? AND (name LIKE ? OR description LIKE ?) ORDER BY created DESC LIMIT ? OFFSET ?', (entity, '%'+q+'%', '%'+q+'%', limit, offset)).fetchall()
    return [dict(r) for r in rows]

@app.post('/api/{entity}', status_code=201, dependencies=[Depends(authorize)])
def create_record(entity: str, value: RecordInput):
    entity_check(entity)
    now=datetime.now(timezone.utc).isoformat()
    row={'id':str(uuid4()),'entity':entity,**value.model_dump(),'created':now,'updated':now}
    with connection() as c:
        c.execute('INSERT INTO records (id,entity,name,description,status,created,updated) VALUES (?,?,?,?,?,?,?)', tuple(row[k] for k in ['id','entity','name','description','status','created','updated']))
    return row

@app.put('/api/{entity}/{record_id}', dependencies=[Depends(authorize)])
def update_record(entity: str, record_id: str, value: RecordInput):
    entity_check(entity)
    with connection() as c:
        r=c.execute('UPDATE records SET name=?,description=?,status=?,updated=? WHERE id=? AND entity=?', (value.name,value.description,value.status,datetime.now(timezone.utc).isoformat(),record_id,entity))
        if r.rowcount != 1: raise HTTPException(404, 'Record not found')
        return dict(c.execute('SELECT * FROM records WHERE id=? AND entity=?',(record_id,entity)).fetchone())

@app.delete('/api/{entity}/{record_id}', status_code=204, dependencies=[Depends(authorize)])
def delete_record(entity: str, record_id: str):
    entity_check(entity)
    with connection() as c:
        r=c.execute('DELETE FROM records WHERE id=? AND entity=?',(record_id,entity))
        if r.rowcount != 1: raise HTTPException(404,'Record not found')
