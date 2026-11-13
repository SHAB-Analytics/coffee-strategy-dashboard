import openpyxl, json, os, zipfile, shutil, statistics
from pathlib import Path
src='/mnt/data/Coffee_Shop_Strategy_Review (1)(1).xlsx'
out=Path('/mnt/data/BrewLab_Coffee_Simulation_Dashboard')
if out.exists(): shutil.rmtree(out)
out.mkdir()
wb=openpyxl.load_workbook(src,data_only=True)
# Run summary
ws=wb['Run Summary']; runs=[]
for r in ws.iter_rows(min_row=5,max_row=19,values_only=True):
    if r[0]: runs.append(dict(level=r[0],run=r[1],label=r[2],strategy=r[3],game_total=r[4],workbook_total=r[5],target=r[6],pct_target=r[7],difference=r[8]))
# L1/L2 annual
ws=wb['Data L1-L2']; annual=[]
headers=[c.value for c in ws[4]]
for row in ws.iter_rows(min_row=5,values_only=True):
    if row[0] is not None:
        annual.append(dict(zip(headers,row)))
# L3 market
ws=wb['Data L3']; l3=[]
headers3=[c.value for c in ws[4]][:9]
for row in ws.iter_rows(min_row=5,values_only=True):
    if isinstance(row[0],int) and row[1] in ('Mature','Emerging'):
        l3.append(dict(zip(headers3,row[:9])))
# experiments/rules
ws=wb['Experiments & Playbook']; experiments=[]; rules=[]
for row in ws.iter_rows(min_row=5,max_row=18,values_only=True):
    if row[0] and str(row[0]).startswith('E'):
        experiments.append(dict(id=row[0],pillar=row[1],question=row[2],change=row[3],runs=row[4],profit_effect=row[5],conclusion=row[6],quality=row[7]))
for row in ws.iter_rows(min_row=22,max_row=28,values_only=True):
    if isinstance(row[0],int): rules.append(dict(n=row[0],pillar=row[1],situation=row[2],rule=row[3],evidence=row[4],caveat=row[6]))
