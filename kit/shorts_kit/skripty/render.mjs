import fs from 'fs';
const dir=process.argv[2], fps=30, DUR=parseFloat(process.argv[3]||"10"), N=Math.round(DUR*fps);
fs.mkdirSync(dir+'/frames',{recursive:true});
let list;for(let i=0;i<50;i++){try{list=await (await fetch('http://127.0.0.1:9333/json')).json();if(list.find(p=>p.type==='page'))break;}catch(e){}await new Promise(r=>setTimeout(r,300));}
const page=list.find(p=>p.type==='page');
const ws=new WebSocket(page.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0;const pend=new Map();ws.onmessage=m=>{const d=JSON.parse(m.data);if(pend.has(d.id)){pend.get(d.id)(d);pend.delete(d.id);}};
const send=(method,params)=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}));});
await new Promise(r=>setTimeout(r,1500));
for(let i=0;i<N;i++){const t=(i/fps).toFixed(4);
 const r=await send('Runtime.evaluate',{expression:`playing=false; T=${t}; render(${t}); document.getElementById('stage').toDataURL('image/jpeg',0.95)`,returnByValue:true});
 if(!r.result||!r.result.result||typeof r.result.result.value!=='string'){console.error('fail',i,JSON.stringify(r).slice(0,300));process.exit(1);}
 fs.writeFileSync(`${dir}/frames/f${String(i).padStart(5,'0')}.jpg`,Buffer.from(r.result.result.value.split(',')[1],'base64'));
 if(i%300===0)console.log('frame',i,'/',N);}
ws.close();console.log('done',N);
