let D,state={level:'ALL',metric:'multiple',selected:null,experiment:null,step:0,timer:null};
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const money=n=>(n<0?'−':'')+'$'+Math.abs(Math.round(n)).toLocaleString('en-US');
const compact=n=>{let a=Math.abs(n),s=a>=1e6?'$'+(a/1e6).toFixed(2)+'M':'$'+Math.round(a/1000)+'K';return n<0?'−'+s:s};
const signed=n=>(n>=0?'+':'−')+compact(Math.abs(n)).replace('−','');

/* Level 3 replay: each run as it was played (figures from the game's result screens) */
const STEPS=[
 {run:'Run 1',total:10637554,delta:null,tag:'Baseline',changed:'Roasting in Emerging Markets, the maximum franchises in both markets, and only 2 Emerging own stores.',why:'Year 1 Emerging profit was only $34,238, so from Year 2 I stopped opening own stores there.',result:'$10.64M, 213% of target. With hindsight, the Emerging Market was under-built.'},
 {run:'Run 2',total:11590330,delta:952776,tag:'Kept',changed:'Three more Emerging own stores a year in Years 2–4 (11 in total). Nothing else changed.',why:'Run 1 showed each Emerging store’s yearly contribution rising from about $18,000 in Year 2 to about $108,000 by Year 5.',result:'Profit trailed Run 1 by $248K after Year 2, overtook in Year 4 and finished $953K ahead.'},
 {run:'Run 3',total:12332111,delta:741781,tag:'Kept',changed:'Roasting moved from Emerging to Mature Markets. Nothing else changed.',why:'Roasting lifted Emerging sales by only 2–4%, while Mature customers valued quality and sustainability.',result:'Mature profit +$584K, and Emerging +$158K without the roasters: +$742K in total.'},
 {run:'Run 4',total:12174325,delta:-157786,tag:'Reversed',changed:'Roasting in both markets, compared with Run 3.',why:'To test whether Emerging roasting pays once prices and volumes rise.',result:'Exactly Run 3’s Mature result plus Run 2’s Emerging result: Emerging roasting still lost $158K, so it was dropped.'},
 {run:'Run 5',total:12501031,delta:168920,vs:'vs Run 3',tag:'Best run',changed:'Run 3 plus a third Emerging own store in Year 1.',why:'Run 3’s store economics suggested one more early store would add about $180K.',result:'−$87K in Year 1, level by Year 3, then $169K ahead: $12.50M, 250% of target.'}];

/* People, planet, profit scorecard (from the run logs) */
const SCORE=[
 {c:'Organic beans',src:'Level 2 · test E8',p:['0','No direct effect'],pl:['+','Certified sustainable sourcing'],pr:['+','+$49,916 over five years']},
 {c:'Fair Trade + organic beans',src:'Level 3 · Mature, Year 1',p:['+','Fair prices for farmers'],pl:['+','Sustainable sourcing'],pr:['+','+$46,938 in Year 1 alone']},
 {c:'Roast our own beans',src:'Level 2 · test E7',p:['0','No direct effect'],pl:['0','No direct effect'],pr:['+','+$134,049 over five years']},
 {c:'Keep one extra job for five years',src:'Level 2 · test E9',p:['+','One more job, every year'],pl:['0','No direct effect'],pr:['-','−$122,794 over five years']},
 {c:'$1,000 pay lead instead of $2,000',src:'Level 1 · test E4',p:['=','Staff stayed at 5 stars'],pl:['0','No direct effect'],pr:['+','+$14,359 over two years']}];

fetch('data.json').then(r=>{if(!r.ok)throw Error('data.json missing');return r.json()}).then(x=>{D=x;state.selected=x.runs[0];state.experiment=x.experiments.find(e=>e.ID==='E13')||x.experiments[0];init()}).catch(e=>document.body.insertAdjacentHTML('afterbegin','<div style="padding:12px;background:#a33;color:white">Data failed to load: '+e.message+'</div>'));

