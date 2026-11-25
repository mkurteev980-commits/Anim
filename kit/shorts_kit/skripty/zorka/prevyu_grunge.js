function splat(x,y,r,seed,col){ctx.fillStyle=col;circ(x,y,r);ctx.fill();for(let i=0;i<14;i++){const a=rnd(seed+i)*Math.PI*2,d=r*(0.8+rnd(seed+i+30)*1.6),s=r*(0.08+rnd(seed+i+60)*0.25);circ(x+Math.cos(a)*d,y+Math.sin(a)*d,s);ctx.fill();}for(let i=0;i<5;i++){const xx=x+(rnd(seed+i+90)-0.5)*r*1.4;const len=r*(0.6+rnd(seed+i+120)*1.8);rr(xx-r*0.06,y,r*0.12,len,r*0.06);ctx.fill();circ(xx,y+len,r*0.1);ctx.fill();}}
function grungeTitle(txt,y,size,skew=-0.14){ctx.save();ctx.translate(540,y);ctx.transform(1,0,skew,1,0,0);ctx.font=`900 ${size}px Inter`;ctx.textAlign='center';ctx.textBaseline='middle';
 const w=ctx.measureText(txt).width;if(w>1000){const k=1000/w;ctx.scale(k,k);}
 splat(-w*0.28,-size*0.05,size*0.42,11,'rgba(190,14,14,0.95)');splat(w*0.3,size*0.08,size*0.36,23,'rgba(190,14,14,0.95)');splat(w*0.02,-size*0.15,size*0.3,37,'rgba(170,10,10,0.9)');for(let i=0;i<9;i++)splat((rnd(i+3)-0.5)*w*0.9,(rnd(i+7)-0.5)*size*0.5,size*0.12,i*17,'rgba(200,16,16,0.95)');
 ctx.lineJoin='round';ctx.lineWidth=size*0.16;ctx.strokeStyle='#0A0A0A';ctx.strokeText(txt,8,10);ctx.strokeText(txt,0,0);
 ctx.fillStyle='#F2F0EA';ctx.fillText(txt,0,0);
 ctx.save();ctx.globalCompositeOperation='source-atop';ctx.fillStyle='rgba(10,10,10,0.9)';for(let i=0;i<420;i++){const xx=(rnd(i+200)-0.5)*w,yy=(rnd(i+500)-0.5)*size;ctx.beginPath();ctx.ellipse(xx,yy,2+rnd(i+800)*7,1+rnd(i+900)*3,rnd(i)*3,0,Math.PI*2);ctx.fill();}
 ctx.strokeStyle='rgba(10,10,10,0.85)';ctx.lineWidth=3;for(let i=0;i<40;i++){const xx=(rnd(i+1200)-0.5)*w,yy=(rnd(i+1300)-0.5)*size;ctx.beginPath();ctx.moveTo(xx,yy);ctx.lineTo(xx+30+rnd(i)*60,yy+(rnd(i+5)-0.5)*10);ctx.stroke();}ctx.restore();
 ctx.fillStyle='rgba(200,16,16,0.95)';for(let i=0;i<6;i++){const xx=(rnd(i+1500)-0.5)*w*0.9;const len=size*(0.25+rnd(i+1600)*0.5);rr(xx-6,size*0.3,12,len,6);ctx.fill();circ(xx,size*0.3+len,9);ctx.fill();}
 ctx.restore();}
function ribbon(txt,y,rot,bg,fg,size,pad){ctx.save();ctx.translate(540,y);ctx.rotate(rot);ctx.font=`900 ${size}px Inter`;const w=ctx.measureText(txt).width+pad*2,h=size*1.25;
 ctx.beginPath();ctx.moveTo(-w/2-20,-h/2);ctx.lineTo(w/2+10,-h/2+4);ctx.lineTo(w/2+24,h/2);ctx.lineTo(-w/2-8,h/2-4);ctx.closePath();ctx.fillStyle=bg;ctx.fill();ctx.lineWidth=7;ctx.strokeStyle='#0A0A0A';ctx.stroke();
 ctx.fillStyle=fg;ctx.textAlign='center';ctx.textBaseline='middle';if(fg==='#F2F0EA'){ctx.lineWidth=size*0.14;ctx.strokeStyle='#0A0A0A';ctx.strokeText(txt,0,4);}ctx.fillText(txt,0,4);ctx.restore();}