# metrics
beat=sum(r['game_total']>=r['target'] for r in runs)
best=max(runs,key=lambda r:r['game_total'])
avg=sum(r['game_total'] for r in runs)/len(runs)
level_avg={lvl:sum(r['game_total'] for r in runs if r['level']==lvl)/sum(1 for r in runs if r['level']==lvl) for lvl in ['L1','L2','L3']}
data={'runs':runs,'annual':annual,'l3':l3,'experiments':experiments,'rules':rules,'metrics':{'beat':beat,'count':len(runs),'best':best,'average':avg,'level_avg':level_avg},'source':{'file':os.path.basename(src),'sheets':wb.sheetnames,'notes':['Game total ($) is the simulation-reported cumulative profit from Run Summary.','% of target = Game total / Target.','Target achievement count = runs where Game total >= Target.','Average game total = arithmetic mean of the 15 Game total values.','L1/L2 yearly operating profit is read from Data L1-L2.','L3 market charts use Data L3 market-year operating profit; run totals use Run Summary because Level 3 also includes all-markets/franchise results.']}}
(out/'data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
# self-contained-ish app uses local data.js to work via file:// too
(out/'data.js').write_text('window.COFFEE_DATA='+json.dumps(data,ensure_ascii=False)+';',encoding='utf-8')
html=r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Interactive Coffee Shop Inc. strategy simulation dashboard"><title>BREW/LAB · Coffee Strategy Dashboard</title><link rel="stylesheet" href="styles.css"></head><body>
<a class="skip" href="#main">Skip to dashboard</a><div class="steam-bg" aria-hidden="true"></div>
<header><div class="brand"><div class="logo">☕</div><div><b>BREW/LAB</b><span>strategy intelligence</span></div></div><button id="theme" aria-label="Toggle theme">◐</button></header>
<main id="main"><section class="hero"><div><p class="eyebrow">BUSINESS ESSENTIALS SIMULATION</p><h1>Coffee Shop Strategy<br><em>Dashboard</em></h1><p class="lede">A data-driven view of 15 simulation runs across Starting Up, Building the Brand, and Going International.</p><div class="filters" role="group" aria-label="Filter level"><button class="active" data-level="ALL">All levels</button><button data-level="L1">Level 1</button><button data-level="L2">Level 2</button><button data-level="L3">Level 3</button></div></div>
<div class="brew-scene" aria-label="Animated coffee brewing illustration"><div class="steam s1"></div><div class="steam s2"></div><div class="steam s3"></div><div class="drip"></div><div class="cup"><div class="coffee"></div><div class="shine"></div></div><div class="handle"></div><div class="saucer"></div><div class="bean b1">●</div><div class="bean b2">●</div></div></section>
<section class="kpis" id="kpis"></section>
<section class="grid"><article class="card wide"><div class="card-head"><div><span class="tag">PERFORMANCE</span><h2>Simulation run performance</h2></div><span id="runHint" class="muted">Click a bar for details</span></div><div id="barChart" class="chart" role="img" aria-label="Simulation run profit chart"></div></article>
<article class="card"><span class="tag">TARGETS</span><h2>Achievement</h2><div id="donut" class="donut"></div><p id="donutText" class="center"></p></article>
<article class="card"><span class="tag">LEVELS</span><h2>Average game total</h2><div id="levelBars"></div></article>
<article class="card wide"><div class="card-head"><div><span class="tag">TRAJECTORY</span><h2>Annual operating profit</h2></div><select id="runSelect" aria-label="Select simulation run"></select></div><div id="lineChart" class="chart line"></div><p class="note" id="trajectoryNote"></p></article>
<article class="card"><span class="tag">RUN DETAIL</span><h2 id="detailTitle">Select a run</h2><div id="detail"></div></article></section>
<section class="section"><div class="section-title"><div><span class="tag">EVIDENCE</span><h2>Strategic experiments</h2></div><select id="experimentFilter"><option value="ALL">All pillars</option><option value="1 · Where">Where</option><option value="2 · How">How</option><option value="3 · Grow">Grow</option></select></div><div id="experiments" class="experiment-grid"></div></section>
<section class="section"><div class="section-title"><div><span class="tag">PLAYBOOK</span><h2>Decision rules supported by the workbook</h2></div></div><div id="rules" class="rules"></div></section>
<section class="method"><h2>Metric definitions & data provenance</h2><div id="method"></div><p><strong>Source workbook:</strong> <span id="sourceFile"></span>. Dashboard values are generated from workbook data; no simulation values are invented.</p></section></main>
<footer>BREW/LAB · Static GitHub Pages dashboard · <span id="stamp"></span></footer><script src="data.js"></script><script src="app.js"></script></body></html>'''
(out/'index.html').write_text(html,encoding='utf-8')
css=r''':root{--bg:#140c08;--panel:#21140e;--panel2:#2b1a11;--text:#fff8ed;--muted:#c8b6a6;--cream:#f7e7ce;--gold:#d99a4e;--amber:#f3b45c;--green:#7bd89b;--red:#ff8a7d;--line:#4a3021;--shadow:0 24px 60px #0008}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 80% 0,#3b2114 0,transparent 30%),linear-gradient(180deg,#100906,#1a0f0a 55%,#0f0906);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;min-height:100vh}.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:#fff;color:#000;padding:.7rem;z-index:99}header{height:72px;display:flex;align-items:center;justify-content:space-between;padding:0 max(20px,4vw);border-bottom:1px solid #ffffff12;position:sticky;top:0;background:#140c08dd;backdrop-filter:blur(18px);z-index:20}.brand{display:flex;gap:12px;align-items:center}.brand b{font-family:Georgia,serif;font-size:22px;letter-spacing:.06em}.brand span{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.15em}.logo{font-size:28px}button,select{font:inherit}#theme{border:1px solid var(--line);background:var(--panel);color:var(--cream);width:42px;height:42px;border-radius:50%;cursor:pointer}main{max-width:1440px;margin:auto;padding:36px max(18px,4vw) 70px}.hero{min-height:390px;display:grid;grid-template-columns:1.35fr .65fr;align-items:center;gap:40px}.eyebrow,.tag{font-size:11px;letter-spacing:.18em;font-weight:800;color:var(--gold)}h1{font-family:Georgia,serif;font-size:clamp(46px,6vw,88px);line-height:.92;margin:.15em 0 .25em;font-weight:500}h1 em{color:var(--amber);font-style:italic}h2{font-family:Georgia,serif;font-weight:500;margin:.3rem 0 1rem}.lede{color:var(--muted);max-width:720px;font-size:17px;line-height:1.7}.filters{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}.filters button{border:1px solid var(--line);background:#ffffff08;color:var(--cream);padding:10px 16px;border-radius:999px;cursor:pointer}.filters button.active,.filters button:hover{background:var(--cream);color:#2b180d}.brew-scene{height:330px;position:relative;filter:drop-shadow(0 25px 35px #0009)}.cup{position:absolute;left:50%;top:130px;transform:translateX(-50%);width:190px;height:125px;border-radius:10px 10px 80px 80px;background:linear-gradient(100deg,#f2d7b3,#fff5e3 48%,#cda77c);overflow:hidden;z-index:3}.coffee{height:22px;width:174px;border-radius:50%;background:radial-gradient(ellipse,#8a4c25,#2d1309 70%);position:absolute;top:-8px;left:8px;animation:ripple 1.8s ease-in-out infinite}.shine{position:absolute;left:24px;top:25px;width:18px;height:65px;border-radius:50%;background:#fff5;transform:rotate(15deg)}.handle{position:absolute;left:calc(50% + 72px);top:155px;width:75px;height:70px;border:16px solid #e4c49e;border-left:0;border-radius:0 50% 50% 0}.saucer{position:absolute;left:50%;top:245px;transform:translateX(-50%);width:260px;height:32px;border-radius:50%;background:linear-gradient(#f4dec0,#aa805a)}.drip{position:absolute;left:50%;top:45px;width:6px;height:95px;background:linear-gradient(#4b2410,#b86b32);border-radius:4px;animation:pour 1.3s ease-in-out infinite}.steam{position:absolute;top:55px;width:24px;height:90px;border-left:4px solid #f9eadb66;border-radius:50%;filter:blur(1px);animation:steam 3s ease-in-out infinite}.s1{left:44%}.s2{left:50%;animation-delay:.7s}.s3{left:56%;animation-delay:1.4s}.bean{position:absolute;color:#7b3f1f;font-size:35px;transform:scaleX(.65) rotate(25deg)}.b1{bottom:20px;left:20%;animation:float 4s ease-in-out infinite}.b2{bottom:10px;right:18%;animation:float 4.7s ease-in-out infinite reverse}@keyframes steam{0%{opacity:0;transform:translateY(25px) scale(.7)}50%{opacity:.8}100%{opacity:0;transform:translateY(-55px) translateX(18px) scale(1.3)}}@keyframes pour{0%,100%{height:78px;opacity:.75}50%{height:100px;opacity:1}}@keyframes ripple{50%{transform:scaleX(.96);filter:brightness(1.25)}}@keyframes float{50%{transform:scaleX(.65) rotate(10deg) translateY(-14px)}}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:10px 0 18px}.kpi,.card,.method{background:linear-gradient(145deg,#ffffff0a,#ffffff03);border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow)}.kpi{padding:20px;position:relative;overflow:hidden}.kpi:after{content:"";position:absolute;inset:auto -20% -60% 30%;height:120px;background:radial-gradient(circle,var(--glow,#d99a4e33),transparent 65%)}.kpi .value{font-family:Georgia,serif;font-size:clamp(26px,3vw,42px);margin:6px 0}.kpi .label{color:var(--muted);font-size:12px}.grid{display:grid;grid-template-columns:1.35fr .65fr;gap:18px}.card{padding:22px;min-width:0}.wide{min-height:390px}.card-head,.section-title{display:flex;justify-content:space-between;gap:18px;align-items:flex-start}.muted,.note{color:var(--muted);font-size:12px}.chart{height:300px;display:flex;align-items:flex-end;gap:8px;padding:20px 8px 32px;border-bottom:1px solid var(--line);position:relative}.bar{flex:1;min-width:12px;border-radius:8px 8px 2px 2px;background:linear-gradient(180deg,var(--amber),#8a4b20);cursor:pointer;position:relative;transition:.25s}.bar:hover,.bar.selected{filter:brightness(1.25);transform:translateY(-4px)}.bar span{position:absolute;bottom:-25px;left:50%;transform:translateX(-50%);font-size:10px;color:var(--muted)}.bar .tip{display:none;position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);white-space:nowrap;background:#090504;padding:6px 8px;border-radius:8px;font-size:10px}.bar:hover .tip{display:block}.donut{width:170px;height:170px;border-radius:50%;margin:25px auto 15px;display:grid;place-items:center;position:relative}.donut:after{content:"";width:115px;height:115px;border-radius:50%;background:var(--panel);position:absolute}.center{text-align:center}.level-row{display:grid;grid-template-columns:40px 1fr 80px;gap:10px;align-items:center;margin:18px 0}.track{height:13px;background:#ffffff0b;border-radius:99px;overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,#8d4f27,var(--amber));border-radius:99px}.line svg{width:100%;height:100%;overflow:visible}.line{display:block;padding:10px;border:0}.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.detail-item{padding:12px;border-radius:12px;background:#ffffff07}.detail-item b{display:block;font-family:Georgia,serif;font-size:20px}.section{margin-top:48px}.section-title{margin-bottom:16px}.section-title h2{font-size:32px}.section select,.card select{background:var(--panel2);color:var(--cream);border:1px solid var(--line);border-radius:12px;padding:10px}.experiment-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.experiment{padding:18px;border:1px solid var(--line);border-radius:18px;background:#ffffff05}.experiment .effect{font-family:Georgia,serif;font-size:28px;color:var(--green)}.experiment.negative .effect{color:var(--red)}.experiment p{color:var(--muted);line-height:1.5}.quality{font-size:10px;padding:5px 8px;border-radius:99px;background:#ffffff0b}.rules{display:grid;grid-template-columns:repeat(7,1fr);gap:10px}.rule{padding:16px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(160deg,#2e1c12,#1a100b)}.rule .num{font-family:Georgia,serif;color:var(--gold);font-size:28px}.rule p{font-size:12px;color:var(--muted)}.method{margin-top:48px;padding:24px;line-height:1.6}.method ul{columns:2;color:var(--muted)}footer{text-align:center;color:var(--muted);padding:28px;font-size:12px}.light{--bg:#f5eadb;--panel:#fffaf3;--panel2:#f3e2ce;--text:#2a180f;--muted:#715a4a;--cream:#2a180f;--line:#d8bea1;--shadow:0 18px 40px #6a3b1718;background:#f7efe4}.light header{background:#f7efe4dd}.light .donut:after{background:#fffaf3}.light .tip{color:#fff}@media(max-width:1000px){.hero{grid-template-columns:1fr}.brew-scene{height:270px}.kpis{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:1fr}.rules{grid-template-columns:repeat(2,1fr)}}@media(max-width:640px){header{height:62px}main{padding-top:18px}.hero{min-height:auto}.brew-scene{transform:scale(.8);margin:-20px -30px}.kpis{grid-template-columns:1fr 1fr}.kpi{padding:15px}.experiment-grid{grid-template-columns:1fr}.rules{grid-template-columns:1fr}.method ul{columns:1}.chart{gap:4px}.bar span{font-size:8px}.card-head,.section-title{flex-direction:column}.wide{min-height:350px}}@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}'''
(out/'styles.css').write_text(css,encoding='utf-8')
js=r'''const D=window.COFFEE_DATA;let level='ALL',selected=null;const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];const money=n=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(n);const compact=n=>n>=1e6?'$'+(n/1e6).toFixed(2)+'M':'$'+(n/1e3).toFixed(0)+'K';
function filtered(){return D.runs.filter(r=>level==='ALL'||r.level===level)}
function renderKPIs(){const r=filtered(),beat=r.filter(x=>x.game_total>=x.target).length,best=r.reduce((a,b)=>a.game_total>b.game_total?a:b),avg=r.reduce((s,x)=>s+x.game_total,0)/r.length,avgPct=r.reduce((s,x)=>s+x.pct_target,0)/r.length;$('#kpis').innerHTML=[['Target achievement',`${beat}/${r.length}`,`${(100*beat/r.length).toFixed(1)}% of filtered runs`],['Highest game total',compact(best.game_total),best.label],['Average game total',compact(avg),'Calculated: mean of filtered runs'],['Average target multiple',avgPct.toFixed(2)+'×','Calculated: mean(Game total ÷ target)']].map((x,i)=>`<article class="kpi" style="--glow:${['#7bd89b44','#f3b45c44','#c28cff44','#69b7ff44'][i]}"><div class="label">${x[0]}</div><div class="value">${x[1]}</div><div class="label">${x[2]}</div></article>`).join('')}
function renderBars(){const r=filtered(),max=Math.max(...r.map(x=>x.game_total));$('#barChart').innerHTML=r.map(x=>`<div class="bar ${selected&&selected.level===x.level&&selected.run===x.run?'selected':''}" data-l="${x.level}" data-r="${x.run}" style="height:${Math.max(6,x.game_total/max*100)}%"><div class="tip">${x.label}: ${money(x.game_total)}</div><span>${x.level.replace('L','')}·${x.run}</span></div>`).join('');$$('.bar').forEach(b=>b.onclick=()=>{selected=D.runs.find(x=>x.level===b.dataset.l&&x.run==b.dataset.r);renderBars();renderDetail();setRunSelect()})}
function renderDonut(){const r=filtered(),beat=r.filter(x=>x.game_total>=x.target).length,p=beat/r.length*100;$('#donut').style.background=`conic-gradient(var(--green) 0 ${p}%, var(--red) ${p}% 100%)`;$('#donutText').innerHTML=`<b>${p.toFixed(1)}%</b> achieved target<br><span class="muted">${beat} of ${r.length} runs</span>`}
function renderLevels(){const av=D.metrics.level_avg,max=Math.max(...Object.values(av));$('#levelBars').innerHTML=['L1','L2','L3'].map(l=>`<div class="level-row"><b>${l}</b><div class="track"><div class="fill" style="width:${av[l]/max*100}%"></div></div><span>${compact(av[l])}</span></div>`).join('')}
function setRunSelect(){const r=filtered();$('#runSelect').innerHTML=r.map(x=>`<option value="${x.level}|${x.run}" ${selected&&selected.level===x.level&&selected.run===x.run?'selected':''}>${x.label}</option>`).join('');if(!selected||!r.some(x=>x.level===selected.level&&x.run===selected.run))selected=r[0];$('#runSelect').value=`${selected.level}|${selected.run}`;renderLine();renderDetail()}
function renderLine(){if(!selected)return;let pts=[],note='';if(selected.level!=='L3'){pts=D.annual.filter(x=>x.Level==Number(selected.level.slice(1))&&x.Run==selected.run).map(x=>({year:x.Year,val:x['Operating profit ($)']}));note='Annual operating profit from Data L1-L2.'}else{const rows=D.l3.filter(x=>x.Run==selected.run);for(let y=1;y<=5;y++){const ys=rows.filter(x=>x.Year===y);pts.push({year:y,val:ys.reduce((s,x)=>s+x['Operating profit ($)'],0)})}note='Calculated: Mature + Emerging market operating profit from Data L3. This is not the L3 run total; franchise/all-markets results are excluded.'}const max=Math.max(...pts.map(p=>p.val),1),min=Math.min(0,...pts.map(p=>p.val));const W=700,H=240,pad=35;const x=i=>pad+i*(W-2*pad)/(pts.length-1),y=v=>H-pad-(v-min)/(max-min||1)*(H-2*pad);let poly=pts.map((p,i)=>`${x(i)},${y(p.val)}`).join(' ');$('#lineChart').innerHTML=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Annual operating profit trajectory"><line x1="${pad}" y1="${y(0)}" x2="${W-pad}" y2="${y(0)}" stroke="var(--line)"/><polyline points="${poly}" fill="none" stroke="var(--amber)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>${pts.map((p,i)=>`<circle cx="${x(i)}" cy="${y(p.val)}" r="6" fill="var(--cream)" stroke="var(--gold)" stroke-width="3"/><text x="${x(i)}" y="${H-8}" text-anchor="middle" fill="var(--muted)" font-size="11">Y${p.year}</text><title>Year ${p.year}: ${money(p.val)}</title>`).join('')}</svg>`;$('#trajectoryNote').textContent=note}
function renderDetail(){if(!selected)return;$('#detailTitle').textContent=selected.label;$('#detail').innerHTML=`<p class="muted">${selected.strategy}</p><div class="detail-grid"><div class="detail-item"><span class="muted">Game total</span><b>${money(selected.game_total)}</b></div><div class="detail-item"><span class="muted">Target</span><b>${money(selected.target)}</b></div><div class="detail-item"><span class="muted">% of target</span><b>${(selected.pct_target*100).toFixed(1)}%</b></div><div class="detail-item"><span class="muted">Workbook − game</span><b>${money(selected.difference)}</b></div></div>`}
function renderExperiments(){const f=$('#experimentFilter').value;$('#experiments').innerHTML=D.experiments.filter(e=>f==='ALL'||e.pillar===f).map(e=>`<article class="experiment ${e.profit_effect<0?'negative':''}"><div class="card-head"><span class="tag">${e.id} · ${e.pillar}</span><span class="quality">${e.quality}</span></div><h3>${e.question}</h3><div class="effect">${e.profit_effect>=0?'+':''}${money(e.profit_effect)}</div><p>${e.conclusion}</p><small class="muted">${e.change} · ${e.runs}</small></article>`).join('')}
function renderRules(){$('#rules').innerHTML=D.rules.map(r=>`<article class="rule"><div class="num">0${r.n}</div><span class="tag">${r.pillar}</span><h3>${r.rule}</h3><p><b>${r.situation}</b><br>${r.evidence}</p><p>${r.caveat||''}</p></article>`).join('')}
function renderMethod(){$('#method').innerHTML='<ul>'+D.source.notes.map(n=>`<li>${n}</li>`).join('')+'</ul>';$('#sourceFile').textContent=D.source.file;$('#stamp').textContent='Generated from workbook snapshot'}
$$('.filters button').forEach(b=>b.onclick=()=>{$$('.filters button').forEach(x=>x.classList.remove('active'));b.classList.add('active');level=b.dataset.level;selected=null;renderAll()});$('#experimentFilter').onchange=renderExperiments;$('#runSelect').onchange=e=>{const [l,r]=e.target.value.split('|');selected=D.runs.find(x=>x.level===l&&x.run==r);renderBars();renderLine();renderDetail()};$('#theme').onclick=()=>document.body.classList.toggle('light');function renderAll(){renderKPIs();renderBars();renderDonut();renderLevels();setRunSelect()}renderExperiments();renderRules();renderMethod();renderAll();'''
(out/'app.js').write_text(js,encoding='utf-8')
readme=f'''# BREW/LAB — Coffee Shop Strategy Dashboard

A static, interactive GitHub Pages dashboard generated from **{os.path.basename(src)}**.

## What is in the workbook

The source workbook contains {len(wb.sheetnames)} sheets. The dashboard uses:
- `Run Summary`: 15 simulation runs, five runs each for L1/L2/L3.
- `Data L1-L2`: {len(annual)} run-year records with location, roasting, coffee, pricing, stars, demand, revenue, costs and operating profit.
- `Data L3`: {len(l3)} market-year records split between Mature and Emerging markets.
- `Experiments & Playbook`: {len(experiments)} strategic comparisons and {len(rules)} evidence-supported decision rules.

## Calculated metrics

- **Target achievement** = count of filtered runs where `Game total ($) >= Target ($)`.
- **Average game total** = arithmetic mean of `Game total ($)` for filtered runs.
- **Average target multiple** = mean of `Game total ($) / Target ($)`.
- **Level average** = arithmetic mean of the five `Game total ($)` values within each level.
- **L3 annual market operating profit** = Mature operating profit + Emerging operating profit for the selected year. This deliberately excludes franchise/all-markets results and is labelled as such in the dashboard.

## Run locally

The site has no build step and no external JavaScript dependencies. Open `index.html` directly in a modern browser. For a local web server, run:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Deploy to GitHub Pages

1. Create a GitHub repository, for example `coffee-strategy-dashboard`.
2. Upload **all files in this folder** to the repository root.
3. Commit to the `main` branch.
4. Open **Settings → Pages**.
5. Under **Build and deployment**, choose **Deploy from a branch**.
6. Select **main** and **/(root)**, then save.
7. GitHub will show the published Pages URL after deployment.

## Updating the Excel data

The browser does not read `.xlsx` files directly. `data.js` and `data.json` are generated snapshots of the workbook.

When the workbook changes, regenerate those files from the updated workbook, keeping the same field names used by `app.js`. The safest workflow is to rerun the workbook-to-dashboard generator used to create this package. If columns/sheets are renamed, update the extraction mapping before publishing.

## Reliability and privacy

- No analytics, trackers, account credentials, or external APIs are included.
- No workbook formulas are executed in the browser.
- Missing chart data is handled by the dashboard's selection logic; unsupported fields are not fabricated.
- The site respects `prefers-reduced-motion` for accessibility.
- `data.json` is included for transparency and auditing; `data.js` is the browser-ready equivalent.
'''
(out/'README.md').write_text(readme,encoding='utf-8')
(out/'.nojekyll').write_text('',encoding='utf-8')
# generator source for updates
shutil.copy('/tmp/build_dashboard.py',out/'build_dashboard.py')
zip_path='/mnt/data/BrewLab_Coffee_Simulation_Dashboard.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in out.rglob('*'):
        if f.is_file(): z.write(f,f.relative_to(out))
print('OUT',out,'ZIP',zip_path)
print('FILES',[p.name for p in out.iterdir()])
print('metrics',data['metrics'])
