import streamlit.components.v1 as components

def render_firefighter():
    html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>สุขภาพอาสาสมัครดับไฟป่า อำเภอสันทราย</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- โหลดไลบรารีสำหรับแคปเจอร์หน้าเว็บเป็นรูปภาพ -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

<style>
  :root{
    --bg:#f4f6f8;
    --bg-panel:#ffffff;
    --bg-panel-2:#f1f3f6;
    --line: rgba(15,23,42,0.08);
    --line-strong: rgba(15,23,42,0.14);
    --ink:#16202a;
    --ink-dim:#647082;
    --ember:#e0642c;
    --ember-dim:#f6c4a6;
    --ember-glow: rgba(224,100,44,0.20);
    --sage:#1f9d70;
    --sage-dim:#a9e0c6;
    --sage-glow: rgba(31,157,112,0.16);
    --gold:#c98a1a;
    --danger:#d64545;
    --blue:#3f7fd6;
    --radius: 10px;
    --shadow: 0 1px 2px rgba(15,23,42,0.04), 0 6px 20px rgba(15,23,42,0.05);
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    background:
      radial-gradient(ellipse 900px 460px at 12% -12%, rgba(224,100,44,0.06), transparent 60%),
      radial-gradient(ellipse 900px 560px at 100% 6%, rgba(31,157,112,0.06), transparent 60%),
      var(--bg);
    color:var(--ink);
    font-family:'Sarabun','Google Sans','Noto Sans Thai',sans-serif;
    min-height:100vh;
    padding: 28px 20px 60px;
  }
  .wrap{max-width:1180px;margin:0 auto;}

  /* คลาสพิเศษสำหรับตอนแคปเจอร์เป็นรูปภาพ: บังคับพื้นหลังทึบ ปิดเงา เพื่อให้ภาพออกมาคมชัด */
  .exporting {
    background: #f4f6f8 !important;
    padding: 20px !important;
  }
  .exporting .kpi, .exporting .chart-card, .exporting section.card-block {
    box-shadow: none !important;
    border: 1px solid var(--line-strong) !important;
  }

  header{
    display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between;
    gap:16px; padding-bottom:22px; margin-bottom:8px;
    border-bottom:1px solid var(--line);
  }
  .eyebrow{
    font-family:'JetBrains Mono',monospace; font-size:11.5px; letter-spacing:.14em;
    color:var(--gold); text-transform:uppercase; margin-bottom:8px; display:flex; gap:8px; align-items:center;
  }
  .eyebrow .dot{width:6px;height:6px;border-radius:50%;background:var(--ember);box-shadow:0 0 8px var(--ember-glow);}
  h1{
    font-family:'Sarabun',sans-serif; font-weight:800; font-size:clamp(24px,3.4vw,34px);
    margin:0; line-height:1.25; color:var(--ink); letter-spacing:.01em;
  }
  .sub{color:var(--ink-dim); font-size:14.5px; margin-top:6px;}
  .headline-stat{ text-align:right; }
  .headline-stat .n{font-family:'JetBrains Mono',monospace; font-size:38px; font-weight:700; color:var(--ink); line-height:1;}
  .headline-stat .l{font-size:12px; color:var(--ink-dim); margin-top:4px;}

  .btn-print {
    background-color: var(--blue);
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-family: 'Sarabun', sans-serif;
    font-weight: 700;
    font-size: 13.5px;
    cursor: pointer;
    box-shadow: var(--shadow);
    margin-bottom: 12px;
    transition: opacity 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }
  .btn-print:hover { opacity: 0.9; }

  .firebreak{
    position:relative; margin: 26px 0 30px; height:2px;
    background: repeating-linear-gradient(90deg, var(--line-strong) 0 10px, transparent 10px 16px);
  }
  .tabs{ display:flex; gap:4px; margin-bottom:6px; position:relative; z-index:2; }
  .tab-btn{
    appearance:none; border:none; cursor:pointer; background:transparent;
    font-family:'Sarabun',sans-serif; font-weight:600; font-size:15px;
    color:var(--ink-dim); padding:12px 20px 14px; border-radius:8px 8px 0 0;
    display:flex; align-items:center; gap:9px; transition:color .2s ease, background .2s ease;
    border-bottom:2px solid transparent;
  }
  .tab-btn .flame{font-size:15px; opacity:.7;}
  .tab-btn.active{ color:var(--ink); background:var(--bg-panel); }
  .tab-btn[data-tab="before"].active{ border-bottom:2px solid var(--ember); }
  .tab-btn[data-tab="before"].active .flame{ color:var(--ember); opacity:1;}
  .tab-btn[data-tab="after"].active{ border-bottom:2px solid var(--sage); }
  .tab-btn[data-tab="after"].active .flame{ color:var(--sage); opacity:1;}
  .tab-btn:not(.active):hover{ color:var(--ink); }

  .panel{ display:none; animation: fade .35s ease; }
  .panel.active{ display:block; }
  @keyframes fade{ from{opacity:0; transform:translateY(4px);} to{opacity:1; transform:translateY(0);} }

  section.card-block{
    background:var(--bg-panel); border:1px solid var(--line); border-radius:var(--radius);
    padding:22px 22px 8px; margin-bottom:18px; box-shadow:var(--shadow);
  }

  .kpi-row{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px; margin-bottom:18px;}
  .kpi{
    background:var(--bg-panel); border:1px solid var(--line); border-radius:var(--radius);
    padding:16px 18px; position:relative; overflow:hidden; box-shadow:var(--shadow);
  }
  .kpi::before{ content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--accent, var(--ember)); }
  .kpi .n{ font-family:'JetBrains Mono',monospace; font-size:28px; font-weight:700; color:var(--ink); }
  .kpi .pct{ font-size:13px; color:var(--accent,var(--ember)); font-weight:600; margin-left:6px;}
  .kpi .l{ font-size:12.5px; color:var(--ink-dim); margin-top:5px; line-height:1.4;}

  .grid2{ display:grid; grid-template-columns:1.3fr 1fr; gap:18px; margin-bottom:18px;}
  .grid3{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-bottom:18px;}
  @media(max-width:820px){ .grid2,.grid3{grid-template-columns:1fr;} }

  .chart-card{
    background:var(--bg-panel); border:1px solid var(--line); border-radius:var(--radius);
    padding:18px 20px 16px; box-shadow:var(--shadow);
  }
  .chart-card h3{ font-family:'Sarabun',sans-serif; font-size:16px; font-weight:700; margin:0 0 2px; color:var(--ink); }
  .chart-card .note{ font-size:11.5px; color:var(--ink-dim); margin-bottom:14px;}

  .donut-wrap{ display:flex; align-items:center; gap:16px; flex-wrap:wrap; justify-content:center;}
  .donut-wrap svg{ flex:none; }
  .leg{ display:flex; flex-direction:column; gap:7px; flex:1; min-width:150px;}
  .leg-row{ display:flex; align-items:center; gap:8px; font-size:12px; color:var(--ink-dim);}
  .leg-sw{ width:9px; height:9px; border-radius:2px; flex:none;}
  .leg-row b{ color:var(--ink); font-weight:600; margin-left:auto; font-family:'JetBrains Mono',monospace; font-size:12px;}

  .hbar-chart{ display:flex; flex-direction:column; gap:11px; }
  .hbar-row{ display:grid; grid-template-columns:230px 1fr 74px; align-items:center; gap:10px; }
  .hbar-row .hb-label{ font-size:12.5px; color:var(--ink-dim); text-align:right; white-space:normal; line-height:1.3;}
  .hbar-row .hb-track{ background:rgba(15,23,42,0.06); border-radius:5px; height:16px; overflow:hidden; }
  .hbar-row .hb-fill{ height:100%; border-radius:5px; }
  .hbar-row .hb-val{ font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--ink); }
  .hbar-row .hb-val span{ color:var(--ink-dim); font-size:10.5px; }
  @media(max-width:600px){ .hbar-row{ grid-template-columns:110px 1fr 60px; } .hbar-row .hb-label{font-size:11px;} }

  .simplebar{ display:flex; flex-direction:column; gap:14px; padding:6px 0;}
  .simplebar-row .sb-top{ display:flex; justify-content:space-between; font-size:12.5px; color:var(--ink-dim); margin-bottom:6px;}
  .simplebar-row .sb-top b{ color:var(--ink); font-family:'JetBrains Mono',monospace;}
  .simplebar-row .sb-track{ background:rgba(15,23,42,0.06); border-radius:6px; height:20px; overflow:hidden;}
  .simplebar-row .sb-fill{ height:100%; border-radius:6px; }

  table.data-table{ width:100%; border-collapse:collapse; font-size:13.5px; margin: 4px 0 20px;}
  table.data-table th{
    text-align:left; font-size:11px; letter-spacing:.06em; text-transform:uppercase;
    color:var(--ink-dim); font-weight:600; padding:10px 10px; border-bottom:1px solid var(--line-strong);
  }
  table.data-table td{ padding:9px 10px; border-bottom:1px solid var(--line); color:var(--ink); }
  table.data-table td.num, table.data-table th.num{ text-align:right; font-family:'JetBrains Mono',monospace; }
  table.data-table tr.section-row td{ background:var(--bg-panel-2); font-weight:700; color:var(--ink); }
  table.data-table tr.sub td:first-child{ padding-left:26px; color:var(--ink-dim); }
  table.data-table tr:hover td{ background:rgba(15,23,42,0.025); }

  .section-title{
    font-family:'Sarabun',sans-serif; font-size:15px; font-weight:700; color:var(--ink);
    margin: 0 0 14px; padding-top:4px; display:flex; align-items:center; gap:8px;
  }
  .section-title::before{ content:""; width:3px; height:14px; background:var(--accent,var(--ember)); border-radius:2px;}

  .callout{
    display:flex; gap:14px; align-items:flex-start; background:var(--bg-panel-2);
    border:1px solid var(--line-strong); border-left:3px solid var(--danger);
    border-radius:8px; padding:14px 16px; margin: 6px 0 20px; font-size:13.5px; line-height:1.6;
  }
  .callout .ic{ font-size:18px; }
  .callout b{ color:var(--ink); }
  .callout .tag{
    display:inline-block; font-family:'JetBrains Mono',monospace; font-size:10.5px; background:rgba(214,69,69,0.12);
    color:#b5342f; border-radius:4px; padding:1px 6px; margin-left:6px; letter-spacing:.03em;
  }

  .tambon-strip{ display:flex; flex-wrap:wrap; gap:10px; margin: 4px 0 20px;}
  .tambon-chip{
    background:var(--bg-panel-2); border:1px solid var(--line); border-radius:20px;
    padding:7px 14px; font-size:12.5px; color:var(--ink-dim); display:flex; gap:8px; align-items:center;
  }
  .tambon-chip b{ color:var(--ink); font-family:'JetBrains Mono',monospace; }

  footer{ text-align:center; color:var(--ink-dim); font-size:11.5px; margin-top:30px; }
