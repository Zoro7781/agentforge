"""Run on a dedicated Docker host, never in the Sites control plane.
Only the fixed pytest command runs inside the container. Build the sandbox image first.
"""
import hashlib, hmac, json, os, pathlib, secrets, subprocess, tempfile, time, threading
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title='AgentForge isolated test runner')
class Job(BaseModel):
    files: dict[str,str] = Field(min_length=1,max_length=100)
    digest: str = Field(pattern=r'^[a-f0-9]{64}$')

def validate_files(files):
    if len(files)>100 or sum(len(v.encode('utf-8')) for v in files.values())>2_000_000:
        raise ValueError('Artifact exceeds runner limits')
    for name in files:
        p=pathlib.PurePosixPath(name)
        if not name or name == '.' or str(p) != name or p.is_absolute() or '..' in p.parts or '\\' in name or '\x00' in name or ':' in name:
            raise ValueError('Unsafe artifact path')
        if len(name)>200: raise ValueError('Artifact path too long')
    if 'test_app.py' not in files or 'main.py' not in files: raise ValueError('Required test files missing')

def command(folder,container):
    return ['docker','run','--rm','--name',container,'--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--pids-limit=64','--memory=256m','--cpus=1','--user=10001:10001','--tmpfs=/tmp:rw,nosuid,nodev,size=64m','--mount',f'type=bind,src={folder},dst=/app,readonly','--workdir=/app','--env=PYTHONDONTWRITEBYTECODE=1','agentforge-sandbox:local','python','-m','pytest','-q','-p','no:cacheprovider']

@app.get('/health')
def health(): return {'status':'ok'}

@app.post('/test')
def run(job: Job, authorization: str = Header(default='')):
    expected=os.getenv('RUNNER_TOKEN','')
    if len(expected)<32 or not hmac.compare_digest(authorization,'Bearer '+expected):
        raise HTTPException(401,'Invalid runner token')
    try: validate_files(job.files)
    except ValueError as e: raise HTTPException(400,str(e))
    # JS insertion order and compact UTF-8 serialization are preserved by JSON parsing.
    digest=hashlib.sha256(json.dumps(job.files,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    if digest!=job.digest: raise HTTPException(400,'Artifact digest mismatch')
    name='agentforge-test-'+secrets.token_hex(12);start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='agentforge-') as folder:
        os.chmod(folder,0o755)
        for path,content in job.files.items():
            target=pathlib.Path(folder,path);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding="utf-8");target.chmod(0o644)
        try:
            proc=subprocess.Popen(command(folder,name),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            buffers=[bytearray(),bytearray()]
            def drain(stream,buffer):
                while True:
                    chunk=stream.read(8192)
                    if not chunk: break
                    if len(buffer)<45000: buffer.extend(chunk[:45000-len(buffer)])
                stream.close()
            threads=[threading.Thread(target=drain,args=(stream,buffers[i]),daemon=True) for i,stream in enumerate([proc.stdout,proc.stderr])]
            for thread in threads: thread.start()
            try: code=proc.wait(timeout=45)
            except subprocess.TimeoutExpired:
                proc.kill();proc.wait(timeout=5)
                raise
            finally:
                for thread in threads: thread.join(timeout=2)
            if code in [125,126,127]: raise HTTPException(503,'The sandbox image or Docker runtime is unavailable')
            return {'exit_code':code,'stdout':buffers[0].decode(errors='replace'),'stderr':buffers[1].decode(errors='replace'),'duration_seconds':round(time.monotonic()-start,3),'digest':job.digest}
        except subprocess.TimeoutExpired:
            raise HTTPException(504,'Test exceeded the 45-second execution limit')
        except FileNotFoundError:
            raise HTTPException(503,'Docker is unavailable on the runner host')
        finally:
            try: subprocess.run(['docker','rm','-f',name],capture_output=True,timeout=10)
            except (FileNotFoundError,subprocess.TimeoutExpired): pass