function init(){
 let io=new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting&&e.target.classList.add('visible')),{threshold:.08});$$('.reveal').forEach(x=>io.observe(x));
 $$('#levelTabs button').forEach(b=>b.onclick=()=>{state.level=b.dataset.level;$$('#levelTabs button').forEach(x=>x.classList.toggle('active',x===b));let f=runs();if(!f.includes(state.selected))state.selected=f[0];render()});
 $$('.metric-toggle button').forEach(b=>b.onclick=()=>{state.metric=b.dataset.metric;$$('.metric-toggle button').forEach(x=>x.classList.toggle('active',x===b));renderChart()});
 $('#runSelect').onchange=e=>{state.selected=D.runs.find(x=>x.Label===e.target.value);renderDetail();renderTrajectory();renderChart()};
 $('#theme').onclick=()=>document.body.classList.toggle('dark');$('#export').onclick=exportCSV;
 $('#prevRun').onclick=()=>{stop();setStep(state.step-1)};$('#nextRun').onclick=()=>{stop();setStep(state.step+1)};$('#playRuns').onclick=play;
 let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{renderTrajectory();renderReplay()},150)});
 renderKpis();renderScore();render();setStep(0)}

const runs=()=>D.runs.filter(r=>state.level==='ALL'||r.Level===state.level);
const pct=r=>r['Game total ($)']/r['Target ($)'];
function avg(a,f){return a.reduce((s,x)=>s+f(x),0)/a.length}
function render(){renderChart();renderDetail();renderTrajectory();renderLevels();renderImpact();renderRules();$('#runSelect').innerHTML=runs().map(x=>`<option ${x===state.selected?'selected':''} value="${x.Label}">${x.Label}</option>`).join('')}

function count(el,end,fmt){let t0=performance.now();function f(t){let p=Math.min(1,(t-t0)/650),v=end*(1-Math.pow(1-p,3));el.textContent=fmt(v);p<1&&requestAnimationFrame(f)}requestAnimationFrame(f)}
function renderKpis(){
 let beat=D.runs.filter(r=>r['Game total ($)']>=r['Target ($)']).length,best=D.runs.reduce((a,b)=>pct(a)>pct(b)?a:b),l3=D.runs.filter(r=>r.Level==='L3'),gain=l3[4]['Game total ($)']-l3[0]['Game total ($)'],top=D.experiments.reduce((a,b)=>a['Profit effect ($)']>b['Profit effect ($)']?a:b);
 let items=[['Runs that beat the target',beat,v=>Math.round(v)+'/'+D.runs.length,'Only the low-price Campus run missed','var(--sage)',beat/D.runs.length*100],
  ['Best result',pct(best)*100,v=>Math.round(v)+'%',`of target · ${best.Label} (${compact(best['Game total ($)'])})`,'var(--copper)',100],
  ['Gained by testing in Level 3',gain,v=>'+'+compact(v),'Run 1 → Run 5, one change at a time','var(--teal)',80],
  ['Biggest single lever',top['Profit effect ($)'],v=>'+'+compact(v),`${top['What changed'].replace(/, Years.*$/,'')} (${top.ID})`,'var(--caramel)',65]];
 $('#kpis').innerHTML=items.map((x,i)=>`<article class="kpi" style="--accent:${x[4]};--pct:${x[5]}%"><label>${x[0]}</label><strong id="k${i}">—</strong><small>${x[3]}</small></article>`).join('');items.forEach((x,i)=>count($('#k'+i),x[1],x[2]))}