</style>
</head>
<body>
<div class="wrap" id="dashboard-wrap">

  <header>
    <div>
      <div class="eyebrow"><span class="dot"></span>ระบบเฝ้าระวังสุขภาพอาสาสมัคร</div>
      <h1>สุขภาพอาสาสมัครดับไฟป่า</h1>
      <div class="sub">อำเภอสันทราย จังหวัดเชียงใหม่ · ก่อน–หลังปฏิบัติภารกิจดับไฟป่า</div>
    </div>
    <div class="headline-stat">
      <!-- ปุ่มสั่ง Print PDF -->
      <button id="print-btn" class="btn-print" onclick="captureAsImage()">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        <span id="print-btn-text">บันทึกเป็นรูปภาพ (PNG)</span>
      </button>
      <br>
      <div class="n" id="hero-n">128</div>
      <div class="l" id="hero-l">คนเข้ารับการตรวจคัดกรอง (ก่อนภารกิจ)</div>
    </div>
  </header>

  <div class="tabs" id="tabs-section">
    <button class="tab-btn active" data-tab="before"><span class="flame">◆</span> ก่อนปฏิบัติภารกิจ</button>
    <button class="tab-btn" data-tab="after"><span class="flame">◆</span> หลังปฏิบัติภารกิจ</button>
  </div>
  <div class="firebreak"></div>

  <!-- ================= BEFORE PANEL ================= -->
  <div class="panel active" id="panel-before">

    <div class="kpi-row">
      <div class="kpi" style="--accent:var(--ember)"><div class="n">128</div><div class="l">จำนวนตรวจคัดกรองทั้งหมด</div></div>
      <div class="kpi" style="--accent:var(--gold)"><div class="n">106<span class="pct">82.8%</span></div><div class="l">เพศชาย</div></div>
      <div class="kpi" style="--accent:var(--gold)"><div class="n">22<span class="pct">17.2%</span></div><div class="l">เพศหญิง</div></div>
      <div class="kpi" style="--accent:var(--danger)"><div class="n">8<span class="pct">6.3%</span></div><div class="l">อายุมากกว่า 65 ปี</div></div>
      <div class="kpi" style="--accent:var(--ember)"><div class="n">85<span class="pct">66.4%</span></div><div class="l">มีโรคประจำตัว / ความผิดปกติ</div></div>
    </div>

    <div class="grid2">
      <div class="chart-card">
        <h3>ความเหมาะสมเข้าร่วมเผชิญเหตุ (ด่านหน้า)</h3>
        <div class="note">ผลประเมินสุขภาพก่อนปฏิบัติงานผจญเพลิงแนวหน้า</div>
        <div id="chart-b-fit"></div>
      </div>
      <div class="chart-card">
        <h3>บทบาทการเข้าร่วมภารกิจ</h3>
        <div class="note">จำนวนคน จากผู้เข้ารับการคัดกรองทั้งหมด 128 คน</div>
        <div id="chart-b-role"></div>
      </div>
    </div>

    <div class="chart-card" style="margin-bottom:18px;">
      <h3>โรคประจำตัว / ความผิดปกติที่พบ</h3>
      <div class="note">ร้อยละคำนวณจากผู้มีโรคประจำตัว 85 คน — เรียงจากมากไปน้อย</div>
      <div id="chart-b-disease" class="hbar-chart"></div>
    </div>

    <section class="card-block">
      <div class="section-title" style="--accent:var(--ember)">ตารางผลการคัดกรองฉบับเต็ม</div>
      <table class="data-table">
        <thead><tr><th>ผลการคัดกรอง</th><th class="num">จำนวน (คน)</th><th class="num">ร้อยละ</th></tr></thead>
        <tbody id="tbl-before"></tbody>
      </table>
    </section>

  </div>

  <!-- ================= AFTER PANEL ================= -->
  <div class="panel" id="panel-after">

    <div class="kpi-row">
      <div class="kpi" style="--accent:var(--sage)"><div class="n">92</div><div class="l">จำนวนตรวจคัดกรองทั้งหมด</div></div>
      <div class="kpi" style="--accent:var(--gold)"><div class="n">82<span class="pct">89.1%</span></div><div class="l">เพศชาย</div></div>
      <div class="kpi" style="--accent:var(--gold)"><div class="n">10<span class="pct">10.9%</span></div><div class="l">เพศหญิง</div></div>
      <div class="kpi" style="--accent:var(--danger)"><div class="n">6<span class="pct">6.5%</span></div><div class="l">อายุมากกว่า 65 ปี</div></div>
      <div class="kpi" style="--accent:var(--sage)"><div class="n">39<span class="pct">42.4%</span></div><div class="l">มีโรคประจำตัว</div></div>
    </div>

    <div class="callout">
      <span class="ic">⚑</span>
      <div>
        <b>ผลการตรวจสุขภาพหลังภารกิจ</b> — 91 คน (98.9%) สุขภาพปกติ เหมาะสมกับภารกิจ
        <span class="tag">พบผิดปกติ 1 ราย</span><br>
        อาสาสมัคร 1 ราย (ตำบลแม่แฝก) ตรวจพบ <b>หัวใจเต้นผิดจังหวะ</b> และ <b>การมองเห็นผิดปกติ</b>
        (ตาซ้ายมองไม่ชัดจากอุบัติเหตุเดิม, irregular rhythm, CXR ไม่พบ infiltration ใหม่)
      </div>
    </div>

    <div class="grid3">
      <div class="chart-card">
        <h3>ดัชนีมวลกาย (BMI)</h3>
        <div class="note">n = 92</div>
        <div id="chart-a-bmi"></div>
      </div>
      <div class="chart-card">
        <h3>ระดับความเสี่ยงความดันโลหิต</h3>
        <div class="note">n = 92</div>
        <div id="chart-a-bp"></div>
      </div>
      <div class="chart-card">
        <h3>พฤติกรรมการสูบบุหรี่</h3>
        <div class="note">n = 92</div>
        <div id="chart-a-smoke"></div>
      </div>
    </div>

    <div class="grid2">
      <div class="chart-card">
        <h3>โรคประจำตัวที่พบ</h3>
        <div class="note">ร้อยละคำนวณจากผู้มีโรคประจำตัว 39 คน (บางรายมีมากกว่า 1 โรค)</div>
        <div id="chart-a-disease" class="hbar-chart"></div>
      </div>
      <div class="chart-card">
        <h3>ตรวจสุขภาพก่อนปฏิบัติภารกิจหรือไม่</h3>
        <div class="note">n = 92</div>
        <div id="chart-a-precheck"></div>
      </div>
    </div>

    <section class="card-block">
      <div class="section-title" style="--accent:var(--sage)">จำนวนอาสาสมัครแยกตามตำบล</div>
      <div class="tambon-strip" id="tambon-strip"></div>

      <div class="section-title" style="--accent:var(--sage)">ตารางสรุปผลการคัดกรอง (หลังภารกิจ)</div>
      <table class="data-table">
        <thead><tr><th>ผลการคัดกรอง</th><th class="num">จำนวน (คน)</th><th class="num">ร้อยละ</th></tr></thead>
        <tbody id="tbl-after"></tbody>
      </table>
    </section>

  </div>

  <footer>ข้อมูลจากการตรวจคัดกรองสุขภาพอาสาสมัครดับไฟป่า อำเภอสันทราย จังหวัดเชียงใหม่</footer>
