from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/ui", tags=["ui"])


@router.get("/reflections", response_class=HTMLResponse)
def reflections_ui() -> HTMLResponse:
    html = """
<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>習慣スタック日記</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif;background:#fafaf9;color:#1a1a18;padding:20px 16px 48px;min-height:100vh}
.app{max-width:660px;margin:0 auto}
.top-nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px}
.nav-title{font-size:15px;font-weight:500}
.nav-right{display:flex;align-items:center;gap:12px}
.nav-date{font-size:12px;color:#888}
.nav-link{font-size:12px;color:#7F77DD;text-decoration:none}
.tab-row{display:flex;gap:2px;margin-bottom:24px;border-bottom:1px solid #e8e8e5}
.tab{font-size:13px;padding:7px 16px 10px;color:#999;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;transition:all .15s}
.tab.active{color:#1a1a18;font-weight:500;border-bottom-color:#7F77DD}
.pane{display:none}.pane.active{display:block}
.sec-label{font-size:10px;font-weight:500;letter-spacing:.08em;color:#aaa;text-transform:uppercase;margin-bottom:12px}
.task-list{display:flex;flex-direction:column;gap:8px;margin-bottom:10px}
.task-card{background:#fff;border:1px solid #e8e8e5;border-radius:12px;overflow:hidden}
.task-card:focus-within{border-color:#ccc}
.task-top{display:flex;align-items:center;gap:8px;padding:10px 12px}
.chk{width:18px;height:18px;border-radius:5px;border:1px solid #ccc;display:flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0;background:#fff;transition:all .15s}
.chk.done{background:#5DCAA5;border-color:#1D9E75}
.chk svg{display:none}.chk.done svg{display:block}
.task-inp{flex:1;border:none;outline:none;font-size:14px;color:#1a1a18;background:transparent;font-family:inherit}
.task-inp::placeholder{color:#bbb}
.task-inp.struck{text-decoration:line-through;color:#bbb}
.del-btn{width:20px;height:20px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#ccc;font-size:13px;border-radius:50%;transition:all .15s;flex-shrink:0}
.del-btn:hover{background:#f5f5f3;color:#888}
.task-body{border-top:1px solid #f0f0ee;padding:10px 12px;display:flex;flex-direction:column;gap:10px}
.stack-row{display:flex;gap:8px;align-items:flex-start}
.stack-ico{font-size:12px;width:18px;flex-shrink:0;margin-top:2px;text-align:center;color:#bbb}
.stack-inner{flex:1;display:flex;flex-direction:column;gap:5px}
.sub-lbl{font-size:11px;color:#bbb;letter-spacing:.04em}
.line-inp{border:none;border-bottom:1px solid #e8e8e5;outline:none;font-size:13px;color:#555;background:transparent;font-family:inherit;padding:2px 0;width:100%}
.line-inp::placeholder{color:#ccc}
.chip-wrap{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:2px}
.chip{font-size:11px;padding:3px 9px;border-radius:10px;border:1px solid #e8e8e5;cursor:pointer;color:#777;background:#fff;transition:all .12s;white-space:nowrap}
.chip.sel{background:#EEEDFE;border-color:#AFA9EC;color:#3C3489}
.add-task{display:flex;align-items:center;gap:6px;cursor:pointer;font-size:13px;color:#bbb;padding:4px 0;border:none;background:transparent;font-family:inherit}
.add-task:hover{color:#888}
.divider{border:none;border-top:1px solid #f0f0ee;margin:20px 0}
.streak-wrap{margin-bottom:20px}
.streak-meta{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.streak-ttl{font-size:10px;font-weight:500;letter-spacing:.08em;color:#aaa;text-transform:uppercase}
.streak-count{font-size:12px;font-weight:500;color:#534AB7}
.streak-bar{display:flex;gap:3px;flex-wrap:wrap}
.s-dot{width:22px;height:22px;border-radius:4px;border:1px solid #e8e8e5;display:flex;align-items:center;justify-content:center;font-size:8px;color:#bbb;flex-shrink:0}
.s-dot.hit{background:#E1F5EE;border-color:#9FE1CB;color:#085041}
.s-dot.today-dot{border:1.5px solid #7F77DD;color:#534AB7;font-weight:500}
.r-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px;margin-bottom:20px}
.r-card{background:#fff;border:1px solid #e8e8e5;border-radius:12px;padding:14px}
.r-tag{display:inline-block;font-size:10px;font-weight:500;padding:2px 8px;border-radius:10px;letter-spacing:.05em;margin-bottom:7px}
.t-habit{background:#EAF3DE;color:#27500A}
.t-woop{background:#FAEEDA;color:#633806}
.t-sc{background:#EEEDFE;color:#3C3489}
.t-free{background:#F1EFE8;color:#444441}
.r-q{font-size:13px;font-weight:500;color:#1a1a18;margin-bottom:3px;line-height:1.45}
.r-hint{font-size:11px;color:#aaa;line-height:1.55;margin-bottom:9px}
textarea{width:100%;border:none;outline:none;font-size:13px;color:#1a1a18;background:transparent;resize:none;font-family:inherit;line-height:1.65}
textarea::placeholder{color:#ccc}
.woop-rows{display:flex;flex-direction:column;gap:7px}
.woop-row{display:flex;gap:7px;align-items:flex-start}
.woop-key{font-size:10px;font-weight:500;color:#BA7517;min-width:14px;margin-top:3px}
.woop-inp{flex:1;border:none;border-bottom:1px solid #e8e8e5;outline:none;font-size:12px;color:#555;background:transparent;font-family:inherit;padding:2px 0}
.woop-inp::placeholder{color:#ccc}
.intention-card{border:1px solid #e8e8e5;border-radius:12px;padding:12px 14px;margin-bottom:20px;background:#fff}
.int-lbl{font-size:10px;font-weight:500;letter-spacing:.07em;color:#aaa;margin-bottom:3px}
.int-sub{font-size:11px;color:#bbb;margin-bottom:7px;line-height:1.5}
.int-inp{border:none;outline:none;font-size:13px;color:#1a1a18;background:transparent;font-family:inherit;width:100%}
.int-inp::placeholder{color:#ccc}
.save-row{display:flex;justify-content:flex-end}
button.save{background:transparent;border:1px solid #ccc;border-radius:8px;padding:8px 22px;font-size:13px;color:#777;cursor:pointer;font-family:inherit;transition:all .15s}
button.save:hover{background:#f5f5f3;color:#1a1a18}
button.save:disabled{opacity:.5;cursor:default}
.feedback{margin-top:12px;padding:10px 14px;border-radius:8px;font-size:13px;display:none;text-align:right}
.feedback.success{background:#f0fdf4;color:#16a34a;border:1px solid #bbf7d0;display:block}
.feedback.error{background:#fef2f2;color:#dc2626;border:1px solid #fecaca;display:block}
.sec-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.group-card{background:#fff;border:1px solid #e8e8e5;border-radius:12px;margin-bottom:12px;overflow:hidden}
.group-header{font-size:13px;font-weight:500;padding:10px 14px;border-bottom:1px solid #f0f0ee;color:#1a1a18}
.group-items{padding:6px 14px 10px}
.habit-item{display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid #f8f8f6}
.habit-item:last-child{border-bottom:none}
.habit-label{font-size:13px;color:#1a1a18;flex:1;line-height:1.4}
.habit-label.struck{text-decoration:line-through;color:#bbb}
.empty-items{font-size:12px;color:#bbb;padding:4px 0}
.group-woop{padding:8px 14px 10px;border-top:1px solid #f0f0ee;background:#faf9f7}
.group-woop-title{font-size:10px;font-weight:500;letter-spacing:.06em;color:#BA7517;text-transform:uppercase;margin-bottom:6px}
.no-groups-msg{text-align:center;color:#bbb;font-size:13px;padding:32px 0}
.no-groups-msg a{color:#7F77DD;text-decoration:none}
</style>
</head>
<body>
<div class="app">
  <div class="top-nav">
    <span class="nav-title">習慣スタック日記</span>
    <div class="nav-right">
      <span class="nav-date" id="navDate"></span>
    </div>
  </div>
  <div class="tab-row">
    <div class="tab active" onclick="sw('today')">今日のスタック</div>
    <div class="tab" onclick="sw('reflect')">振り返り</div>
  </div>

  <!-- 今日のスタック -->
  <div id="pane-today" class="pane active">
    <div class="sec-header">
      <span class="sec-label">今日の習慣チェック</span>
      <a class="nav-link" href="/ui/habits">グループを管理 →</a>
    </div>
    <div id="groupList"></div>
    <div class="divider"></div>
    <div class="intention-card">
      <div class="int-lbl">明日の意図（Implementation Intention）</div>
      <div class="int-sub">「もし〜なら、〜する」の形で書く。曖昧な意志より具体的な計画が実行率を上げる。</div>
      <input class="int-inp" id="implementation_intention" type="text" placeholder="例：朝コーヒーを淹れたら、その場で5分だけ本を開く。">
    </div>
    <div class="save-row"><button class="save" id="save-stack-btn" onclick="saveReflection()">保存する</button></div>
    <div class="feedback" id="feedback-stack"></div>
  </div>

  <!-- 振り返り -->
  <div id="pane-reflect" class="pane">
    <div class="streak-wrap">
      <div class="streak-meta">
        <span class="streak-ttl">記録（直近14日）</span>
        <div style="display:flex;align-items:center;gap:12px">
          <span class="streak-count" id="streakCount"></span>
          <a href="/ui/reflections/list" style="font-size:13px;color:#7F77DD;text-decoration:none;padding:4px 0">過去の記録 →</a>
        </div>
      </div>
      <div class="streak-bar" id="streakDots"></div>
    </div>
    <div class="r-grid">
      <div class="r-card">
        <span class="r-tag t-habit">習慣モニタリング</span>
        <div class="r-q">今日どうだった？</div>
        <div class="r-hint">記録すること自体が目標達成を促進する。崩れた状況も書くとヒントになる。</div>
        <textarea id="free_text" rows="3" placeholder="例：朝の時間が取れた。夜は疲れていてスキップしてしまった。"></textarea>
      </div>
      <div class="r-card">
        <span class="r-tag t-woop">WOOP</span>
        <div class="r-q">目標・障害・if-thenプラン</div>
        <div class="r-hint">理想だけでなく障害も直視すると達成率が上がる。</div>
        <div class="woop-rows">
          <div class="woop-row"><span class="woop-key">W</span><input class="woop-inp" id="woop_wish" type="text" placeholder="Wish — 達成したいこと"></div>
          <div class="woop-row"><span class="woop-key">O</span><input class="woop-inp" id="woop_outcome" type="text" placeholder="Outcome — 達成したらどんな感覚？"></div>
          <div class="woop-row"><span class="woop-key">O</span><input class="woop-inp" id="woop_obstacle" type="text" placeholder="Obstacle — 邪魔しそうな障害は？"></div>
          <div class="woop-row"><span class="woop-key">P</span><input class="woop-inp" id="woop_plan" type="text" placeholder="Plan — もし障害が起きたら？"></div>
        </div>
      </div>
      <div class="r-card">
        <span class="r-tag t-sc">Self-Concordance</span>
        <div class="r-q">「やらなきゃ」、本当にやりたい？</div>
        <div class="r-hint">内発的動機と一致した目標は達成しやすく、満足度も高い。</div>
        <textarea id="want_to_do" rows="3" placeholder="例：義務感より、体が軽くなる感覚に焦点を当ててみる。"></textarea>
      </div>
      <div class="r-card">
        <span class="r-tag t-free">無意識</span>
        <div class="r-q">今、無意識が求めていることは？</div>
        <div class="r-hint">論理より先に、体や感情が欲しがっているものを言語化する。</div>
        <textarea id="unconscious_desire" rows="3" placeholder="例：静かな時間。誰にも連絡しない夜。"></textarea>
      </div>
    </div>
    <div class="save-row"><button class="save" id="save-btn" onclick="saveReflection()">振り返りを保存</button></div>
    <div class="feedback" id="feedback"></div>
  </div>
</div>

<script>
let existingId = null;
let TODAY = '';

function todayJST(){
  return new Date(Date.now()+9*60*60*1000).toISOString().slice(0,10);
}
function nowJST(){
  const jst=new Date(Date.now()+9*60*60*1000);
  return jst.toISOString().replace('Z','+09:00').slice(0,19)+'+09:00';
}
function v(id){ return document.getElementById(id).value.trim()||null; }
function set(id,val){ document.getElementById(id).value=val||''; }
function escHtml(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

function sw(name){
  ['today','reflect'].forEach(n=>{
    document.getElementById('pane-'+n).classList.toggle('active',n===name);
  });
  document.querySelectorAll('.tab').forEach((t,i)=>{
    t.classList.toggle('active',['today','reflect'][i]===name);
  });
}

/* ---- 習慣グループ ---- */
function buildGroupCard(group){
  const card = document.createElement('div');
  card.className = 'group-card';
  const itemsHtml = group.items.length === 0
    ? '<div class="empty-items">アイテムがありません</div>'
    : group.items.map(item => `
      <div class="habit-item">
        <div class="chk${item.done?' done':''}" onclick="toggleItem(this,${item.id})">
          <svg width="10" height="10" viewBox="0 0 10 10"><polyline points="1,5 4,8 9,2" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
        <span class="habit-label${item.done?' struck':''}">${escHtml(item.content)}</span>
      </div>`).join('');
  const hasWoop = group.woop_wish || group.woop_outcome || group.woop_obstacle || group.woop_plan;
  const woopHtml = hasWoop ? `
    <div class="group-woop">
      <div class="group-woop-title">WOOP</div>
      <div class="woop-rows">
        ${group.woop_wish?`<div class="woop-row"><span class="woop-key">W</span><span style="font-size:12px;color:#555">${escHtml(group.woop_wish)}</span></div>`:''}
        ${group.woop_outcome?`<div class="woop-row"><span class="woop-key">O</span><span style="font-size:12px;color:#555">${escHtml(group.woop_outcome)}</span></div>`:''}
        ${group.woop_obstacle?`<div class="woop-row"><span class="woop-key">O</span><span style="font-size:12px;color:#555">${escHtml(group.woop_obstacle)}</span></div>`:''}
        ${group.woop_plan?`<div class="woop-row"><span class="woop-key">P</span><span style="font-size:12px;color:#555">${escHtml(group.woop_plan)}</span></div>`:''}
      </div>
    </div>` : '';
  card.innerHTML = `
    <div class="group-header">${escHtml(group.name)}</div>
    <div class="group-items">${itemsHtml}</div>
    ${woopHtml}`;
  return card;
}

async function toggleItem(chkEl, itemId){
  const done = !chkEl.classList.contains('done');
  chkEl.classList.toggle('done', done);
  const label = chkEl.parentElement.querySelector('.habit-label');
  if(label) label.classList.toggle('struck', done);
  await fetch('/habit-groups/items/'+itemId+'/completion?day='+TODAY, {
    method:'PATCH', headers:{'Content-Type':'application/json'},
    body:JSON.stringify({done})
  });
}

async function loadGroups(){
  const container = document.getElementById('groupList');
  try{
    const r = await fetch('/habit-groups?day='+TODAY);
    const data = await r.json();
    const groups = data.groups || [];
    if(groups.length === 0){
      container.innerHTML = '<div class="no-groups-msg">習慣グループがありません。<br><a href="/ui/habits">グループを追加する →</a></div>';
    } else {
      container.innerHTML = '';
      groups.forEach(g => container.appendChild(buildGroupCard(g)));
    }
  }catch(e){
    container.innerHTML = '<div class="no-groups-msg">読み込みに失敗しました。</div>';
  }
}

/* ---- 振り返り ---- */
function showFeedback(feedbackId, msg, type){
  const el = document.getElementById(feedbackId);
  el.textContent=msg; el.className='feedback '+type;
  setTimeout(()=>{ el.className='feedback'; },3000);
}

async function saveReflection(){
  const btn = document.getElementById('save-btn');
  const btnStack = document.getElementById('save-stack-btn');
  if(btn) btn.disabled=true;
  if(btnStack) btnStack.disabled=true;
  const body={
    free_text:v('free_text'), woop_wish:v('woop_wish'), woop_outcome:v('woop_outcome'),
    woop_obstacle:v('woop_obstacle'), woop_plan:v('woop_plan'), want_to_do:v('want_to_do'),
    unconscious_desire:v('unconscious_desire'), implementation_intention:v('implementation_intention'),
  };
  const feedId = document.getElementById('pane-reflect').classList.contains('active')?'feedback':'feedback-stack';
  try {
    let res;
    if(existingId){
      res=await fetch('/reflections/'+existingId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    } else {
      const nonEmpty = Object.values(body).some(x=>x!==null);
      if(!nonEmpty){ showFeedback(feedId,'何か入力してから保存してください。','error'); if(btn)btn.disabled=false; if(btnStack)btnStack.disabled=false; return; }
      res=await fetch('/reflections',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...body,recorded_at:nowJST()})});
      if(res.ok){ const d=await res.json(); existingId=d.reflection?.id??null; }
    }
    showFeedback(feedId, res.ok?'保存しました。':'保存に失敗しました ('+res.status+')', res.ok?'success':'error');
  } catch(e){ showFeedback(feedId,'通信エラー: '+e.message,'error'); }
  if(btn) btn.disabled=false;
  if(btnStack) btnStack.disabled=false;
}

/* ---- streak ---- */
async function buildStreak(){
  const days=['日','月','火','水','木','金','土'];
  const container=document.getElementById('streakDots');
  const dates=[];
  for(let i=13;i>=0;i--){
    const d=new Date(Date.now()+9*60*60*1000); d.setDate(d.getDate()-i);
    dates.push(d.toISOString().slice(0,10));
  }
  let hitSet=new Set();
  try{ const r=await fetch('/reflections?limit=60'); const d=await r.json(); (d.reflections||[]).forEach(r=>hitSet.add(r.day)); }catch(e){}
  let hits=0;
  dates.forEach((date,i)=>{
    const hit=hitSet.has(date); const isToday=i===13;
    const d=new Date(date+'T00:00:00+09:00');
    const dot=document.createElement('div');
    dot.className='s-dot'+(hit?' hit':'')+(isToday?' today-dot':'');
    dot.textContent=days[d.getDay()];
    container.appendChild(dot);
    if(hit)hits++;
  });
  document.getElementById('streakCount').textContent=hits+'/14日 記録';
}

/* ---- init ---- */
async function init(){
  TODAY = todayJST();
  const d=new Date(TODAY);
  document.getElementById('navDate').textContent=
    `${d.getFullYear()} / ${String(d.getMonth()+1).padStart(2,'0')} / ${String(d.getDate()).padStart(2,'0')}`;
  buildStreak();
  loadGroups();
  // 振り返り読み込み
  try{
    const r=await fetch('/reflections/today');
    if(!r.ok) return;
    const data=await r.json();
    const ref=data.reflection;
    if(ref){
      existingId=ref.id;
      set('free_text',ref.free_text); set('woop_wish',ref.woop_wish);
      set('woop_outcome',ref.woop_outcome); set('woop_obstacle',ref.woop_obstacle);
      set('woop_plan',ref.woop_plan); set('want_to_do',ref.want_to_do);
      set('unconscious_desire',ref.unconscious_desire);
      set('implementation_intention',ref.implementation_intention);
    }
  }catch(e){}
}

init();
</script>
</body>
</html>
    """
    return HTMLResponse(content=html)



