import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const req=createRequire(import.meta.url);
const {generate,tar}=req(path.resolve(process.argv[2],'generator.js'));
for(const template of ['inventory','crm','booking','projects']){
 const files=generate('Test <workspace>','Create a usable CRUD workspace.',template);
 assert(files['main.py'].includes('ENTITIES = ['));
 assert(!files['main.py'].includes('__TITLE__'));
 assert(files['index.html'].includes('Test &lt;workspace&gt;'));
 assert(files['test_app.py'].includes('test_crud_search_update_delete'));
 assert(!Object.keys(files).some(n=>n.startsWith('/')||n.includes('..')));
 const folder=path.resolve(process.argv[3],template);fs.mkdirSync(folder,{recursive:true});
 for(const [name,content] of Object.entries(files))fs.writeFileSync(path.join(folder,name),content);
 fs.writeFileSync(folder+'.tar',tar(files));
}
console.log('Four template bundles generated; escaping and manifest checks passed.');