</div>

<script>
const EMBER = '#e0642c', EMBER2='#d64545', GOLD='#c98a1a', SAGE='#1f9d70', SAGE2='#178059', INKDIM='#9aa3b0', BLUE='#3f7fd6';

/* ---------------- TABS ---------------- */
const tabBtns = document.querySelectorAll('.tab-btn');
const heroN = document.getElementById('hero-n');
const heroL = document.getElementById('hero-l');
tabBtns.forEach(btn=>{
  btn.addEventListener('click', ()=>{
    tabBtns.forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
    document.getElementById('panel-'+btn.dataset.tab).classList.add('active');
    if(btn.dataset.tab === 'before'){
      heroN.textContent='128'; heroL.textContent='คนเข้ารับการตรวจคัดกรอง (ก่อนภารกิจ)';
    } else {
      heroN.textContent='92'; heroL.textContent='คนเข้ารับการตรวจคัดกรอง (หลังภารกิจ)';
    }
  });
});

/* ---------------- SVG donut chart builder ---------------- */
function buildDonut(containerId, data, centerLabel){
  const total = data.reduce((s,d)=>s+d.value,0);
  const size = 150, stroke = 22, r = (size-stroke)/2, cx=size/2, cy=size/2;
  const circumference = 2*Math.PI*r;
  let offset = 0;
  let circles = '';
  data.forEach(d=>{
    const frac = d.value/total;
    const len = frac*circumference;
    circles += '<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+d.color+'" stroke-width="'+stroke+'" stroke-dasharray="'+len+' '+(circumference-len)+'" stroke-dashoffset="'+(-offset)+'" transform="rotate(-90 '+cx+' '+cy+')" stroke-linecap="butt"/>';
    offset += len;
  });
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="'+size+'" height="'+size+'" viewBox="0 0 '+size+' '+size+'">' + circles +
    '<text x="'+cx+'" y="'+(cy-4)+'" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="20" font-weight="700" fill="#16202a">'+total+'</text>' +
    '<text x="'+cx+'" y="'+(cy+15)+'" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#647082">'+(centerLabel||'คน')+'</text>' +
    '</svg>';
  const legend = '<div class="leg">' + data.map(function(d){
    return '<div class="leg-row"><span class="leg-sw" style="background:'+d.color+'"></span>'+d.label+'<b>'+d.value+'</b></div>';
  }).join('') + '</div>';
  document.getElementById(containerId).innerHTML = '<div class="donut-wrap">'+svg+legend+'</div>';
}