@router.get("/reflections/list", response_class=HTMLResponse)
def reflections_list_ui() -> HTMLResponse:
    html = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>振り返り一覧</title>
    <style>
      :root { color-scheme: light; }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        padding: 24px 20px 40px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f6f7fb;
        color: #111827;
      }
      .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
      }
      h1 { margin: 0; font-size: 22px; }
      a.write-btn {
        font-size: 13px;
        color: #6366f1;
        text-decoration: none;
      }
      .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 12px;
        cursor: pointer;
      }
      .card-date {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 8px;
      }
      .card-body { display: none; }
      .card.open .card-body { display: block; }
      .field-label {
        font-size: 11px;
        color: #9ca3af;
        margin-top: 10px;
        margin-bottom: 2px;
      }
      .field-value {
        font-size: 14px;
        color: #111827;
        white-space: pre-wrap;
        word-break: break-word;
      }
      .preview {
        font-size: 14px;
        color: #374151;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .empty {
        text-align: center;
        color: #9ca3af;
        margin-top: 60px;
        font-size: 15px;
      }
    </style>
  </head>
  <body>
    <div class="header">
      <h1>振り返り一覧</h1>
      <a class="write-btn" href="/ui/reflections">今日を書く →</a>
    </div>
    <div id="list"></div>

    <script>
      const LABELS = {
        free_text: "今日どうだった？",
        want_to_do: "やりたいこと（自己一致）",
        unconscious_desire: "無意識が求めること",
        anxiety: "不安なこと",
        woop_wish: "WOOP — Wish",
        woop_outcome: "WOOP — Outcome",
        woop_obstacle: "WOOP — Obstacle",
        woop_plan: "WOOP — Plan",
        implementation_intention: "明日の意図",
      };

      function escHtml(s) {
        return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
      }

      function firstText(r) {
        for (const key of Object.keys(LABELS)) {
          if (r[key]) return escHtml(r[key]);
        }
        return "（入力なし）";
      }

      function renderCard(r) {
        const card = document.createElement("div");
        card.className = "card";

        const fields = Object.entries(LABELS)
          .filter(([k]) => r[k])
          .map(([k, label]) => `
            <div class="field-label">${label}</div>
            <div class="field-value">${escHtml(r[k])}</div>
          `).join("");

        card.innerHTML = `
          <div class="card-date">${escHtml(r.day)}</div>
          <div class="preview">${firstText(r)}</div>
          <div class="card-body">${fields || "<div style='color:#9ca3af;font-size:13px;'>入力なし</div>"}</div>
        `;

        card.addEventListener("click", () => {
          card.classList.toggle("open");
          card.querySelector(".preview").style.display =
            card.classList.contains("open") ? "none" : "block";
        });

        return card;
      }

      async function init() {
        const listEl = document.getElementById("list");
        try {
          const res = await fetch("/reflections?limit=60");
          const data = await res.json();
          const reflections = data.reflections || [];
          if (reflections.length === 0) {
            listEl.innerHTML = '<div class="empty">まだ記録がありません。</div>';
            return;
          }
          reflections.forEach(r => listEl.appendChild(renderCard(r)));
        } catch (e) {
          listEl.innerHTML = '<div class="empty">読み込みに失敗しました。</div>';
        }
      }

      init();
    </script>
  </body>
