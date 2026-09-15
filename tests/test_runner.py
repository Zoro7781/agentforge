import hashlib,json,os,subprocess,unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from services.runner.server import app,validate_files,command
class RunnerTests(unittest.TestCase):
 def test_unsafe_paths(self):
  for path in ['../secret','/etc/passwd','a/../../x','a\\x','.', './main.py','a//b', 'x\x00']:
   with self.subTest(path=path), self.assertRaises(ValueError):validate_files({'main.py':'','test_app.py':'',path:'x'})
 def test_file_limits(self):
  with self.assertRaises(ValueError):validate_files({'main.py':'a'*2_000_001,'test_app.py':''})
  with self.assertRaises(ValueError):validate_files({'main.py':''})
 def test_container_isolation(self):
  args=command('/tmp/job','container')
  for flag in ['--network=none','--read-only','--cap-drop=ALL','--security-opt=no-new-privileges','--user=10001:10001','--pids-limit=64','--memory=256m']:self.assertIn(flag,args)
  self.assertEqual(args[-5:],['-m','pytest','-q','-p','no:cacheprovider'])
 def test_unauthenticated_rejected(self):
  with TestClient(app) as client:self.assertEqual(client.post('/test',json={'files':{'main.py':'','test_app.py':''},'digest':'0'*64}).status_code,401)
 def test_digest_mismatch(self):
  with patch.dict(os.environ,{'RUNNER_TOKEN':'x'*32}),TestClient(app) as client:
   self.assertEqual(client.post('/test',headers={'Authorization':'Bearer '+'x'*32},json={'files':{'main.py':'','test_app.py':''},'digest':'0'*64}).status_code,400)
 def test_docker_unavailable(self):
  files={'main.py':'','test_app.py':''};digest=hashlib.sha256(json.dumps(files,separators=(',',':')).encode()).hexdigest()
  with patch.dict(os.environ,{'RUNNER_TOKEN':'x'*32}),patch('services.runner.server.subprocess.Popen',side_effect=FileNotFoundError),TestClient(app) as client:
   self.assertEqual(client.post('/test',headers={'Authorization':'Bearer '+'x'*32},json={'files':files,'digest':digest}).status_code,503)