/* ---------------- horizontal bar chart builder ---------------- */
function buildHBar(containerId, data, color){
  const max = Math.max.apply(null, data.map(function(d){return d.value;}));
  const html = data.map(function(d){
    return '<div class="hbar-row">' +
      '<div class="hb-label">'+d.label+'</div>' +
      '<div class="hb-track"><div class="hb-fill" style="width:'+(d.value/max*100).toFixed(1)+'%; background:'+color+'"></div></div>' +
      '<div class="hb-val">'+d.value+' <span>('+d.pct.toFixed(1)+'%)</span></div>' +
      '</div>';
  }).join('');
  document.getElementById(containerId).innerHTML = html;
}

/* ---------------- simple 2-bar comparison ---------------- */
function buildSimpleBar(containerId, data){
  const max = Math.max.apply(null, data.map(function(d){return d.value;}));
  const html = '<div class="simplebar">' + data.map(function(d){
    return '<div class="simplebar-row">' +
      '<div class="sb-top"><span>'+d.label+'</span><b>'+d.value+' คน</b></div>' +
      '<div class="sb-track"><div class="sb-fill" style="width:'+(d.value/max*100).toFixed(1)+'%; background:'+d.color+'"></div></div>' +
      '</div>';
  }).join('') + '</div>';
  document.getElementById(containerId).innerHTML = html;
}

