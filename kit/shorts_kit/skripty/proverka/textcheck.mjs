// node textcheck.mjs <port> <DUR> <out.json>
import fs from 'fs';
const [port,DUR,out]=[process.argv[2],parseFloat(process.argv[3]),process.argv[4]];
const list=await (await fetch(`http://127.0.0.1:${port}/json`)).json();const page=list.find(p=>p.type==='page');
const ws=new WebSocket(page.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);let id=0;const pend=new Map();ws.onmessage=m=>{const d=JSON.parse(m.data);if(pend.has(d.id)){pend.get(d.id)(d);pend.delete(d.id);}};
const send=(method,params)=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}));});
await new Promise(r=>setTimeout(r,2000));
const inject=`(()=>{if(window.__QA)return 'already';window.__QA=1;window.__REC=[];window.__SRC=null;let inst=0;
const P=CanvasRenderingContext2D.prototype;
function rec(ctx,text,x,y){if(ctx!==mainCtx||!text||!String(text).trim())return;const m=ctx.getTransform();const w=ctx.measureText(text).width;const fm=/(\\d+)px/.exec(ctx.font);const h=fm?parseFloat(fm[1]):20;
 let x0=x;if(ctx.textAlign==='center')x0=x-w/2;else if(ctx.textAlign==='right'||ctx.textAlign==='end')x0=x-w;
 let y0=y-h*0.8;if(ctx.textBaseline==='middle')y0=y-h/2;else if(ctx.textBaseline==='top')y0=y;
 const pts=[[x0,y0],[x0+w,y0],[x0,y0+h],[x0+w,y0+h]].map(([a,b])=>[m.a*a+m.c*b+m.e,m.b*a+m.d*b+m.f]);
 const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);window.__REC.push({src:window.__SRC||'art',text:String(text),b:[Math.min(...xs),Math.min(...ys),Math.max(...xs),Math.max(...ys)],a:ctx.globalAlpha});}
const of=P.fillText;P.fillText=function(t,x,y,mw){rec(this,t,x,y);return of.call(this,t,x,y,mw);};
['drawSubs','bubble','plate','burst','stamp','brackets','bigNum','cta','head2','lbl','vtag','tag'].forEach(n=>{if(typeof window[n]!=='function')return;const f=window[n];window[n]=function(...a){const prev=window.__SRC;if(!prev||prev==='art'||prev.startsWith('scene'))window.__SRC=n+'#'+(++inst);try{return f.apply(this,a);}finally{window.__SRC=prev;}};});
return 'ok';})()`;
console.log((await send('Runtime.evaluate',{expression:inject,returnByValue:true})).result.result.value);
const res=[];const N=Math.round(DUR*30);
for(let i=0;i<N;i+=2){const t=(i/30).toFixed(4);const r=await send('Runtime.evaluate',{expression:`(()=>{__REC=[];playing=false;render(${t});return JSON.stringify(__REC);})()`,returnByValue:true});res.push({t:+t,r:JSON.parse(r.result.result.value)});}
fs.writeFileSync(out,JSON.stringify(res));console.log('frames',res.length);process.exit(0);