</html>
    """
    return HTMLResponse(content=html)


@router.get("/habits", response_class=HTMLResponse)
def habits_ui() -> HTMLResponse:
    html = """
<!doctype html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>習慣グループ管理</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif;background:#fafaf9;color:#1a1a18;padding:20px 16px 48px;min-height:100vh}
.app{max-width:660px;margin:0 auto}
.top-nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px}
.nav-title{font-size:15px;font-weight:500}
.nav-link{font-size:12px;color:#7F77DD;text-decoration:none}
.add-row{display:flex;gap:8px;margin-bottom:24px}
.txt-inp{flex:1;padding:10px 12px;font-size:14px;font-family:inherit;border:1px solid #e8e8e5;border-radius:10px;background:#fff;color:#1a1a18;outline:none;transition:border-color .15s}
.txt-inp:focus{border-color:#7F77DD}
.btn-add{padding:10px 18px;font-size:13px;font-weight:600;color:#fff;background:#7F77DD;border:none;border-radius:10px;cursor:pointer;white-space:nowrap}
.btn-add:active{background:#534AB7}
.btn-add:disabled{background:#c4c0ef;cursor:default}
.group-card{background:#fff;border:1px solid #e8e8e5;border-radius:12px;margin-bottom:14px;overflow:hidden}
.group-head{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid #f0f0ee}
.group-name{font-size:14px;font-weight:500;color:#1a1a18;flex:1}
.group-name-inp{flex:1;border:none;outline:none;font-size:14px;font-weight:500;color:#1a1a18;background:transparent;font-family:inherit}
.btn-icon{background:none;border:none;cursor:pointer;font-size:13px;color:#bbb;padding:2px 6px;border-radius:6px;transition:color .15s}
.btn-icon:hover{color:#888;background:#f5f5f3}
.btn-del{color:#e0a0a0}.btn-del:hover{color:#dc2626;background:#fef2f2}
.items-area{padding:6px 14px 10px}
.item-row{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid #f8f8f6}
.item-row:last-child{border-bottom:none}
.item-text{flex:1;font-size:13px;color:#444}
.item-add-row{display:flex;gap:8px;margin-top:8px}
.item-txt-inp{flex:1;padding:7px 10px;font-size:13px;font-family:inherit;border:1px solid #e8e8e5;border-radius:8px;background:#fafaf9;color:#1a1a18;outline:none}
.item-txt-inp:focus{border-color:#7F77DD}
.btn-sm{padding:7px 14px;font-size:12px;font-weight:600;color:#fff;background:#7F77DD;border:none;border-radius:8px;cursor:pointer}
.btn-sm:disabled{background:#c4c0ef;cursor:default}
.woop-section{padding:8px 14px 12px;border-top:1px solid #f0f0ee;background:#faf9f7}
.woop-toggle{font-size:11px;color:#BA7517;cursor:pointer;font-weight:500;background:none;border:none;font-family:inherit;padding:0;margin-bottom:6px}
.woop-fields{display:none;flex-direction:column;gap:6px}
.woop-fields.open{display:flex}
.woop-row{display:flex;gap:6px;align-items:center}
.woop-key{font-size:10px;font-weight:500;color:#BA7517;min-width:14px}
.woop-inp{flex:1;border:none;border-bottom:1px solid #e8e8e5;outline:none;font-size:12px;color:#555;background:transparent;font-family:inherit;padding:2px 0}
.woop-inp::placeholder{color:#ccc}
.woop-save{margin-top:8px;font-size:12px;color:#7F77DD;background:none;border:none;cursor:pointer;font-family:inherit;padding:0}
.empty-msg{text-align:center;color:#bbb;font-size:13px;padding:32px 0}
</style>
</head>
<body>
<div class="app">
  <div class="top-nav">
    <span class="nav-title">習慣グループ管理</span>
    <a class="nav-link" href="/ui/reflections">← 振り返りに戻る</a>
  </div>
  <div class="add-row">
    <input class="txt-inp" id="new-group" type="text" placeholder="新しいグループ名（例：朝の習慣）">
    <button class="btn-add" onclick="addGroup()">追加</button>
  </div>
  <div id="groupList"></div>
</div>

<script>
function escHtml(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

async function load(){
  const res = await fetch('/habit-groups');
  const data = await res.json();
  render(data.groups || []);
}

function render(groups){
  const el = document.getElementById('groupList');
  el.innerHTML = '';
  if(groups.length === 0){
    el.innerHTML = '<div class="empty-msg">グループがありません。上から追加してください。</div>';
    return;
  }
  groups.forEach(g => el.appendChild(buildCard(g)));
}

function buildCard(group){
  const card = document.createElement('div');
  card.className = 'group-card';
  card.dataset.id = group.id;

  const itemsHtml = group.items.map(item => `
    <div class="item-row" data-item-id="${item.id}">
      <span class="item-text">${escHtml(item.content)}</span>
      <button class="btn-icon btn-del" onclick="deleteItem(${item.id}, this)">✕</button>
    </div>`).join('') || '';

  const hasWoop = group.woop_wish || group.woop_outcome || group.woop_obstacle || group.woop_plan;

  card.innerHTML = `
    <div class="group-head">
      <input class="group-name-inp" value="${escHtml(group.name)}" onblur="renameGroup(${group.id}, this)">
      <button class="btn-icon btn-del" onclick="deleteGroup(${group.id}, this)" title="グループ削除">🗑</button>
    </div>
    <div class="items-area">
      ${itemsHtml}
      <div class="item-add-row">
        <input class="item-txt-inp" type="text" placeholder="習慣を追加（例：水を200ml飲む）">
        <button class="btn-sm" onclick="addItem(${group.id}, this)">追加</button>
      </div>
    </div>
    <div class="woop-section">
      <button class="woop-toggle" onclick="toggleWoop(this)">${hasWoop ? '▼ WOOP を編集' : '▶ WOOP を設定（任意）'}</button>
      <div class="woop-fields${hasWoop ? ' open' : ''}">
        <div class="woop-row"><span class="woop-key">W</span><input class="woop-inp" placeholder="Wish — 達成したいこと" value="${escHtml(group.woop_wish||'')}"></div>
        <div class="woop-row"><span class="woop-key">O</span><input class="woop-inp" placeholder="Outcome — 達成したらどんな感覚？" value="${escHtml(group.woop_outcome||'')}"></div>
        <div class="woop-row"><span class="woop-key">O</span><input class="woop-inp" placeholder="Obstacle — 邪魔しそうな障害は？" value="${escHtml(group.woop_obstacle||'')}"></div>
        <div class="woop-row"><span class="woop-key">P</span><input class="woop-inp" placeholder="Plan — もし障害が起きたら？" value="${escHtml(group.woop_plan||'')}"></div>
        <button class="woop-save" onclick="saveWoop(${group.id}, this)">保存する</button>
      </div>
    </div>`;

  card.querySelector('.item-txt-inp').addEventListener('keydown', e => {
    if(e.key === 'Enter') card.querySelector('.btn-sm').click();
  });
  return card;
}

function toggleWoop(btn){
  const fields = btn.nextElementSibling;
  const open = fields.classList.toggle('open');
  btn.textContent = open ? '▼ WOOP を編集' : '▶ WOOP を設定（任意）';
}

async function addGroup(){
  const inp = document.getElementById('new-group');
  const name = inp.value.trim();
  if(!name) return;
  const res = await fetch('/habit-groups', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({name, sort_order: 0})
  });
  if(res.ok){ inp.value = ''; load(); }
}

async function renameGroup(id, inp){
  const name = inp.value.trim();
  if(!name){ inp.value = inp.dataset.prev || inp.value; return; }
  await fetch('/habit-groups/'+id, {
    method:'PATCH', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({name})
  });
}

async function deleteGroup(id, btn){
  if(!confirm('グループとすべての習慣を削除しますか？')) return;
  btn.disabled = true;
  const res = await fetch('/habit-groups/'+id, {method:'DELETE'});
  if(res.ok) load();
  else btn.disabled = false;
}

async function addItem(groupId, btn){
  const row = btn.closest('.item-add-row');
  const inp = row.querySelector('.item-txt-inp');
  const content = inp.value.trim();
  if(!content) return;
  btn.disabled = true;
  const res = await fetch('/habit-groups/'+groupId+'/items', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({content, sort_order: 0})
  });
  if(res.ok){ inp.value = ''; load(); }
  else btn.disabled = false;
}

async function deleteItem(itemId, btn){
  btn.disabled = true;
  const res = await fetch('/habit-groups/items/'+itemId, {method:'DELETE'});
  if(res.ok) load();
  else btn.disabled = false;
}

async function saveWoop(groupId, btn){
  const section = btn.closest('.woop-fields');
  const inps = section.querySelectorAll('.woop-inp');
  const body = {
    woop_wish: inps[0].value.trim() || null,
    woop_outcome: inps[1].value.trim() || null,
    woop_obstacle: inps[2].value.trim() || null,
    woop_plan: inps[3].value.trim() || null,
  };
  btn.disabled = true;
  const res = await fetch('/habit-groups/'+groupId, {
    method:'PATCH', headers:{'Content-Type':'application/json'},
    body: JSON.stringify(body)
  });
  btn.disabled = false;
  if(res.ok){ btn.textContent = '保存しました ✓'; setTimeout(()=>{ btn.textContent = '保存する'; },2000); }
}

document.getElementById('new-group').addEventListener('keydown', e => {
  if(e.key === 'Enter') addGroup();
});

load();
</script>
</body>
</html>
    """
    return HTMLResponse(content=html)


@router.get("/wishes", response_class=HTMLResponse)
def wishes_ui() -> HTMLResponse:
    html = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>やりたいことリスト</title>
    <style>
      :root { color-scheme: light; }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        padding: 24px 20px 40px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f6f7fb;
        color: #111827;
      }
      h1 { margin: 0 0 24px; font-size: 22px; }
      .add-row {
        display: flex;
        gap: 8px;
        margin-bottom: 24px;
      }
      input {
        flex: 1;
        padding: 10px 12px;
        font-size: 15px;
        font-family: inherit;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        background: #fff;
        color: #111827;
        outline: none;
        transition: border-color 0.15s;
      }
      input:focus { border-color: #6366f1; }
      .btn {
        padding: 10px 18px;
        font-size: 14px;
        font-weight: 600;
        color: #fff;
        background: #6366f1;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        white-space: nowrap;
        transition: background 0.15s;
      }
      .btn:active { background: #4f46e5; }
      .btn:disabled { background: #a5b4fc; cursor: default; }
      .btn-danger {
        padding: 4px 10px;
        font-size: 12px;
        background: transparent;
        color: #9ca3af;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        cursor: pointer;
        transition: color 0.15s, border-color 0.15s;
      }
      .btn-danger:hover { color: #dc2626; border-color: #dc2626; }
      .category {
        background: #fff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        margin-bottom: 16px;
        overflow: hidden;
      }
      .category-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 16px;
        border-bottom: 1px solid #f3f4f6;
      }
      .category-name { font-weight: 600; font-size: 16px; }
      .items { padding: 8px 16px 12px; }
      .item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #f3f4f6;
        font-size: 15px;
      }
      .item:last-child { border-bottom: none; }
      .item-add-row {
        display: flex;
        gap: 8px;
        margin-top: 10px;
      }
      .empty-cat { font-size: 13px; color: #9ca3af; padding: 4px 0 8px; }
    </style>
  </head>
  <body>
    <h1>やりたいことリスト</h1>

    <div class="add-row">
      <input id="new-cat" type="text" placeholder="新しいカテゴリ（例: 本）" />
      <button class="btn" onclick="addCategory()">追加</button>
    </div>

    <div id="list"></div>

    <script>
      async function load() {
        const res = await fetch("/wishes/categories");
        const data = await res.json();
        render(data.categories || []);
      }

      function render(categories) {
        const listEl = document.getElementById("list");
        listEl.innerHTML = "";
        if (categories.length === 0) {
          listEl.innerHTML = '<div style="text-align:center;color:#9ca3af;margin-top:40px;font-size:15px;">カテゴリがありません</div>';
          return;
        }
        categories.forEach(cat => listEl.appendChild(buildCategory(cat)));
      }

      function buildCategory(cat) {
        const el = document.createElement("div");
        el.className = "category";
        el.dataset.id = cat.id;

        const itemsHtml = cat.items.length === 0
          ? '<div class="empty-cat">アイテムなし</div>'
          : cat.items.map(item => `
              <div class="item" data-item-id="${item.id}">
                <span>${escHtml(item.content)}</span>
                <button class="btn-danger" onclick="deleteItem(${item.id}, this)">削除</button>
              </div>`).join("");

        el.innerHTML = `
          <div class="category-header">
            <span class="category-name">${escHtml(cat.name)}</span>
            <button class="btn-danger" onclick="deleteCategory(${cat.id}, this)">カテゴリ削除</button>
          </div>
          <div class="items">
            ${itemsHtml}
            <div class="item-add-row">
              <input type="text" placeholder="やりたいことを追加" data-cat-id="${cat.id}" />
              <button class="btn" onclick="addItem(${cat.id}, this)">追加</button>
            </div>
          </div>`;
        return el;
      }

      function escHtml(str) {
        return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
      }

      async function addCategory() {
        const input = document.getElementById("new-cat");
        const name = input.value.trim();
        if (!name) return;
        const res = await fetch("/wishes/categories", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name }),
        });
        if (res.ok) { input.value = ""; load(); }
      }

      async function deleteCategory(id, btn) {
        if (!confirm("カテゴリとアイテムをすべて削除しますか？")) return;
        btn.disabled = true;
        const res = await fetch("/wishes/categories/" + id, { method: "DELETE" });
        if (res.ok) load();
        else btn.disabled = false;
      }

      async function addItem(categoryId, btn) {
        const row = btn.closest(".item-add-row");
        const input = row.querySelector("input");
        const content = input.value.trim();
        if (!content) return;
        btn.disabled = true;
        const res = await fetch("/wishes/categories/" + categoryId + "/items", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content }),
        });
        if (res.ok) { input.value = ""; load(); }
        else btn.disabled = false;
      }

      async function deleteItem(id, btn) {
        btn.disabled = true;
        const res = await fetch("/wishes/items/" + id, { method: "DELETE" });
        if (res.ok) load();
        else btn.disabled = false;
      }

      document.getElementById("new-cat").addEventListener("keydown", e => {
        if (e.key === "Enter") addCategory();
      });

      load();
    </script>
  </body>
</html>
    """
    return HTMLResponse(content=html)


@router.get("/steps", response_class=HTMLResponse)
def steps_ui() -> HTMLResponse:
    html = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Daily Steps</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      :root {
        color-scheme: light;
      }
      body {
        margin: 0;
        padding: 24px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f6f7fb;
        color: #111827;
      }
      .container {
        max-width: 980px;
        margin: 0 auto;
      }
      h1 {
        margin: 0 0 16px;
        font-size: 24px;
      }
      .meta,
      .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 8px;
        margin-bottom: 16px;
      }
      .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 12px;
      }
      .label {
        font-size: 12px;
        color: #6b7280;
      }
      .value {
        margin-top: 6px;
        font-size: 18px;
        font-weight: 600;
      }
      .chart-card {
        height: 420px;
      }
      .error {
        color: #b91c1c;
        margin-top: 8px;
      }
      .footnote {
        margin-top: 12px;
        font-size: 12px;
        color: #6b7280;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>歩数（日次）</h1>

      <div class="meta">
        <div class="card">
          <div class="label">start_day</div>
          <div id="start-day" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">end_day</div>
          <div id="end-day" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">rows件数</div>
          <div id="rows-count" class="value">0</div>
        </div>
      </div>

      <div class="card chart-card">
        <canvas id="steps-chart"></canvas>
      </div>
      <div id="error" class="error"></div>
      <div class="footnote">source: health_connect / metric: steps_total / days: 90</div>

      <div class="stats" style="margin-top: 16px;">
        <div class="card">
          <div class="label">最新値</div>
          <div id="latest" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">前日差分</div>
          <div id="day-diff" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">週平均差</div>
          <div id="week-diff" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">7日移動平均</div>
          <div id="dma7-latest" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">平均 (mean)</div>
          <div id="mean" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">標準偏差 (std)</div>
          <div id="std" class="value">-</div>
        </div>
      </div>
    </div>

    <script>
      const endpoint = "/metrics/daily?metric=steps_total&source=health_connect&days=90";

      function mean(values) {
        if (values.length === 0) return null;
        return values.reduce((sum, v) => sum + v, 0) / values.length;
      }

      function std(values, avg) {
        if (values.length === 0 || avg === null) return null;
        const variance = values.reduce((sum, v) => sum + (v - avg) ** 2, 0) / values.length;
        return Math.sqrt(variance);
      }

      function movingAverage(values, windowSize) {
        const result = [];
        for (let i = 0; i < values.length; i++) {
          if (i < windowSize - 1) {
            result.push(null);
            continue;
          }
          let sum = 0;
          for (let j = i - windowSize + 1; j <= i; j++) {
            sum += values[j];
          }
          result.push(sum / windowSize);
        }
        return result;
      }

      function formatNumber(value, fractionDigits = 1) {
        if (value === null || !Number.isFinite(value)) return "-";
        return value.toLocaleString("ja-JP", {
          minimumFractionDigits: fractionDigits,
          maximumFractionDigits: fractionDigits,
        });
      }

      async function init() {
        const startDayEl = document.getElementById("start-day");
        const endDayEl = document.getElementById("end-day");
        const rowsCountEl = document.getElementById("rows-count");
        const latestEl = document.getElementById("latest");
        const dayDiffEl = document.getElementById("day-diff");
        const weekDiffEl = document.getElementById("week-diff");
        const meanEl = document.getElementById("mean");
        const stdEl = document.getElementById("std");
        const dma7LatestEl = document.getElementById("dma7-latest");
        const errorEl = document.getElementById("error");

        try {
          const res = await fetch(endpoint);
          if (!res.ok) {
            throw new Error("fetch failed: " + res.status);
          }

          const payload = await res.json();
          const rows = Array.isArray(payload.rows) ? payload.rows : [];
          const labels = rows.map((r) => r.day);
          const values = rows.map((r) => Number(r.value ?? 0));
          const dma7 = movingAverage(values, 7);

          startDayEl.textContent = payload.start_day ?? "-";
          endDayEl.textContent = payload.end_day ?? "-";
          rowsCountEl.textContent = String(rows.length);

          const avg = mean(values);
          const sigma = std(values, avg);
          const dma7Latest = dma7.filter((v) => Number.isFinite(v)).slice(-1)[0] ?? null;

          // 最新値・前日差分・週平均差
          const latestVal = values.length > 0 ? values[values.length - 1] : null;
          const prevVal = values.length > 1 ? values[values.length - 2] : null;
          const week7 = values.length >= 7 ? values.slice(-7) : null;
          const week7avg = week7 ? mean(week7) : null;

          latestEl.textContent = latestVal !== null ? Math.round(latestVal).toLocaleString("ja-JP") + " 歩" : "-";

          if (latestVal !== null && prevVal !== null) {
            const diff = Math.round(latestVal - prevVal);
            dayDiffEl.textContent = (diff >= 0 ? "+" : "") + diff.toLocaleString("ja-JP") + " 歩";
            dayDiffEl.style.color = diff >= 0 ? "#16a34a" : "#dc2626";
          } else {
            dayDiffEl.textContent = "-";
          }

          if (latestVal !== null && week7avg !== null) {
            const wdiff = Math.round(latestVal - week7avg);
            weekDiffEl.textContent = (wdiff >= 0 ? "+" : "") + wdiff.toLocaleString("ja-JP") + " 歩";
            weekDiffEl.style.color = wdiff >= 0 ? "#16a34a" : "#dc2626";
          } else {
            weekDiffEl.textContent = "-";
          }

          meanEl.textContent = formatNumber(avg);
          stdEl.textContent = formatNumber(sigma);
          dma7LatestEl.textContent = formatNumber(dma7Latest);

          const ctx = document.getElementById("steps-chart");
          new Chart(ctx, {
            type: "line",
            data: {
              labels,
              datasets: [
                {
                  label: "steps_total",
                  data: values,
                  borderColor: "#1d4ed8",
                  backgroundColor: "rgba(29, 78, 216, 0.12)",
                  tension: 0,
                  pointRadius: 2,
                  pointHoverRadius: 4,
                  fill: false,
                },
                {
                  label: "7dma",
                  data: dma7,
                  borderColor: "#dc2626",
                  tension: 0,
                  borderDash: [6, 4],
                  pointRadius: 0,
                  spanGaps: true,
                },
              ],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              interaction: {
                mode: "index",
                intersect: false,
              },
              scales: {
                y: {
                  beginAtZero: true,
                  title: {
                    display: true,
                    text: "steps",
                  },
                },
              },
            },
          });
        } catch (err) {
          errorEl.textContent = "データ取得に失敗しました: " + err.message;
        }
      }

      init();
    </script>
  </body>
</html>
    """
    return HTMLResponse(content=html)
