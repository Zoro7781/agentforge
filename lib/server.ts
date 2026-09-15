import { env } from 'cloudflare:workers';
import { getChatGPTUser } from '@/app/chatgpt-auth';
export class ApiError extends Error { constructor(public status:number,message:string){super(message);} }
export function db(){ const binding = (env as typeof env & {DB?:D1Database}).DB; if(!binding)throw new ApiError(503,'Workspace storage is unavailable. Please try again.');return binding; }
export function config(){return env as typeof env & {OPENAI_API_KEY?:string;OPENAI_MODEL?:string;RUNNER_URL?:string;RUNNER_TOKEN?:string};}
export async function owner(){const u=await getChatGPTUser();if(!u)throw new ApiError(401,'Sign in with ChatGPT to access your workspace.');return u;}
export async function project(id:string){const u=await owner();const p=await db().prepare('SELECT * FROM projects WHERE id=? AND owner=?').bind(id,u.userId).first<Record<string,string>>();if(!p)throw new ApiError(404,'Project not found.');return p;}
export function sameOrigin(req:Request){const origin=req.headers.get('origin');if(origin&&origin!==new URL(req.url).origin)throw new ApiError(403,'Cross-origin request rejected.');}
export async function body(req:Request){if(Number(req.headers.get('content-length')||0)>20000)throw new ApiError(413,'Request too large.');const text=await req.text();if(text.length>20000)throw new ApiError(413,'Request too large.');try{return JSON.parse(text)}catch{throw new ApiError(400,'Invalid JSON.');}}
export async function safe(fn:()=>Promise<Response>){try{return await fn()}catch(e){if(e instanceof ApiError)return Response.json({error:e.message},{status:e.status});console.error('workspace_request_failed',e instanceof Error?e.message:'unknown');return Response.json({error:'The operation could not be completed. Please try again.'},{status:500});}}
export function eventStatement(id:string,agent:string,message:string){return db().prepare('INSERT INTO events (id,project_id,agent,message,created) VALUES (?,?,?,?,?)').bind(crypto.randomUUID(),id,agent,message,new Date().toISOString());}
export async function digest(value:string){return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(value)))).map(b=>b.toString(16).padStart(2,'0')).join('');}