function color(level){return level==='L1'?'var(--sage)':level==='L2'?'var(--caramel)':'var(--copper)'}
function renderChart(){
 let a=runs(),m=state.metric,val=r=>m==='multiple'?pct(r)*100:r['Game total ($)'],max=Math.max(...a.map(val),m==='multiple'?100:0),base=m==='multiple'?100/max*90:null;
 $('#chartTitle').textContent=m==='multiple'?'Result as % of target':'Five-year profit by run';
 $('#runChart').innerHTML=(base?`<div class="target-line" style="--base:${base}"><span>target</span></div>`:'')+a.map((r,i)=>{let v=val(r),h=Math.max(4,v/max*90),lab=m==='multiple'?Math.round(v)+'%':compact(v),parts=r.Label.split(' '),miss=r['Game total ($)']<r['Target ($)'];
  return `<button class="bar-wrap ${r===state.selected?'selected':''}" data-label="${r.Label}" aria-label="${r.Label}: ${money(r['Game total ($)'])}, ${Math.round(pct(r)*100)}% of target"><div class="value">${lab}</div><div class="bar" style="--h:${h}%;--accent:${miss?'var(--coral)':color(r.Level)};--delay:${i*45}ms"></div><small>${parts[0]} ${parts[1]}<br><em>${parts.slice(2).join(' ')||'&nbsp;'}</em></small></button>`}).join('');
 $$('.bar-wrap').forEach(el=>{let r=D.runs.find(x=>x.Label===el.dataset.label);el.onclick=()=>{state.selected=r;renderChart();renderDetail();renderTrajectory();$('#runSelect').value=r.Label};el.onmousemove=e=>tip(e,`<b>${r.Label}</b><br>${money(r['Game total ($)'])} five-year profit<br>${Math.round(pct(r)*100)}% of target<br>${r['Strategy (one line)']}`);el.onmouseleave=()=>$('#tip').hidden=true})}
function renderDetail(){let r=state.selected,d=r['Game total ($)']-r['Target ($)'];$('#runDetail').innerHTML=`<h2>${r.Label}</h2><p class="strategy">${r['Strategy (one line)']}</p><div class="metric-row"><span>Five-year profit</span><b>${money(r['Game total ($)'])}</b></div><div class="metric-row"><span>Target</span><b>${money(r['Target ($)'])}</b></div><div class="metric-row"><span>Above or below target</span><b class="${d>=0?'pos':'neg'}">${signed(d)}</b></div><div class="metric-row"><span>Result vs target</span><b>${Math.round(pct(r)*100)}%</b></div>`}

function series(r){if(r.Level!=='L3')return D.l12.filter(x=>'L'+x.Level===r.Level&&x.Run===r.Run).map(x=>({y:x.Year,v:x['Operating profit ($)']}));let z=D.l3.filter(x=>x.Run===r.Run);return[1,2,3,4,5].map(y=>({y,v:z.filter(x=>x.Year===y).reduce((s,x)=>s+(x['Operating profit ($)']||0),0)}))}
function renderTrajectory(){let el=$('#trajectory'),s=series(state.selected),W=Math.max(300,el.clientWidth||680),H=260,p={l:62,r:18,t:18,b:34},vals=s.map(x=>x.v),mn=Math.min(0,...vals),mx=Math.max(...vals)*1.1,sy=v=>p.t+(mx-v)/(mx-mn)*(H-p.t-p.b),sx=i=>p.l+i*(W-p.l-p.r)/(s.length-1),pts=s.map((x,i)=>sx(i)+','+sy(x.v)).join(' ');
 let grid=[0,.5,1].map(t=>{let v=mn+(mx-mn)*t,y=sy(v);return `<line class="gridline" x1="${p.l}" y1="${y}" x2="${W-p.r}" y2="${y}"/><text class="axis" x="${p.l-8}" y="${y+4}" text-anchor="end">${compact(v)}</text>`}).join('');
 let dots=s.map((x,i)=>`<circle class="dot" style="animation-delay:${800+i*100}ms" cx="${sx(i)}" cy="${sy(x.v)}" r="5"><title>Year ${x.y}: ${money(x.v)}</title></circle><text class="axis" x="${sx(i)}" y="${H-8}" text-anchor="middle">Year ${x.y}</text>`).join('');
 el.innerHTML=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Operating profit by year for ${state.selected.Label}">${grid}<polyline class="line" points="${pts}"/>${dots}</svg>`;
 let d=s.at(-1).v-s[0].v;$('#trajectoryNote').textContent=(state.selected.Level==='L3'?'Mature + Emerging market operating profit by year. ':'Operating profit by year, as the game reported it. ')+`Year 1 to Year 5 change: ${signed(d)}.`}
