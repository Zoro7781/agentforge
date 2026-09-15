import {owner,db,config,safe} from '@/lib/server';
export const dynamic='force-dynamic';
export async function GET(){return safe(async()=>{const u=await owner();const projects=await db().prepare('SELECT * FROM projects WHERE owner=? ORDER BY updated DESC LIMIT 100').bind(u.userId).all();const c=config();return Response.json({user:{name:u.fullName||'Noel',email:u.email},projects:projects.results,connections:{openai:!!(c.OPENAI_API_KEY&&c.OPENAI_MODEL),runner:!!(c.RUNNER_URL&&c.RUNNER_TOKEN),github:'https://github.com/Zoro7781/agentforge'}},{headers:{'Cache-Control':'no-store'}})});}