/* ---------------- BEFORE: data ---------------- */
const beforeRows = [
  {label:'จำนวนตรวจคัดกรอง', n:128, pct:null, section:true},
  {label:'สุขภาพเหมาะสมเข้าร่วมเผชิญเหตุ ผจญเพลิงเพื่อดับไฟป่า (ด่านหน้า)', n:68, pct:53.1},
  {label:'สุขภาพไม่เหมาะสมเข้าร่วมเผชิญเหตุ ผจญเพลิงเพื่อดับไฟป่า (ด่านหน้า)', n:1, pct:0.8},
  {label:'เข้าร่วมปฏิบัติภารกิจทำแนวกันไฟ', n:75, pct:58.6},
  {label:'เข้าร่วมปฏิบัติการถอสนับสนุนช่วยเหลือ และร่วมสังเกตการณ์', n:74, pct:57.8},
  {label:'อายุมากกว่า 65 ปี', n:8, pct:6.3},
  {label:'เพศหญิง', n:22, pct:17.2},
  {label:'เพศชาย', n:106, pct:82.8},
  {label:'โรคประจำตัว / ความผิดปกติที่พบ', n:85, pct:66.4, section:true},
  {label:'ความดันโลหิตสูง', n:44, pct:51.8, sub:1},
  {label:'โรคเบาหวาน และใช้ยาฉีดอินซูลิน', n:8, pct:9.4, sub:2},
  {label:'เบาหวาน', n:8, pct:9.4, sub:3},
  {label:'โรคหัวใจเต้นผิดจังหวะ', n:3, pct:3.5, sub:4},
  {label:'ปัญหาเกี่ยวกับหู', n:2, pct:2.4, sub:5},
  {label:'โรคเกี่ยวกับการเคลื่อนไหวผิดปกติหรือกล้ามเนื้อ', n:1, pct:1.2, sub:6},
  {label:'เก๊าท์', n:1, pct:1.2, sub:7},
  {label:'ไขมันในเลือดสูง', n:16, pct:18.8, sub:8},
  {label:'โรคหัวใจโต', n:1, pct:1.2, sub:9},
  {label:'โรคซึมเศร้า โรคจิตเภท', n:1, pct:1.2, sub:10},
];