function renderLevels(){let a=['L1','L2','L3'].map(l=>{let z=D.runs.filter(x=>x.Level===l);return{l,avg:avg(z,x=>x['Game total ($)']),mult:avg(z,pct),c:color(l)}});let mm=Math.max(...a.map(x=>x.mult));$('#levelCards').innerHTML=a.map(x=>`<div class="level-card"><b>${x.l}</b><div><div class="mini"><i style="--w:${x.mult/mm*100}%;--accent:${x.c}"></i></div><small>${Math.round(x.mult*100)}% of target on average</small></div><strong>${compact(x.avg)}</strong></div>`).join('')}

function renderImpact(){let a=[...D.experiments].sort((x,y)=>Math.abs(y['Profit effect ($)'])-Math.abs(x['Profit effect ($)'])),max=Math.max(...a.map(x=>Math.abs(x['Profit effect ($)'])));
 $('#impactAxis').innerHTML='<div class="axis-zero"></div><span class="axis-side neg">← PROFIT LOST</span><span class="axis-side pos">PROFIT GAINED →</span>'+a.map((x,i)=>{let v=x['Profit effect ($)'],w=Math.max(4,Math.abs(v)/max*43);return `<button class="impact ${v>=0?'pos':'neg'} ${x.ID===state.experiment.ID?'active':''}" data-id="${x.ID}" aria-label="${x.ID}: ${x.Question} ${signed(v)}" style="--y:${8+i*6.5}%;--w:${w}%;--delay:${i*35}ms"><span>${x.ID} · ${signed(v)}</span></button>`}).join('');
 $$('.impact').forEach(el=>{el.onclick=()=>{state.experiment=D.experiments.find(x=>x.ID===el.dataset.id);renderImpact()}});
 let x=state.experiment,v=x['Profit effect ($)'],q=x['Evidence quality']==='Good'?'Good evidence (location test)':'Clean one-variable test';
 $('#decisionStory').innerHTML=`<span class="pill">${x.ID} · ${x.Pillar} · ${q}</span><h3>${x.Question}</h3><div class="effect">${signed(v)}</div><p><b>What changed:</b> ${x['What changed']}</p><p><b>What happened:</b> ${x.Conclusion}</p><div class="why"><small>RUNS COMPARED</small><p>${x['Runs compared']}</p><small>WHAT IT MEANS</small><p>${x['Strategic reading']}</p></div>`}

