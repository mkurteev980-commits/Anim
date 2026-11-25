import fs from 'fs';
const list=await (await fetch('http://127.0.0.1:9336/json')).json();const page=list.find(p=>p.type==='page');
const ws=new WebSocket(page.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);let id=0;const pend=new Map();ws.onmessage=m=>{const d=JSON.parse(m.data);if(pend.has(d.id)){pend.get(d.id)(d);pend.delete(d.id);}};
const send=(method,params)=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}));});
await new Promise(r=>setTimeout(r,2000));
const code=fs.readFileSync(process.argv[2],'utf8');
for(const n of [1,2]){const r=await send('Runtime.evaluate',{expression:code+`;playing=false;ctx=mainCtx;SC=1;T=1.3;TN=0;LIPV=0;CAM={z:1,fx:540,fy:960};ctx.setTransform(1,0,0,1,0,0);COVER${n}();document.getElementById('stage').toDataURL('image/png')`,returnByValue:true});
 const v=r.result.result.value;if(!v||!v.startsWith('data')){console.log('ERR',JSON.stringify(r).slice(0,600));continue;}fs.writeFileSync(process.argv[3]+`/prevyu_seriya${n}.png`,Buffer.from(v.split(',')[1],'base64'));console.log('ok',n);}
process.exit(0);