const tblBefore = document.getElementById('tbl-before');
beforeRows.forEach(function(r){
  const tr=document.createElement('tr');
  if(r.section) tr.className='section-row';
  else if(r.sub) tr.className='sub';
  tr.innerHTML = '<td>'+(r.sub? r.sub+'. ':'')+r.label+'</td><td class="num">'+r.n+'</td><td class="num">'+(r.pct!==null? r.pct.toFixed(1)+'%':'')+'</td>';
  tblBefore.appendChild(tr);
});

buildDonut('chart-b-fit', [
  {label:'เหมาะสม เข้าร่วมด่านหน้า', value:68, color:SAGE},
  {label:'ไม่เหมาะสม เข้าร่วมด่านหน้า', value:1, color:EMBER2},
], 'คน');

buildSimpleBar('chart-b-role', [
  {label:'เข้าร่วมทำแนวกันไฟ', value:75, color:EMBER},
  {label:'สนับสนุน/สังเกตการณ์', value:74, color:GOLD},
]);

const bDiseaseRows = beforeRows.filter(function(r){return r.sub;}).sort(function(a,b){return b.n-a.n;})
  .map(function(r){return {label:r.label, value:r.n, pct:r.pct};});
buildHBar('chart-b-disease', bDiseaseRows, EMBER);