/* ---------- Level 3 replay ---------- */
function setStep(i){state.step=Math.max(0,Math.min(STEPS.length-1,i));renderReplay()}
function stop(){if(state.timer){clearInterval(state.timer);state.timer=null;$('#playRuns').textContent='▶ Play'}}
function play(){if(state.timer){stop();return}if(state.step>=STEPS.length-1)setStep(0);$('#playRuns').textContent='❚❚ Pause';state.timer=setInterval(()=>{if(state.step>=STEPS.length-1){stop();return}setStep(state.step+1)},2400)}
function renderReplay(){
 let i=state.step,st=STEPS[i];
 $('#stepper').innerHTML=STEPS.map((s,j)=>`<button class="${j===i?'active':''} ${j<i?'done':''}" data-j="${j}" aria-pressed="${j===i}">${s.run}</button>`).join('');
 $$('#stepper button').forEach(b=>b.onclick=()=>{stop();setStep(+b.dataset.j)});
 $('#prevRun').disabled=i===0;$('#nextRun').disabled=i===STEPS.length-1;
 let el=$('#replayChart'),W=Math.max(300,el.clientWidth||600),H=300,p={l:66,r:14,t:34,b:34},lo=10e6,hi=12.75e6,sy=v=>p.t+(hi-v)/(hi-lo)*(H-p.t-p.b),bw=(W-p.l-p.r)/STEPS.length;
 let grid=[10,10.5,11,11.5,12,12.5].map(m=>{let y=sy(m*1e6);return `<line class="gridline" x1="${p.l}" y1="${y}" x2="${W-p.r}" y2="${y}"/><text class="axis" x="${p.l-8}" y="${y+4}" text-anchor="end">$${m.toFixed(1)}M</text>`}).join('');
 let target=`<text class="axis" x="${p.l}" y="${p.t-16}">Five-year profit (axis starts at $10M; target was $5M)</text>`;
 let bars=STEPS.map((s,j)=>{let x=p.l+j*bw+bw*.18,w=bw*.64,y=sy(s.total),h=sy(lo)-y,cls=j>i?'ghost':j===i?(s.delta<0?'now neg':'now'):(s.tag==='Reversed'?'past rev':'past');
  let lab=j<=i?`<text class="rv" x="${x+w/2}" y="${y-8}" text-anchor="middle">${compact(s.total)}</text>`:'';
  return `<rect class="rbar ${cls}" x="${x}" y="${y}" width="${w}" height="${h}" rx="5"><title>${s.run}: ${money(s.total)}</title></rect>${lab}<text class="axis" x="${x+w/2}" y="${H-10}" text-anchor="middle">${s.run}</text>`}).join('');
 el.innerHTML=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Level 3 five-year profit, Runs 1 to ${i+1}">${target}${grid}${bars}</svg>`;
 let d=st.delta==null?'':`<div class="effect ${st.delta<0?'neg':''}">${signed(st.delta)} <small>${st.vs||'vs previous run'}</small></div>`;
 $('#replayStory').innerHTML=`<span class="pill">${st.run} · ${st.tag}</span><h3>${compact(st.total)}</h3>${d}<p><b>What changed:</b> ${st.changed}</p><p><b>Why I tried it:</b> ${st.why}</p><div class="why"><small>WHAT HAPPENED</small><p>${st.result}</p></div>`}

/* ---------- scorecard ---------- */
function chip(c){let m={'+':['up','Helps'],'-':['down','Hurts'],'=':['flat','Held'],'0':['none','No effect']}[c[0]];return `<div class="cell" role="cell"><span class="chip ${m[0]}" aria-label="${m[1]}">${c[0]==='0'?'—':c[0]==='-'?'−':c[0]}</span><small>${c[1]}</small></div>`}
function renderScore(){$('#scoreTable').innerHTML=`<div class="srow head" role="row"><div role="columnheader">Choice I tested</div><div role="columnheader">People</div><div role="columnheader">Planet</div><div role="columnheader">Profit</div></div>`+SCORE.map(s=>`<div class="srow" role="row"><div class="choice" role="cell"><b>${s.c}</b><small>${s.src}</small></div>${chip(s.p)}${chip(s.pl)}${chip(s.pr)}</div>`).join('')}