function corners(){ctx.strokeStyle='#D81B1B';ctx.lineWidth=12;ctx.lineCap='square';ctx.beginPath();ctx.moveTo(40,170);ctx.lineTo(40,60);ctx.lineTo(150,60);ctx.moveTo(1040,170);ctx.lineTo(1040,60);ctx.lineTo(930,60);ctx.stroke();}
function header(title,part,sub){grungeTitle(title,215,250);ribbon(part,420,-0.05,'#D81B1B','#F2F0EA',92,40);ribbon(sub,535,-0.03,'#F2F0EA','#0A0A0A',58,34);corners();}
function COVER1(){const t=1.3;
 ctx.fillStyle=vgrad('#05070F','#101A30',0,1150);ctx.fillRect(0,0,W,1150);moon(860,760,80);forest(1150,'#04080E',401,260,420);
 ctx.fillStyle=vgrad('#0B1626','#020408',1150,H);ctx.fillRect(0,1150,W,H-1150);
 ctx.strokeStyle='rgba(244,241,220,0.35)';ctx.lineWidth=5;for(let i=0;i<12;i++){const y=1170+i*36,w=60+rnd(i)*120;ctx.beginPath();ctx.moveTo(860-w/2,y);ctx.lineTo(860+w/2,y);ctx.stroke();}
 [[180,1230,0.55],[330,1250,0.6],[470,1225,0.5]].forEach(([x,y,s],i)=>{ctx.save();ctx.beginPath();ctx.rect(0,0,W,y+20);ctx.clip();headOnly('kid',x,y,s,0,{t,skin:PALE,hair:shade(KIDS[i].hair,-0.4),girl:KIDS[i].girl,mood:'creepy',irisS:0.3,mouth:'flat',wet:true,noBlink:true});ctx.restore();ctx.beginPath();ctx.ellipse(x,y+22,70*s*1.6,12,0,0,Math.PI*2);ctx.strokeStyle='rgba(200,220,255,0.4)';ctx.lineWidth=3;ctx.stroke();});
 const F=[840,1010];litPerson({kind:'gena',x:740,y:2200,s:1.8,t,ra:{to:F,hand:'fist'},la:{a:[-0.15,0.1]},mood:'creepy',lids:[0.25,0.25],irisS:0.55,mouth:'grin',whistle:true,noBlink:true,seed:5},{rim:{col:'rgba(150,180,255,0.9)',dx:8,dy:-4},shade:{x0:0,y0:1000,x1:0,y1:600,a:0.5,warm:[800,900,360]}});flashlight(F[0],F[1],-Math.PI/2-0.7);
 litPerson({kind:'masha',x:250,y:1560+(690+70)*2.5,s:2.5,t,la:{a:[0.3,2.2],hand:'open'},ra:{a:[0.3,-0.2]},turn:1,mood:'terror',eyeS:1.25,irisS:0.7,brows:[[8,-26],[8,-26]],mouth:'scared',look:[10,-3],sweat:true,noBlink:true,seed:1},{rim:{col:'rgba(255,90,90,0.9)',dx:8,dy:-6},shade:{x0:0,y0:0,x1:600,y1:0,a:0.4}});
 lightPass([{type:'radial',x:800,y:900,r:620,k:1,warm:0.35},{type:'radial',x:260,y:1560,r:520,k:0.85},{type:'radial',x:860,y:760,r:400,k:0.6}],0.7);
 const g=ctx.createLinearGradient(0,0,W,0);g.addColorStop(0,'rgba(200,20,20,0.28)');g.addColorStop(0.5,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(40,80,200,0.25)');ctx.fillStyle=g;ctx.fillRect(0,600,W,1320);
 const tg=ctx.createLinearGradient(0,0,0,700);tg.addColorStop(0,'rgba(0,0,0,0.85)');tg.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=tg;ctx.fillRect(0,0,W,700);
 header('ЗОРЬКА','ЧАСТЬ 1','ПРАВИЛА ЛАГЕРЯ');}
function COVER2(){const t=1.3;
 ctx.fillStyle='#4A3022';ctx.fillRect(0,0,W,H);for(let y=560;y<1700;y+=70){rr(-20,y,W+40,66,33);fs('#5E3E28',4);}
 rr(380,640,500,1180,6);fs('#2A1E16',6);ctx.fillStyle=vgrad('#F2C46D','#A8642A',660,1820);ctx.fillRect(400,660,460,1160);
 litPerson({kind:'ded',x:640,y:1880,s:1.3,t,la:{to:[500,1300],hand:'fist'},ra:{a:[0.2,-0.1]},mood:'creepy',irisS:0.2,lids:[0.08,0.08],eyeS:0.95,mouth:'flat',noBlink:true,seed:7},{rim:{col:'rgba(255,200,120,0.95)',dx:8,dy:-6},shade:{x0:0,y0:1600,x1:0,y1:800,a:0.5}});lantern(500,1360,t);
 headOnly('gena',870,980,1.15,0.15,{t,mood:'creepy',irisS:0.45,lids:[0.2,0.2],mouth:'grin',noBlink:true});
 rr(-20,1500,560,60,12);fs('#6B4A30',5);ctx.fillStyle='#7A3A2E';ctx.beginPath();ctx.moveTo(-20,1540);ctx.lineTo(540,1540);ctx.lineTo(540,1640);for(let x=540;x>=-20;x-=36)ctx.lineTo(x,1640+(x/36%2?12:-4));ctx.closePath();ctx.fill();ctx.lineWidth=5;ctx.strokeStyle=OL;ctx.stroke();
 headOnly('masha',230,1790,1.9,-0.1,{t,mood:'terror',eyeS:1.25,irisS:0.7,brows:[[8,-26],[8,-26]],mouth:'scared',look:[10,-6],sweat:true,noBlink:true});HSC=1.7;hand(60,1900,0.4,-1,'open','#F6CFAE');hand(430,1910,-0.4,-1,'open','#F6CFAE');HSC=1;
 lightPass([{type:'radial',x:520,y:1350,r:650,k:1,warm:0.4},{type:'radial',x:230,y:1780,r:420,k:0.8},{type:'radial',x:870,y:980,r:300,k:0.6}],0.72);
 ctx.save();ctx.globalCompositeOperation='lighter';[[588,890],[692,890]].forEach(([x,y])=>{const gg=ctx.createRadialGradient(x,y,0,x,y,46);gg.addColorStop(0,'rgba(220,245,255,0.9)');gg.addColorStop(1,'rgba(220,245,255,0)');ctx.fillStyle=gg;ctx.fillRect(x-46,y-46,92,92);});ctx.restore();
 const g=ctx.createLinearGradient(0,0,W,0);g.addColorStop(0,'rgba(200,20,20,0.3)');g.addColorStop(0.55,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(40,80,200,0.25)');ctx.fillStyle=g;ctx.fillRect(0,600,W,1320);
 const tg=ctx.createLinearGradient(0,0,0,760);tg.addColorStop(0,'rgba(0,0,0,0.9)');tg.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=tg;ctx.fillRect(0,0,W,760);
 header('ЗОРЬКА','ЧАСТЬ 2','СТОРОЖ');}