/* ---------------- AFTER: data ---------------- */
const afterRows = [
  {label:'จำนวนตรวจคัดกรอง', n:92, pct:null, section:true},
  {label:'เพศชาย', n:82, pct:89.1},
  {label:'เพศหญิง', n:10, pct:10.9},
  {label:'อายุมากกว่า 65 ปี', n:6, pct:6.5},
  {label:'ได้ตรวจสุขภาพก่อนปฏิบัติภารกิจ', n:84, pct:91.3},
  {label:'ไม่ได้ตรวจสุขภาพก่อนปฏิบัติภารกิจ', n:8, pct:8.7},
  {label:'ผลตรวจ: สุขภาพปกติ เหมาะสมกับภารกิจ', n:91, pct:98.9},
  {label:'ผลตรวจ: พบความผิดปกติ', n:1, pct:1.1},
  {label:'มีโรคประจำตัว', n:39, pct:42.4, section:true},
  {label:'ความดันโลหิตสูง', n:27, pct:69.2, sub:1},
  {label:'ไขมันในเลือดสูง', n:12, pct:30.8, sub:2},
  {label:'เบาหวาน', n:11, pct:28.2, sub:3},
  {label:'เก๊าท์', n:3, pct:7.7, sub:4},
  {label:'ไทรอยด์', n:2, pct:5.1, sub:5},
  {label:'โรคหัวใจ (รวมผ่าตัดหัวใจ)', n:2, pct:5.1, sub:6},
  {label:'ภูมิคุ้มกัน/ภูมิแพ้ตนเอง/โปรตีนรั่ว', n:3, pct:7.7, sub:7},
];
const tblAfter = document.getElementById('tbl-after');
afterRows.forEach(function(r){
  const tr=document.createElement('tr');
  if(r.section) tr.className='section-row';
  else if(r.sub) tr.className='sub';
  tr.innerHTML = '<td>'+(r.sub? r.sub+'. ':'')+r.label+'</td><td class="num">'+r.n+'</td><td class="num">'+(r.pct!==null? r.pct.toFixed(1)+'%':'')+'</td>';
  tblAfter.appendChild(tr);
});

/* tambon chips */
const tambons = [
  ['ตำบลแม่แฝก',27],['ตำบลหนองแหย่ง',24],['ตำบลแม่แฝกใหม่',23],
  ['ตำบลป่าไผ่',7],['อส. (ที่ว่าการอำเภอ)',6],['ตำบลหนองหาร',5]
];
const strip = document.getElementById('tambon-strip');
tambons.forEach(function(t){
  const el=document.createElement('div'); el.className='tambon-chip';
  el.innerHTML = t[0]+' <b>'+t[1]+'</b>';
  strip.appendChild(el);
});

buildDonut('chart-a-bmi', [
  {label:'โรคอ้วนระดับ 1', value:37, color:GOLD},
  {label:'น้ำหนักปกติ/สมส่วน', value:22, color:SAGE},
  {label:'น้ำหนักเกิน / ท้วม', value:21, color:EMBER},
  {label:'โรคอ้วนระดับ 2 (อันตราย)', value:10, color:EMBER2},
  {label:'น้ำหนักต่ำกว่าเกณฑ์', value:2, color:BLUE},
], 'คน');

buildDonut('chart-a-bp', [
  {label:'ความดันสูง', value:45, color:EMBER},
  {label:'ค่อนข้างสูง/กลุ่มเสี่ยง', value:31, color:GOLD},
  {label:'ปกติ', value:11, color:SAGE},
  {label:'สูงวิกฤต', value:5, color:EMBER2},
], 'คน');

buildDonut('chart-a-smoke', [
  {label:'ไม่สูบ', value:62, color:SAGE},
  {label:'สูบ', value:21, color:EMBER},
  {label:'เลิกแล้ว', value:8, color:GOLD},
  {label:'ไม่ระบุ', value:1, color:INKDIM},
], 'คน');

const aDiseaseRows = afterRows.filter(function(r){return r.sub;}).sort(function(a,b){return b.n-a.n;})
  .map(function(r){return {label:r.label, value:r.n, pct:r.pct};});
buildHBar('chart-a-disease', aDiseaseRows, SAGE2);

buildDonut('chart-a-precheck', [
  {label:'ได้ตรวจก่อนภารกิจ', value:84, color:SAGE},
  {label:'ไม่ได้ตรวจก่อนภารกิจ', value:8, color:EMBER2},
], 'คน');