function renderRules(){$('#rules').innerHTML=D.rules.map(r=>`<article class="rule"><strong>0${r.ID}</strong><span class="sit">${r.Question}</span><h3>${r['What changed']}</h3><p class="ev"><b>Evidence:</b> ${String(r['Runs compared']).replace(/\bE(\d+)/g,'test E$1')}</p><p class="cav"><b>May not hold:</b> ${r.Conclusion}</p></article>`).join('')}
function tip(e,html){let t=$('#tip');t.innerHTML=html;t.hidden=false;t.style.left=Math.min(innerWidth-280,e.clientX+14)+'px';t.style.top=Math.min(innerHeight-120,e.clientY+14)+'px'}
function exportCSV(){let h=['Level','Run','Label','Strategy (one line)','Game total ($)','Target ($)','% of target'],csv=[h.join(','),...runs().map(r=>h.map(k=>'"'+String(r[k]??'').replaceAll('"','""')+'"').join(','))].join('\n'),b=new Blob([csv],{type:'text/csv'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='coffee-shop-simulation-runs.csv';a.click();URL.revokeObjectURL(u)}

/* ---------- public visitor counts (GoatCounter; cached up to 4 hours; hidden until available) ---------- */
function visitorCounts(){const base='https://shabcoffee.goatcounter.com/counter/',get=p=>fetch(base+p+'.json').then(r=>r.ok?r.json():null).catch(()=>null);
 get('TOTAL').then(t=>{if(t&&t.count){let el=$('#visits');el.querySelector('b').textContent=t.count;el.hidden=false}});
 get('/report.html').then(r=>{if(r&&r.count){let el=$('#reportCount');el.textContent='Opened '+r.count+(r.count==='1'?' time':' times');el.hidden=false}})}
visitorCounts();

/* ---------- Living latte art: each pattern blooms in, rests, then dissolves ---------- */
(function(){
 const NS='http://www.w3.org/2000/svg',RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const clamp=v=>Math.max(0,Math.min(1,v)),ease=p=>1-Math.pow(1-p,3),smooth=p=>p*p*(3-2*p);
 const cups=[];
 document.querySelectorAll('.cup-journey .cup-scene').forEach((scene,ci)=>{
  const art=scene.querySelector('.latte .art'),g=art&&art.querySelector('g');if(!g)return;
  const blob=g.querySelector('.blob');
  if(RM){if(blob)blob.remove();return}
  const items=[...g.children].map(el=>{
   if(el.getAttribute('stroke')){const L=el.getTotalLength();el.style.strokeDasharray=L;el.style.strokeDashoffset=L;return{el,stroke:true,L}}
   const w=document.createElementNS(NS,'g');el.replaceWith(w);w.appendChild(el);const b=w.getBBox();
   return{el:w,blob:el.classList.contains('blob'),cx:b.x+b.width/2,cy:b.y+b.height/2}});
  let t=0.3;
  items.forEach(it=>{if(it.blob){it.s=t;it.d=1.6;t+=1.1}else if(it.stroke){it.s=t;it.d=0.5+it.L/70;t+=it.d*0.8}else{it.s=t;it.d=1.0;t+=0.2}});
  const built=Math.max(...items.map(it=>it.s+it.d)),hold=3.6,diss=1.6,gap=0.7;
  cups.push({art,items,built,hold,diss,cycle:built+hold+diss+gap,offset:ci*1.6});
 });
 if(!cups.length)return;
 let visible=true;
 const hero=document.querySelector('.cup-journey');
 if(hero&&'IntersectionObserver'in window)new IntersectionObserver(e=>{visible=e[0].isIntersecting;if(visible)requestAnimationFrame(frame)}).observe(hero);
 function frame(now){
  if(!visible)return;
  const T=now/1000;
  cups.forEach(c=>{
   let t=(T-c.offset)%c.cycle;if(t<0)t+=c.cycle;
   const d=smooth(clamp((t-c.built-c.hold)/c.diss));
   const sway=Math.sin(t*0.9)*1.4*(1-d);
   c.art.style.opacity=1-d;
   c.art.style.filter=d?`blur(${(d*5).toFixed(2)}px)`:'none';
   c.art.style.transform=`rotate(${(sway+d*14).toFixed(2)}deg) scale(${(1+d*0.12).toFixed(3)})`;
   c.items.forEach(it=>{
    const p=clamp((t-it.s)/it.d);
    if(it.stroke){it.el.style.strokeDashoffset=(it.L*(1-ease(p))).toFixed(2);it.el.style.opacity=p>0?1:0;return}
    let sc,op;
    if(it.blob){sc=0.2+0.8*ease(clamp(p/0.6));op=clamp(p*4)*(1-smooth(clamp((p-0.55)/0.45)))}
    else{const e=ease(p);sc=0.6+0.4*e;op=smooth(clamp(p*1.4))}
    it.el.setAttribute('transform',`translate(${it.cx} ${it.cy}) scale(${sc.toFixed(3)}) translate(${-it.cx} ${-it.cy})`);
    it.el.style.opacity=op.toFixed(3);
   });
  });
  requestAnimationFrame(frame);
 }
 requestAnimationFrame(frame);
})();
