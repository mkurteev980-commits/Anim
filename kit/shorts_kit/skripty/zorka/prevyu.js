function bigText(lines,y,size,cols){ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';ctx.font=`900 ${size}px Inter`;ctx.lineJoin='round';
 lines.forEach((l,i)=>{const yy=y+i*size*1.05;ctx.lineWidth=size*0.22;ctx.strokeStyle='#0B0B10';ctx.shadowColor='rgba(0,0,0,0.8)';ctx.shadowBlur=30;ctx.shadowOffsetY=10;ctx.strokeText(l,540,yy);ctx.shadowColor='transparent';ctx.fillStyle=cols[i]||'#fff';ctx.fillText(l,540,yy);});ctx.restore();}
function pill(txt,y,bg,fg){ctx.save();ctx.font='900 40px Inter';const w=ctx.measureText(txt).width+70;rr(540-w/2,y-38,w,76,38);ctx.fillStyle=bg;ctx.fill();ctx.lineWidth=6;ctx.strokeStyle='#0B0B10';ctx.stroke();ctx.fillStyle=fg;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(txt,540,y+2);ctx.restore();}
function COVER1(){const t=1.3,WL=1010;
 ctx.fillStyle=vgrad('#060A18','#141E36',0,WL);ctx.fillRect(0,0,W,WL);moon(880,190,70);forest(WL,'#050A12',301,200,340);
 ctx.fillStyle=vgrad('#0A1626','#020509',WL,H);ctx.fillRect(0,WL,W,H-WL);
 ctx.save();ctx.beginPath();ctx.rect(0,0,W,WL);ctx.clip();
 litPerson({kind:'masha',x:540,y:620+(690+70)*2.15,s:2.15,t,la:{a:[-0.3,0.2]},ra:{a:[0.3,-0.2]},mood:'terror',eyeS:1.25,irisS:0.75,brows:[[8,-26],[8,-26]],mouth:'scared',look:[0,9],sweat:true,noBlink:true,seed:1},{rim:{col:'rgba(190,215,255,0.9)',dx:-8,dy:-4},shade:{x0:200,y0:0,x1:900,y1:0,a:0.35}});
 ctx.restore();
 const Tm=ctx.getTransform();figX.setTransform(1,0,0,1,0,0);figX.clearRect(0,0,W,H);const p=ctx;ctx=figX;ctx.save();ctx.translate(0,2*WL);ctx.scale(1,-1);
 person({kind:'masha',x:540,y:620+(690+70)*2.15,s:2.15,t,skin:PALE,hair:'#2A1A10',dress:'#A8B8C8',la:{a:[-0.3,0.2]},ra:{a:[0.3,-0.2]},mood:'creepy',irisS:0.4,lids:[0.08,0.08],mouth:'grin',wet:true,tina:true,noBlink:true,breathe:false,seed:9});
 ctx.restore();ctx=p;ctx.save();ctx.setTransform(1,0,0,1,0,0);for(let y=WL;y<H;y+=5){const off=Math.sin(y*0.045)*7*(1+(y-WL)/500);ctx.globalAlpha=0.9;ctx.drawImage(figC,0,y,W,5,off,y,W,5);}ctx.globalAlpha=1;ctx.restore();
 ctx.strokeStyle='rgba(200,220,255,0.25)';ctx.lineWidth=3;for(let i=0;i<9;i++){const y=WL+30+i*95;ctx.beginPath();ctx.moveTo(60+i*10,y);ctx.lineTo(1020-i*10,y);ctx.stroke();}
 cap(860,WL+20,800,WL-260,26,PALE);HSC=1.6;hand(800,WL-260,-60,-280,'open',PALE);HSC=1;for(let i=0;i<16;i++){circ(860+(rnd(i)-0.5)*260,WL-20-rnd(i+5)*160,5+rnd(i+9)*9);ctx.fillStyle='rgba(180,215,255,0.8)';ctx.fill();}
 rr(-20,WL-14,W+40,28,6);fs('#3A2A1E',4);
 lightPass([{type:'radial',x:540,y:620,r:620,k:0.95,warm:0.15},{type:'radial',x:540,y:1450,r:620,k:0.85}],0.6);
 grade('#1E3C8C',0.3);const g=ctx.createLinearGradient(0,WL,0,H);g.addColorStop(0,'rgba(183,28,28,0)');g.addColorStop(1,'rgba(183,28,28,0.35)');ctx.fillStyle=g;ctx.fillRect(0,WL,W,H-WL);
 const v=ctx.createRadialGradient(540,960,500,540,960,1200);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,0.65)');ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
 pill('«ЗОРЬКА» · СЕРИЯ 1',300,'#FACC15','#111');
 bigText(['НЕ СМОТРИ','В ВОДУ'],930,138,['#FFFFFF','#E53935']);
 stamp(1.0,540,1640,'ПРАВИЛО 3 НАРУШЕНО');}
function COVER2(){const t=1.3;
 bg('ub',bgUnderBed);
 headOnly('ded',300,1090,2.0,1.3,{t,mood:'creepy',irisS:0.25,lids:[0.08,0.08],mouth:'flat',noBlink:true,eyeS:0.9});
 headOnly('gena',760,1060,2.5,-1.25,{t,mood:'creepy',irisS:0.45,lids:[0.22,0.22],mouth:'grin',noBlink:true});
 bedBand();
 HSC=1.6;hand(150,1840,0.3,-1,'open','#F6CFAE');hand(330,1870,-0.2,-1,'open','#F6CFAE');HSC=1;
 lightPass([{type:'radial',x:640,y:1350,r:760,k:1,warm:0.35},{type:'radial',x:300,y:1100,r:420,k:0.7}],0.85);
 ctx.save();ctx.globalCompositeOperation='lighter';const g=ctx.createRadialGradient(660,1360,0,660,1360,300);g.addColorStop(0,'rgba(255,240,200,0.85)');g.addColorStop(1,'rgba(255,220,150,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore();
 ctx.save();ctx.globalCompositeOperation='lighter';[[260,1120],[340,1120]].forEach(([x,y])=>{const gg=ctx.createRadialGradient(x,y,0,x,y,40);gg.addColorStop(0,'rgba(220,245,255,0.8)');gg.addColorStop(1,'rgba(220,245,255,0)');ctx.fillStyle=gg;ctx.fillRect(x-40,y-40,80,80);});ctx.restore();
 grade('#B71C1C',0.3,'overlay');
 const v=ctx.createRadialGradient(540,960,500,540,960,1200);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,0.6)');ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
 pill('«ЗОРЬКА» · СЕРИЯ 2',360,'#FACC15','#111');
 bigText(['ДЕД ТОЖЕ','ИЗ НИХ?!'],1470,140,['#FFFFFF','#E53935']);}