/* =========================================
   ฟังก์ชันบันทึกเป็นรูปภาพ (รวมทุกอย่างในภาพเดียว)
   ---------------------------------------------------------------
   ความคืบหน้า: การแก้ scrollX/scrollY/x/y ทำให้ตอนนี้ "เนื้อหาครบทุกส่วนแล้ว" (ไม่หายอีกต่อไป)
   แต่ยังเจอปัญหาใหม่คือ "สีซีด/จางทั้งภาพ" (ไม่ใช่แค่บางส่วนแบบเดิม) ซึ่งเป็นคนละสาเหตุกับ
   ปัญหาเนื้อหาหาย — ต้นตอคือโหมดเรนเดอร์ปกติของ html2canvas (foreignObjectRendering:false)
   ไม่ได้ใช้เบราว์เซอร์เรนเดอร์สีจริง แต่ "จำลอง" การผสมสี/ความทึบขึ้นมาเองด้วยอัลกอริทึมภายใน
   ซึ่งมักให้สีอ่อน/ซีดกว่าของจริงอย่างเป็นระบบ (ยิ่งเจอ SVG วงกลม + สีที่ซ้อนทับกันหลายชั้นแบบ
   หน้านี้ ยิ่งเห็นชัด) วิธีแก้ที่ตรงจุดที่สุดคือให้เบราว์เซอร์เรนเดอร์ให้จริงๆ ผ่าน
   foreignObjectRendering:true (ใช้ SVG <foreignObject> เรนเดอร์ DOM ตรงๆ สีจึงตรงกับหน้าจอ
   100%) ผสานกับการแก้ scrollX/scrollY/x/y ที่เพิ่งได้ผลไปแล้วในรอบก่อน และเปลี่ยนไฟล์ผลลัพธ์
   จาก JPEG (มีการบีบอัดข้อมูลภาพ) เป็น PNG (ไม่มีการบีบอัดสูญเสียคุณภาพ) เพื่อตัดปัจจัยการ
   บีบอัดภาพออกไปด้วย ให้สีคมชัดตรงกับที่เห็นบนจอที่สุด
   ========================================= */
async function captureAsImage() {
  const btn = document.getElementById('print-btn');

  // ซ่อนปุ่มชั่วคราวขณะถ่ายภาพ เพื่อไม่ให้ปุ่มติดลงไปในรูป
  btn.style.display = 'none';

  const wrapElement = document.getElementById('dashboard-wrap');

  // เพิ่มคลาส .exporting เพื่อบังคับให้พื้นหลังทึบ ลบเงาเพื่อป้องกันการเรนเดอร์เพี้ยน
  wrapElement.classList.add('exporting');

  // เลื่อนกลับไปบนสุดของหน้าก่อนถ่ายภาพเสมอ (ทั้ง window และตัว document เอง)
  window.scrollTo(0, 0);
  document.documentElement.scrollTop = 0;
  document.body.scrollTop = 0;

  // รอให้ฟอนต์โหลดเสร็จสมบูรณ์ และรอให้ CSS/เลย์เอาต์นิ่งก่อนแคปเจอร์
  if (document.fonts && document.fonts.ready) {
    try { await document.fonts.ready; } catch (e) {}
  }
  await new Promise(resolve => setTimeout(resolve, 350));

  const captureOptions = {
      scale: 2,
      useCORS: true,
      backgroundColor: '#f4f6f8',
      logging: false,
      x: 0,
      y: 0,
      scrollX: 0,
      scrollY: 0,
      windowWidth: wrapElement.scrollWidth,
      windowHeight: wrapElement.scrollHeight
  };

  try {
    let canvas;
    try {
      // วิธีหลัก: ให้เบราว์เซอร์เรนเดอร์จริงผ่าน SVG foreignObject สีจะตรงกับหน้าจอ 100%
      canvas = await html2canvas(wrapElement, Object.assign({}, captureOptions, { foreignObjectRendering: true }));
    } catch (foErr) {
      console.warn('foreignObjectRendering ใช้ไม่ได้ในเบราว์เซอร์นี้ กำลังใช้วิธีสำรอง...', foErr);
      canvas = await html2canvas(wrapElement, captureOptions);
    }

    const activeTab = document.getElementById('panel-after').classList.contains('active') ? 'After' : 'Before';
    const link = document.createElement('a');
    link.download = 'Wildfire_Volunteer_Health_Check_' + activeTab + '.png';
    link.href = canvas.toDataURL('image/png');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

  } catch (error) {
    console.error('Error generating image', error);
    alert('เกิดข้อผิดพลาดในการสร้างรูปภาพ กรุณาลองใหม่อีกครั้ง');
  } finally {
    // นำคลาส .exporting ออก และแสดงปุ่มกลับมาเหมือนเดิม
    wrapElement.classList.remove('exporting');
    btn.style.display = 'inline-flex';
  }
}
</script>
</body>
</html>
    """
    
    components.html(html_code, height=1800, scrolling=True)
