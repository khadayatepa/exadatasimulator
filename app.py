import streamlit as st
from openai import OpenAI
from scenarios import SCENARIOS, PHASE_INFO, CATEGORY_ICONS

st.set_page_config(page_title="Exadata X8M/X10M DBA Simulator", page_icon="🔴",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
.topbar{background:#060e1c;border-bottom:3px solid #e74c3c;padding:10px 20px 8px;margin:-1rem -1rem 0 -1rem;display:flex;align-items:center;gap:14px;}
.t-logo{font-size:9px;color:#e74c3c;letter-spacing:3px;text-transform:uppercase;font-weight:700;font-family:'JetBrains Mono',monospace;}
.t-title{font-size:16px;color:#d0e8f8;font-weight:600;}
.t-sub{font-size:11px;color:#4a7ab5;margin-top:1px;}
.t-right{margin-left:auto;display:flex;gap:8px;align-items:center;}
.pill{background:#0d1e35;border:1px solid #1e3a5f;border-radius:20px;padding:3px 12px;font-size:11px;color:#8aadcc;font-family:'JetBrains Mono',monospace;}
.pill b{color:#f39c12;}.pill.ok{background:#0a2a18;border-color:#1a5a30;color:#5dc888;}.pill.no{background:#2a0a0a;border-color:#5a1a1a;color:#e87a5a;}
.sv-header{background:#0d1e35;border:1px solid #1e3a5f;border-radius:8px;padding:14px 16px;margin-bottom:10px;}
.sv-title{font-size:17px;color:#d0e8f8;font-weight:700;margin-bottom:5px;}
.sv-env{font-size:10px;color:#4a7ab5;font-family:'JetBrains Mono',monospace;margin-bottom:8px;}
.sv-problem{font-size:12px;color:#c8dff0;line-height:1.6;background:#060e1c;border-left:3px solid #e74c3c;padding:8px 12px;border-radius:0 4px 4px 0;margin-top:6px;}
.sv-section{margin:10px 0 5px;font-size:10px;color:#4a7ab5;letter-spacing:1.5px;text-transform:uppercase;font-family:'JetBrains Mono',monospace;}
.symptom-row{background:#060e1c;border:1px solid #1e3a5f;border-radius:3px;padding:4px 10px;margin-bottom:3px;font-size:11px;color:#c8dff0;font-family:'JetBrains Mono',monospace;}
.task-row{background:#060e1c;border:1px solid #1e3a5f;border-radius:3px;padding:5px 10px;margin-bottom:3px;font-size:11px;color:#c8dff0;display:flex;align-items:flex-start;gap:6px;}
.task-done{background:#0a2a18 !important;border-color:#1a5a30 !important;}
.task-num{color:#f39c12;font-weight:700;font-family:'JetBrains Mono',monospace;flex-shrink:0;min-width:18px;}
.mock-log{background:#020810;border:1px solid #1a4a2a;border-radius:5px;padding:10px 12px;font-family:'JetBrains Mono',monospace;font-size:10px;color:#7ae0a0;white-space:pre-wrap;line-height:1.5;max-height:260px;overflow-y:auto;}
.chat-user{background:#150808;border:1px solid #3a1010;border-radius:10px 10px 3px 10px;padding:9px 13px;margin:5px 0 5px 60px;color:#f0d0d0;font-size:13px;line-height:1.6;}
.chat-bot{background:#0d1e35;border:1px solid #1e3a5f;border-radius:10px 10px 10px 3px;padding:9px 13px;margin:5px 0;color:#c8dff0;font-size:13px;line-height:1.65;font-family:'JetBrains Mono',monospace;white-space:pre-wrap;}
.chat-sys{background:#111108;border:1px solid #3a3a10;border-radius:6px;padding:7px 12px;margin:5px 10px;color:#e0d898;font-size:11px;font-family:'JetBrains Mono',monospace;}
.term-hdr{background:#020810;border:1px solid #1a4a2a;border-radius:5px 5px 0 0;padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#5dc888;}
.prog-wrap{background:#1e3a5f;border-radius:3px;height:5px;margin:5px 0 8px;}
.prog-bar{background:#27ae60;border-radius:3px;height:100%;transition:width .3s;}
.tag{font-size:9px;padding:2px 7px;border-radius:3px;font-family:'JetBrains Mono',monospace;border:1px solid;}
[data-testid="stSidebar"]{background:#070f1e !important;border-right:1px solid #1e3a5f;min-width:225px !important;max-width:225px !important;}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] span{color:#8aadcc !important;font-size:11px !important;}
[data-testid="stSidebar"] .stButton > button{background:transparent !important;border:1px solid #1e3a5f !important;color:#8aadcc !important;text-align:left !important;width:100% !important;border-radius:4px !important;font-size:11px !important;padding:5px 9px !important;margin-bottom:2px !important;}
[data-testid="stSidebar"] .stButton > button:hover{background:#122240 !important;border-color:#2a5080 !important;color:#c8dff0 !important;}
[data-testid="stSidebar"] .stButton > button[kind="primary"]{background:#1a0a0a !important;border-color:#e74c3c !important;color:#e74c3c !important;}
.stTextInput label,.stSelectbox label{color:#8aadcc !important;font-size:11px !important;}
.stTextInput input,.stSelectbox > div > div{background:#0d1e35 !important;border-color:#1e3a5f !important;color:#c8dff0 !important;font-size:12px !important;}
.main .block-container{background:#0a1628;padding-top:0;max-width:100% !important;}
.stApp{background:#0a1628;}
hr{border-color:#1e3a5f !important;margin:6px 0 !important;}
</style>""", unsafe_allow_html=True)

# ── Session state ──
DEFAULTS = {
    "openai_key":"","openai_model":"gpt-4o","phase":"Basic",
    "current_scenario":None,"messages":[],"tasks_done":set(),
    "total_score":0,"scenarios_attempted":0,"scenarios_completed":0,
    "correct_answers":0,"hint_count":0,"chat_mode":"guided",
    "env_rack":"Exadata X8M","env_db":"Oracle 19c RAC","env_role":"DBA","env_level":"Intermediate",
}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v

def get_sc(): return SCENARIOS.get(st.session_state.current_scenario)

def build_sys(sc):
    return f"""You are ExaSimBot — Oracle Exadata X8M/X10M Senior DBA Simulator & Trainer.

SCENARIO: {sc['title']} | Phase:{sc['phase']} | {sc['category']} | Priority:{sc['priority']}
ENV: {sc['env']}
PROBLEM: {sc['problem']}
SYMPTOMS:
{chr(10).join(f'  - {s}' for s in sc['symptoms'])}
TASKS:
{chr(10).join(f'  {i+1}. {t}' for i,t in enumerate(sc['tasks']))}
USER: Role={st.session_state.env_role} Level={st.session_state.env_level} Mode={st.session_state.chat_mode}

RULES:
1. Commands in triple-backtick blocks with correct prompt (CellCLI>, SQL>, RMAN>, DGMGRL>, $, #)
2. Show realistic Exadata output after every command
3. guided mode: walk through each task, prompt next step after success
4. quiz mode: ask MCQ questions (A/B/C/D) and score them
5. freeplay mode: answer freely
6. Evaluate user commands: say CORRECT ✓ (+10 pts) or WRONG ✗ with the right answer
7. Reference mock logs when relevant — ground everything in the scenario reality
8. Level adaptation: Basic=full hints, Intermediate=partial hints, Advanced=minimal hints

X8M: Compute=2x48-core Cascade Lake,6TB RAM,3.2TB PMEM; Cell=12x7.2TB HDD+4x6.4TB NVMe+1.5TB PMEM; Full rack=8+14+3 IB
X10M: Compute=2x96-core Sapphire Rapids,8TB DDR5,4TB PMEM; Cell=12x18TB HDD+4x12.8TB NVMe+2TB PMEM

Be a senior DBA mentor. Keep responses focused and practical."""

def call_api(user_text, sc, show_user=True):
    if not st.session_state.openai_key:
        st.markdown('<div class="chat-sys">⚠️ Enter your OpenAI API key in the top bar.</div>',unsafe_allow_html=True)
        return ""
    if show_user:
        st.markdown(f'<div class="chat-user">👤 {user_text}</div>',unsafe_allow_html=True)
    msgs = [{"role":"system","content":build_sys(sc)}]
    for m in st.session_state.messages[-20:]:
        msgs.append({"role":m["role"],"content":m["content"]})
    msgs.append({"role":"user","content":user_text})
    ph = st.empty(); full=""
    try:
        client = OpenAI(api_key=st.session_state.openai_key)
        stream = client.chat.completions.create(model=st.session_state.openai_model,
            messages=msgs,max_tokens=1800,temperature=0.3,stream=True)
        for chunk in stream:
            d = chunk.choices[0].delta.content if chunk.choices else None
            if d:
                full+=d
                ph.markdown(f'<div class="chat-bot">{full}▌</div>',unsafe_allow_html=True)
        ph.markdown(f'<div class="chat-bot">{full}</div>',unsafe_allow_html=True)
        if "CORRECT ✓" in full or "correct ✓" in full.lower():
            st.session_state.total_score+=10; st.session_state.correct_answers+=1
    except Exception as e:
        err=str(e)
        full=("⚠️ Invalid API key." if "401" in err else
              "⚠️ Rate limit hit." if "429" in err else f"⚠️ OpenAI error: {err}")
        ph.markdown(f'<div class="chat-bot">{full}</div>',unsafe_allow_html=True)
    st.session_state.messages.append({"role":"user","content":user_text})
    st.session_state.messages.append({"role":"assistant","content":full})
    return full

def start_scenario(key):
    sc=SCENARIOS[key]; st.session_state.current_scenario=key
    st.session_state.messages=[]; st.session_state.tasks_done=set()
    st.session_state.scenarios_attempted+=1
    intro=(f"[SCENARIO START: {sc['title']}][{sc['phase']}|{sc['category']}|{sc['priority']}]"
           f"[Role:{st.session_state.env_role}|Level:{st.session_state.env_level}|Mode:{st.session_state.chat_mode}]\n\n"
           f"Give me a situation briefing for this scenario. Reference the mock logs. "
           f"Then guide me through Task 1 with the exact diagnostic command to run first.")
    with st.spinner(f"Loading: {sc['title']}…"): call_api(intro,sc,show_user=False)

# ── TOP BAR ──
api_ok=bool(st.session_state.openai_key); sc=get_sc()
st.markdown(f"""<div class="topbar"><div><div class="t-logo">Oracle Exadata</div>
<div class="t-title">X8M / X10M DBA Hands-On Simulator</div>
<div class="t-sub">Incident · Change · Problem · Config · Automation — Basic / Standard / Advanced</div></div>
<div class="t-right">
<span class="pill">Completed: <b>{st.session_state.scenarios_completed}</b>/{st.session_state.scenarios_attempted}</span>
<span class="pill">Score: <b>{st.session_state.total_score}</b></span>
<span class="pill">Correct: <b>{st.session_state.correct_answers}</b></span>
<span class="pill {'ok' if api_ok else 'no'}">{'✅ OpenAI' if api_ok else '⚠️ No Key'}</span>
</div></div>""",unsafe_allow_html=True)

# ── CONFIG ROW ──
c1,c2,c3,c4,c5,c6,c7=st.columns([2.2,1.4,1.4,1.3,1.1,1.3,1.1])
with c1:
    k=st.text_input("OpenAI API Key",type="password",value=st.session_state.openai_key,placeholder="sk-…")
    if k: st.session_state.openai_key=k
with c2:
    mo=["gpt-4o","gpt-4-turbo","gpt-4o-mini","gpt-3.5-turbo"]
    cur=st.session_state.openai_model if st.session_state.openai_model in mo else "gpt-4o"
    st.session_state.openai_model=st.selectbox("Model",mo,index=mo.index(cur))
with c3:
    ro=["Exadata X8M","Exadata X10M","Both"]
    cur2=st.session_state.env_rack if st.session_state.env_rack in ro else "Exadata X8M"
    st.session_state.env_rack=st.selectbox("Hardware",ro,index=ro.index(cur2))
with c4:
    do=["Oracle 19c RAC","Oracle 23ai RAC","Oracle 19c SI","Oracle 23ai SI"]
    cur3=st.session_state.env_db if st.session_state.env_db in do else "Oracle 19c RAC"
    st.session_state.env_db=st.selectbox("Database",do,index=do.index(cur3))
with c5:
    rlo=["DBA","DMA","Both"]
    st.session_state.env_role=st.selectbox("Role",rlo,index=rlo.index(st.session_state.env_role) if st.session_state.env_role in rlo else 0)
with c6:
    lvo=["Basic","Intermediate","Advanced"]
    st.session_state.env_level=st.selectbox("Level",lvo,index=lvo.index(st.session_state.env_level) if st.session_state.env_level in lvo else 1)
with c7:
    mdo=["guided","freeplay","quiz"]
    cur4=st.session_state.chat_mode if st.session_state.chat_mode in mdo else "guided"
    st.session_state.chat_mode=st.selectbox("Mode",mdo,index=mdo.index(cur4))

st.markdown("<div style='height:3px'></div>",unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 📚 Scenario Library")
    for pn,pi in PHASE_INFO.items():
        cnt=sum(1 for s in SCENARIOS.values() if s["phase"]==pn)
        if st.button(f"{pi['icon']} {pn}  ({cnt})",key=f"ph_{pn}",use_container_width=True,
                     type="primary" if st.session_state.phase==pn else "secondary"):
            st.session_state.phase=pn; st.rerun()
    st.markdown("---")
    all_cats=list(dict.fromkeys(s["category"] for s in SCENARIOS.values()))
    cat_f=st.selectbox("Category",["All"]+all_cats,key="cat_f")
    phase_sc={k:v for k,v in SCENARIOS.items() if v["phase"]==st.session_state.phase}
    if cat_f!="All": phase_sc={k:v for k,v in phase_sc.items() if v["category"]==cat_f}
    st.markdown(f"**{len(phase_sc)} scenarios**")
    for key,sv in phase_sc.items():
        is_cur=st.session_state.current_scenario==key
        pr={"P1":"🔴","P2":"🟡","P3":"🔵","P4":"🟢"}.get(sv["priority"],"⚪")
        lbl=f"{sv['icon']} {pr} {sv['title']}"
        if st.button(lbl,key=f"sc_{key}",use_container_width=True,type="primary" if is_cur else "secondary"):
            if not is_cur: start_scenario(key); st.rerun()
    st.markdown("---")
    st.markdown("**Session Stats**")
    st.metric("Total Score",st.session_state.total_score)
    st.metric("Completed",st.session_state.scenarios_completed)
    st.metric("Correct Answers",st.session_state.correct_answers)
    if st.button("🔄 Reset Session",use_container_width=True):
        for k in ["messages","tasks_done","total_score","scenarios_attempted","scenarios_completed",
                  "correct_answers","hint_count","current_scenario"]:
            st.session_state[k]=DEFAULTS.get(k,None if k=="current_scenario" else(set() if k=="tasks_done" else 0))
        st.session_state.messages=[]; st.rerun()

# ── MAIN ──
sc=get_sc()
if sc is None:
    pi=PHASE_INFO[st.session_state.phase]
    st.markdown(f"""<div style="background:#0d1e35;border:1px solid #1e3a5f;border-radius:10px;
padding:24px 28px;margin:8px 0">
<div style="font-size:9px;color:#4a7ab5;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px">
Oracle Exadata DBA Simulator</div>
<div style="font-size:22px;color:#d0e8f8;font-weight:700;margin-bottom:10px">
{pi['icon']} {st.session_state.phase} Phase</div>
<div style="font-size:13px;color:#8aadcc;line-height:1.7">{pi['description']}<br>
Select a scenario from the sidebar, or click Start below.</div></div>""",unsafe_allow_html=True)

    # Phase overview
    cols=st.columns(3)
    for i,(pn,pi2) in enumerate(PHASE_INFO.items()):
        sc_in=[s for s in SCENARIOS.values() if s["phase"]==pn]
        cats=list(dict.fromkeys(s["category"] for s in sc_in))
        with cols[i]:
            st.markdown(f"""<div style="background:#0d1e35;border:1px solid {pi2['border']};
border-radius:8px;padding:14px 16px">
<div style="font-size:13px;color:{pi2['color']};font-weight:700;margin-bottom:5px">{pi2['icon']} {pn}</div>
<div style="font-size:11px;color:#8aadcc;margin-bottom:6px">{pi2['description']}</div>
<div style="font-size:10px;color:#4a7ab5">{len(sc_in)} scenarios · {" · ".join(cats)}</div>
</div>""",unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### All Scenarios")
    hc=st.columns([2.2,1.4,0.8,0.8,0.8,1])
    for h,t in zip(hc,["Scenario","Category","Priority","Difficulty","Phase","Action"]):
        h.markdown(f"<small style='color:#4a7ab5'>{t}</small>",unsafe_allow_html=True)
    for key,sv in SCENARIOS.items():
        pr_col={"P1":"🔴","P2":"🟡","P3":"🔵","P4":"🟢"}.get(sv["priority"],"⚪")
        c1,c2,c3,c4,c5,c6=st.columns([2.2,1.4,0.8,0.8,0.8,1])
        c1.markdown(f"<span style='color:#c8dff0;font-size:11px'>{sv['icon']} {sv['title']}</span>",unsafe_allow_html=True)
        c2.markdown(f"<span style='color:#8aadcc;font-size:10px'>{CATEGORY_ICONS.get(sv['category'],'')} {sv['category']}</span>",unsafe_allow_html=True)
        c3.markdown(f"<span style='font-size:11px'>{pr_col} {sv['priority']}</span>",unsafe_allow_html=True)
        c4.markdown(f"<span style='color:#8aadcc;font-size:10px'>{sv['difficulty']}</span>",unsafe_allow_html=True)
        c5.markdown(f"<span style='color:#8aadcc;font-size:10px'>{sv['phase']}</span>",unsafe_allow_html=True)
        if c6.button("▶ Start",key=f"tbl_{key}",use_container_width=True):
            st.session_state.phase=sv["phase"]; start_scenario(key); st.rerun()

else:
    col_info,col_chat=st.columns([1.3,2.7])

    with col_info:
        pi=PHASE_INFO[sc["phase"]]
        pr_c={"P1":"#e74c3c","P2":"#f39c12","P3":"#5da8e8","P4":"#5dc888"}.get(sc["priority"],"#8aadcc")
        st.markdown(f"""<div class="sv-header">
<div style="display:flex;gap:6px;margin-bottom:6px;flex-wrap:wrap">
<span class="tag" style="background:{pi['bg']};color:{pi['color']};border-color:{pi['border']}">{pi['icon']} {sc['phase']}</span>
<span class="tag" style="color:{pr_c};background:#060e1c;border-color:{pr_c}55">{sc['priority']}</span>
<span class="tag" style="background:#0a1f2a;color:#5da8e8;border-color:#1a3a5a">{CATEGORY_ICONS.get(sc['category'],'')} {sc['category']}</span>
<span class="tag" style="background:#0a2a18;color:#5dc888;border-color:#1a5a30">{sc['difficulty']}</span>
</div>
<div class="sv-title">{sc['icon']} {sc['title']}</div>
<div class="sv-env">🖥️ {sc['env']}</div>
<div class="sv-problem">{sc['problem']}</div></div>""",unsafe_allow_html=True)

        st.markdown('<div class="sv-section">⚠ Symptoms / Alerts</div>',unsafe_allow_html=True)
        for sym in sc["symptoms"]:
            st.markdown(f'<div class="symptom-row">▸ {sym}</div>',unsafe_allow_html=True)

        st.markdown('<div class="sv-section">📋 Mock Logs</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="mock-log">{sc["mock_log"]}</div>',unsafe_allow_html=True)

        done_cnt=len(st.session_state.tasks_done); tot_t=len(sc["tasks"])
        pct=int(done_cnt/tot_t*100) if tot_t else 0
        st.markdown(f'<div class="sv-section">✅ Tasks ({done_cnt}/{tot_t} — {pct}%)</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="prog-wrap"><div class="prog-bar" style="width:{pct}%"></div></div>',unsafe_allow_html=True)
        for i,task in enumerate(sc["tasks"]):
            done=i in st.session_state.tasks_done
            cls="task-done" if done else ""
            lbl="✅" if done else f'<span class="task-num">{i+1}.</span>'
            st.markdown(f'<div class="task-row {cls}">{lbl} {task}</div>',unsafe_allow_html=True)
            if not done:
                if st.button(f"✓ Done {i+1}",key=f"td_{i}"):
                    st.session_state.tasks_done.add(i); st.session_state.total_score+=10
                    if len(st.session_state.tasks_done)>=tot_t:
                        st.session_state.scenarios_completed+=1; st.session_state.total_score+=50
                    st.rerun()

        st.markdown('<div class="sv-section">🎯 Expected Outcome</div>',unsafe_allow_html=True)
        st.markdown(f'<div style="background:#0a2a18;border:1px solid #1a5a30;border-radius:4px;padding:7px 12px;font-size:11px;color:#5dc888;">{sc["expected_outcome"]}</div>',unsafe_allow_html=True)
        st.markdown('<div class="sv-section">🔑 Key Commands</div>',unsafe_allow_html=True)
        for cmd in sc["key_commands"]:
            st.markdown(f'<div style="background:#020810;border:1px solid #1a3a5a;border-radius:3px;padding:3px 9px;font-size:10px;color:#5da8e8;font-family:JetBrains Mono,monospace;margin-bottom:2px;">{cmd}</div>',unsafe_allow_html=True)

    with col_chat:
        mc={"guided":"#5da8e8","freeplay":"#5dc888","quiz":"#e87a5a"}.get(st.session_state.chat_mode,"#8aadcc")
        st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;padding:5px 0 8px;flex-wrap:wrap">
<span style="font-size:13px;color:#d0e8f8;font-weight:600">{sc['icon']} {sc['title']}</span>
<span style="font-size:10px;padding:2px 8px;border-radius:3px;background:#0d1e35;color:{mc};border:1px solid {mc}44;font-family:'JetBrains Mono',monospace">{st.session_state.chat_mode.upper()}</span>
<span class="pill" style="font-size:10px">Score: <b>{st.session_state.total_score}</b></span>
<span class="pill" style="font-size:10px">Correct: <b>{st.session_state.correct_answers}</b></span>
</div>""",unsafe_allow_html=True)

        if not st.session_state.messages:
            st.markdown('<div class="chat-sys">Scenario loaded. AI briefing in progress…</div>',unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                if msg["role"]=="user" and not msg["content"].startswith("[SCENARIO"):
                    st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>',unsafe_allow_html=True)
                elif msg["role"]=="assistant":
                    st.markdown(f'<div class="chat-bot">{msg["content"]}</div>',unsafe_allow_html=True)

        st.markdown("---")
        qa=st.columns(6)
        actions=[
            ("▶ Next Task","Guide me through the next pending task step-by-step with exact commands and expected Exadata output."),
            ("💡 Hint","Give me a targeted hint for the current task — point me in the right direction without revealing the full answer."),
            ("🔍 Diagnose","Walk me through diagnosing this issue step-by-step using the symptoms and logs provided."),
            ("📜 Show Cmd","Show me the exact command(s) for the current task with realistic Exadata output."),
            ("? Quiz","Ask me 3 MCQ questions about this scenario and score my answers as CORRECT ✓ or WRONG ✗."),
            ("📋 RCA","Help me write a structured RCA report: timeline, root cause, impact, fix, prevention."),
        ]
        for i,(lbl,pmt) in enumerate(actions):
            with qa[i]:
                if st.button(lbl,use_container_width=True,key=f"qa_{i}"):
                    call_api(pmt,sc); st.rerun()

        sym_map={
            "b_space":"SQL>","b_user":"SQL>","b_awr":"SQL>","b_rman":"RMAN>","b_dg_check":"DGMGRL>",
            "s_db_crash":"$","s_asm_fail":"CellCLI>","s_smart_scan":"SQL>","s_cell_down":"$",
            "s_rman_fail":"RMAN>","s_rac_evict":"$","s_patch":"$","s_switchover":"DGMGRL>",
            "a_p1_major":"$","a_perf_war":"$","a_upgrade":"$","a_rca":"SQL>","a_tde":"SQL>",
            "a_hcc_compress":"SQL>","a_ansible":"$","a_iorm_adv":"CellCLI>",
        }
        sym=sym_map.get(st.session_state.current_scenario,"$")
        st.markdown(f'<div class="term-hdr">⬡ Practice Terminal &nbsp;|&nbsp; <b style="color:#5dc888">{sym}</b> &nbsp;|&nbsp; <span style="color:#4a7ab5;font-size:10px">Type command → Run ▶ for AI evaluation</span></div>',unsafe_allow_html=True)
        t1,t2=st.columns([5,1])
        with t1:
            cmd=st.text_input("t",key="tc",placeholder=f"{sym} type command…",label_visibility="collapsed")
        with t2:
            rb=st.button("▶ Run",type="primary",use_container_width=True)
        if rb and cmd:
            st.markdown(f'<div class="term-hdr">{sym} {cmd}</div>',unsafe_allow_html=True)
            pending=[t for i,t in enumerate(sc["tasks"]) if i not in st.session_state.tasks_done]
            ep=(f"[PRACTICE TERMINAL] Ran: `{cmd}`\n"
                f"Current task: {pending[0] if pending else 'All tasks done'}\n\n"
                f"Evaluate in 100-150 words: correct for this task? Show Exadata output. "
                f"CORRECT ✓ (+10 pts) or WRONG ✗ with the right command.")
            call_api(ep,sc,show_user=False); st.rerun()

        uq=st.chat_input("Type your answer, command, question, or quiz response…")
        if uq: call_api(uq,sc); st.rerun()

# ── LAB CATALOG ─────────────────────────────────────────────────────────────
LAB_CATALOG = {
  "L1": {"label":"L1 – Basic Operations","color":"#5da8e8","icon":"🔵","groups":{
    "Database & PDB":[
      {"id":1,"title":"Create CDB with 2 PDBs","obj":"Create CDB + 2 PDBs, verify services","scenario":"New application onboarding needs isolated DEV and PROD PDBs","tasks":["Create CDB using DBCA or SQL","Create PDB1 and PDB2 with admin users","Open PDBs and verify via lsnrctl"],"validation":"Both PDBs accessible via service name","tag":"demo"},
      {"id":2,"title":"Open and Close PDBs","obj":"Manage PDB lifecycle states","scenario":"Scheduled maintenance requires controlled PDB shutdown","tasks":["Check PDB status with V$PDBS","Close PDB gracefully","Open PDB READ WRITE and READ ONLY"],"validation":"PDB transitions confirmed in V$PDBS","tag":"lab"},
      {"id":3,"title":"Clone PDB Locally","obj":"Clone an existing PDB within same CDB","scenario":"QA team needs copy of DEV PDB for testing","tasks":["Put source PDB in READ ONLY","CREATE PLUGGABLE DATABASE ... FROM","Open cloned PDB and verify data"],"validation":"Cloned PDB accessible with source data","tag":"lab"},
      {"id":4,"title":"Drop PDB Safely","obj":"Remove a PDB including datafiles","scenario":"Decommission expired test PDB","tasks":["Close the PDB","DROP PLUGGABLE DATABASE ... INCLUDING DATAFILES","Verify removal from V$PDBS and filesystem"],"validation":"PDB and all datafiles removed","tag":"lab"},
      {"id":5,"title":"Rename PDB","obj":"Rename a PDB without data loss","scenario":"PDB naming convention change required","tasks":["Close PDB","ALTER PLUGGABLE DATABASE RENAME GLOBAL_NAME","Open and verify new service name"],"validation":"PDB accessible with new name","tag":"lab"},
      {"id":6,"title":"Configure Default Tablespace","obj":"Set default and temp tablespaces for a PDB","scenario":"Ensure new users get correct storage allocation","tasks":["Create USERS and TEMP tablespaces","ALTER DATABASE DEFAULT TABLESPACE","Verify with DBA_TABLESPACES"],"validation":"New user inherits correct tablespaces","tag":"lab"},
    ],
    "User & Security":[
      {"id":7,"title":"Create User with Roles","obj":"Create DB user and assign roles","scenario":"New developer needs DB access","tasks":["CREATE USER with profile","GRANT CONNECT, RESOURCE","GRANT QUOTA on DATA tablespace"],"validation":"User can connect and create objects","tag":"lab"},
      {"id":8,"title":"Grant and Revoke Privileges","obj":"Manage object and system privileges","scenario":"Application user needs SELECT on specific tables only","tasks":["GRANT SELECT on schema tables","Grant CREATE SESSION","Revoke privilege and verify denial"],"validation":"Privilege changes effective immediately","tag":"lab"},
      {"id":9,"title":"Enable Unified Auditing","obj":"Enable and configure unified audit policy","scenario":"Compliance requires DML audit on sensitive tables","tasks":["CREATE AUDIT POLICY for DML","AUDIT POLICY enable","Verify in UNIFIED_AUDIT_TRAIL"],"validation":"Audit records created for DML operations","tag":"lab"},
      {"id":10,"title":"Create Password Profile","obj":"Enforce password complexity and expiry","scenario":"Security hardening: 90-day password expiry with lockout","tasks":["CREATE PROFILE with PASSWORD_LIFE_TIME=90","Set FAILED_LOGIN_ATTEMPTS=5","Assign profile to users"],"validation":"Password enforcement confirmed by testing","tag":"lab"},
      {"id":11,"title":"Lock and Unlock Users","obj":"Control user account status","scenario":"Offboarding employee - lock DB account immediately","tasks":["ALTER USER ... ACCOUNT LOCK","Verify connection denied","ALTER USER ... ACCOUNT UNLOCK"],"validation":"Lock/unlock transitions verified","tag":"lab"},
    ],
    "Storage Basics":[
      {"id":12,"title":"Create Tablespace in +DATA","obj":"Create ASM-backed tablespace","scenario":"New application needs dedicated tablespace on Exadata","tasks":["CREATE TABLESPACE using +DATA diskgroup","Set EXTENT MANAGEMENT LOCAL","Verify in DBA_TABLESPACES"],"validation":"Tablespace visible and usable","tag":"lab"},
      {"id":13,"title":"Add Datafile to Tablespace","obj":"Extend tablespace by adding datafile","scenario":"Tablespace usage at 85% - add capacity","tasks":["Check usage with DBA_FREE_SPACE","ALTER TABLESPACE ADD DATAFILE on +DATA","Verify in DBA_DATA_FILES"],"validation":"Tablespace free space increased","tag":"lab"},
      {"id":14,"title":"Resize Tablespace Datafile","obj":"Manually resize existing datafile","scenario":"Over-provisioned datafile needs rightsizing","tasks":["Check HWM with dbms_space","ALTER DATABASE DATAFILE RESIZE","Verify new size"],"validation":"Datafile resized without errors","tag":"lab"},
      {"id":15,"title":"Enable Autoextend","obj":"Enable automatic extension on datafiles","scenario":"Prevent ORA-01654 by enabling autoextend","tasks":["ALTER DATABASE DATAFILE ... AUTOEXTEND ON NEXT 512M MAXSIZE 32G","Verify AUTOEXTENSIBLE=YES in DBA_DATA_FILES"],"validation":"Tablespace auto-extends on load","tag":"lab"},
      {"id":16,"title":"Check Tablespace Usage","obj":"Query tablespace utilization and identify risk","scenario":"Proactive capacity check before month-end batch","tasks":["Query DBA_TABLESPACE_USAGE_METRICS","Identify tablespaces over 80%","Generate space report"],"validation":"Usage report with threshold alerts","tag":"lab"},
    ],
    "Backup Basics":[
      {"id":17,"title":"Full RMAN Backup","obj":"Perform full database backup using RMAN","scenario":"Baseline backup before major change","tasks":["Configure RMAN channel on +RECO","BACKUP DATABASE PLUS ARCHIVELOG","Verify with LIST BACKUP SUMMARY"],"validation":"Backup completes with status AVAILABLE","tag":"lab"},
      {"id":18,"title":"Incremental RMAN Backup","obj":"Configure and run level 0 + level 1 incremental","scenario":"Reduce daily backup window using incremental strategy","tasks":["BACKUP INCREMENTAL LEVEL 0 DATABASE","Run LEVEL 1 next day","LIST BACKUP to verify chain"],"validation":"Incremental chain complete and recoverable","tag":"lab"},
      {"id":19,"title":"Validate RMAN Backup","obj":"Validate backup integrity without restoring","scenario":"DR test - confirm backup is valid","tasks":["RESTORE DATABASE VALIDATE","VALIDATE BACKUPSET all","Check V$BACKUP_VALIDATION"],"validation":"Zero corrupt blocks found","tag":"lab"},
      {"id":20,"title":"List and Cross-Check Backups","obj":"Manage RMAN backup catalog","scenario":"Identify expired and obsolete backups","tasks":["LIST BACKUP SUMMARY","CROSSCHECK BACKUP","DELETE EXPIRED BACKUP"],"validation":"Catalog synchronized with physical files","tag":"lab"},
    ],
    "Monitoring":[
      {"id":21,"title":"Generate AWR Report","obj":"Generate and interpret AWR HTML report","scenario":"Performance complaint during peak hours","tasks":["Identify snapshot IDs in DBA_HIST_SNAPSHOT","Run awrrpt.sql","Identify Top 5 Wait Events"],"validation":"AWR report generated, bottleneck identified","tag":"lab"},
      {"id":22,"title":"Generate ASH Report","obj":"Use ASH for real-time and historical analysis","scenario":"5-minute spike in waits needs investigation","tasks":["Run awrashrpt.sql for spike window","Identify blocking sessions","Find hot object from ASH data"],"validation":"Root cause identified from ASH","tag":"lab"},
      {"id":23,"title":"Check Alert Log","obj":"Monitor alert log for ORA- errors","scenario":"Application reports intermittent errors","tasks":["Locate alert log via V$DIAG_INFO","Use adrci to query recent errors","Filter ORA-600 and ORA-7445"],"validation":"All recent errors documented and triaged","tag":"lab"},
      {"id":24,"title":"Setup Tablespace Alert","obj":"Configure automated tablespace threshold alerts","scenario":"Automate alerts before tablespace hits 90%","tasks":["Create monitoring view for usage","Set warning 80%, critical 90%","Test alert by filling tablespace"],"validation":"Alert triggers correctly at threshold","tag":"lab"},
      {"id":25,"title":"Monitor Active Sessions","obj":"Monitor current sessions and identify blocking","scenario":"Application hung - identify blocking chain","tasks":["Query V$SESSION for blocking sessions","Find lock chain with DBA_BLOCKERS","Kill blocking session if approved"],"validation":"Blocking chain identified and resolved","tag":"lab"},
    ],
  }},
  "L2": {"label":"L2 – Intermediate Operations","color":"#5dc888","icon":"🟢","groups":{
    "ASM & Storage":[
      {"id":26,"title":"Create Diskgroup NORMAL Redundancy","obj":"Create new ASM diskgroup using Exadata grid disks","scenario":"New application needs dedicated storage isolation","tasks":["LIST GRIDDISK available on all cells via DCLI","CREATE DISKGROUP with NORMAL REDUNDANCY","Verify in V$ASM_DISKGROUP"],"validation":"Diskgroup online, 3 failure groups confirmed","tag":"lab"},
      {"id":27,"title":"Add Disk to Diskgroup","obj":"Expand diskgroup by adding new grid disks","scenario":"DATA diskgroup at 70% - add capacity from new cell disks","tasks":["Create grid disks via CellCLI","ALTER DISKGROUP DATA ADD DISK","Monitor V$ASM_OPERATION for rebalance"],"validation":"Rebalance completes, free space increased","tag":"lab"},
      {"id":28,"title":"Drop Disk Safely from Diskgroup","obj":"Remove disk from ASM without data loss","scenario":"Replace aging disk from diskgroup","tasks":["ALTER DISKGROUP DROP DISK with WAIT","Monitor rebalance progress","Verify disk removed from V$ASM_DISK"],"validation":"Disk removed, data migrated, no errors","tag":"lab"},
      {"id":29,"title":"Monitor and Control Rebalance","obj":"Monitor ASM rebalance and adjust power","scenario":"Rebalance too slow before maintenance window closes","tasks":["Query V$ASM_OPERATION for status","ALTER DISKGROUP REBALANCE POWER 11","Verify ETA and completion"],"validation":"Rebalance completes within window","tag":"lab"},
      {"id":30,"title":"Fix Diskgroup Imbalance","obj":"Detect and fix uneven disk distribution","scenario":"Some cells have much more free space than others","tasks":["Query V$ASM_DISK for per-disk usage","ALTER DISKGROUP REBALANCE to redistribute","Verify even distribution afterward"],"validation":"Disk usage within 5% across all cells","tag":"lab"},
    ],
    "RAC Administration":[
      {"id":31,"title":"Add a RAC Node","obj":"Extend cluster by adding new compute node","scenario":"Capacity expansion: add node 3 to 2-node RAC","tasks":["Run addNode.sh on new node","cluvfy check prerequisites","srvctl add instance and start"],"validation":"New node ONLINE in crsctl","tag":"demo"},
      {"id":32,"title":"Remove a RAC Node","obj":"Cleanly decommission a cluster node","scenario":"Node 3 decommissioned after capacity downsize","tasks":["Relocate services away from node","srvctl stop instance","Run deleteNode.sh and verify"],"validation":"Node removed, remaining nodes healthy","tag":"demo"},
      {"id":33,"title":"Check Full Cluster Status","obj":"Assess complete cluster health using CRS tools","scenario":"Post-maintenance health check before business hours","tasks":["crsctl check cluster -all","olsnodes -s","srvctl status database -d ORCL"],"validation":"All resources ONLINE, no warnings","tag":"lab"},
      {"id":34,"title":"Restart CRS Stack","obj":"Perform controlled CRS restart on one node","scenario":"CRS resources stuck - rolling restart required","tasks":["crsctl stop crs","crsctl start crs","crsctl check crs and verify resources"],"validation":"CRS restarts cleanly, all resources online","tag":"lab"},
      {"id":35,"title":"Diagnose Node Eviction","obj":"Root cause a node eviction from cluster diagnostics","scenario":"Node 2 was evicted at 3am - find root cause","tasks":["Examine ocssd.log and css trace files","Check network and IB link stats at eviction time","Review misscount and disktimeout settings"],"validation":"Root cause identified: network or disk timeout","tag":"lab"},
    ],
    "Backup & Recovery":[
      {"id":36,"title":"Restore Full Database","obj":"Full database restore and recovery from RMAN","scenario":"DB unrecoverable due to storage corruption","tasks":["Startup MOUNT","RESTORE DATABASE from RMAN backup","RECOVER DATABASE and OPEN RESETLOGS"],"validation":"Database open READ WRITE, data consistent","tag":"demo"},
      {"id":37,"title":"Point-in-Time Recovery","obj":"Recover database to specific SCN or timestamp","scenario":"Accidental DELETE of critical table at 14:30","tasks":["STARTUP MOUNT","SET UNTIL TIME / SCN","RESTORE + RECOVER + OPEN RESETLOGS"],"validation":"Data restored to correct point","tag":"lab"},
      {"id":38,"title":"Recover Dropped Table (TSPITR)","obj":"Use Tablespace Point-in-Time Recovery","scenario":"Entire USERS tablespace dropped with wrong data","tasks":["RECOVER TABLESPACE users UNTIL TIME","Plug recovered tablespace back","Export/import specific table if needed"],"validation":"Original table data recovered","tag":"lab"},
      {"id":39,"title":"Restore Controlfile from Backup","obj":"Recover from lost/corrupted controlfile","scenario":"All controlfile copies lost","tasks":["STARTUP NOMOUNT","RESTORE CONTROLFILE FROM AUTOBACKUP","MOUNT and RECOVER DATABASE"],"validation":"Database mounts and opens after recovery","tag":"lab"},
      {"id":40,"title":"Recover from Missing Archive Logs","obj":"Handle incomplete recovery scenario","scenario":"Some archivelogs missing from backup","tasks":["LIST ARCHIVELOG check for gaps","RECOVER DATABASE UNTIL CANCEL","Evaluate data loss and document"],"validation":"Database recovers as far as possible, gap documented","tag":"lab"},
    ],
    "Data Guard":[
      {"id":41,"title":"Setup Physical Standby","obj":"Configure Data Guard physical standby from scratch","scenario":"New DR requirement: set up standby in secondary site","tasks":["Enable ARCHIVELOG and FORCE LOGGING on primary","Duplicate for standby with RMAN active duplicate","Configure LOG_ARCHIVE_DEST_2 and verify MRP"],"validation":"Standby applying redo, lag < 30 seconds","tag":"demo"},
      {"id":42,"title":"Check Standby Lag","obj":"Monitor and measure Data Guard apply lag","scenario":"DR health check: verify RPO within 5 minutes","tasks":["Query V$DATAGUARD_STATS","Check V$MANAGED_STANDBY for MRP status","Use DGMGRL SHOW DATABASE VERBOSE"],"validation":"Lag confirmed within acceptable RPO","tag":"lab"},
      {"id":43,"title":"Planned Switchover","obj":"Perform zero-downtime planned role reversal","scenario":"Planned maintenance: swap primary and standby roles","tasks":["Validate with DGMGRL VALIDATE DATABASE","DGMGRL SWITCHOVER TO standby","Verify new primary is OPEN READ WRITE"],"validation":"Switchover complete, both sides healthy","tag":"lab"},
      {"id":44,"title":"Emergency Failover","obj":"Perform failover when primary is unreachable","scenario":"Primary site down - activate standby","tasks":["Confirm primary is truly down","DGMGRL FAILOVER TO standby","Redirect application connections"],"validation":"Standby becomes primary, application reconnected","tag":"lab"},
      {"id":45,"title":"Rebuild Failed Standby","obj":"Re-create standby that has diverged","scenario":"Standby gap too large - rebuild from scratch","tasks":["Cancel MRP on standby","Re-duplicate from primary using RMAN","Re-enable and verify sync"],"validation":"New standby in sync, gap zero","tag":"lab"},
    ],
    "Performance Basics":[
      {"id":46,"title":"Identify Top SQL","obj":"Find top resource-consuming SQL statements","scenario":"High CPU alert - identify culprit queries","tasks":["Query V$SQL ordered by ELAPSED_TIME","Use AWR Top SQL section","Check ASH for concurrent SQL waits"],"validation":"Top 5 SQL with execution plans identified","tag":"lab"},
      {"id":47,"title":"Create SQL Profile","obj":"Apply SQL profile to fix bad execution plan","scenario":"Query changed plan after stats update","tasks":["Run SQL Tuning Advisor via DBMS_SQLTUNE","Review recommendation","Accept and apply SQL profile"],"validation":"SQL uses new plan, performance improved","tag":"lab"},
      {"id":48,"title":"Add Index to Improve Query","obj":"Create index to eliminate full table scan","scenario":"Report query doing FTS on 500M row table","tasks":["EXPLAIN PLAN to confirm FTS","CREATE INDEX on filter columns","Verify index used in new plan"],"validation":"Query elapsed time reduced by 90%+","tag":"lab"},
      {"id":49,"title":"Fix Unintentional Full Table Scan","obj":"Force index use or rewrite query to avoid FTS","scenario":"Query ignoring index due to implicit conversion","tasks":["Identify FTS in AWR or V$SQL","Find implicit conversion in predicate","Fix query or add function-based index"],"validation":"FTS eliminated, execution plan optimal","tag":"lab"},
      {"id":50,"title":"Tune Slow Query End-to-End","obj":"Full query tuning cycle: diagnose, plan, fix, verify","scenario":"SLA breach: monthly report 4 hours, needs < 30 min","tasks":["Capture baseline plan with DBMS_XPLAN","Identify bottleneck: join order, FTS, sort","Apply fix: stats, hints, index, rewrite"],"validation":"Query meets SLA < 30 minutes","tag":"lab"},
    ],
    "Exadata Basics":[
      {"id":51,"title":"Check Smart Scan Usage","obj":"Verify Smart Scan is active and measure offload","scenario":"Confirm Exadata offload working for batch queries","tasks":["Query V$SYSSTAT for cell interconnect bytes","Run FTS query and check V$SQL for cell offload","Verify TABLE ACCESS STORAGE FULL in plan"],"validation":"Smart Scan confirmed, offload > 80%","tag":"lab"},
      {"id":52,"title":"Enable and Size Flash Cache","obj":"Configure Exadata Smart Flash Cache","scenario":"High read latency - leverage NVMe flash cache","tasks":["CellCLI> LIST FLASHCACHE DETAIL","DROP and CREATE FLASHCACHE ALL","Monitor hit ratio via V$SYSSTAT"],"validation":"Flash cache hit ratio > 80%","tag":"lab"},
      {"id":53,"title":"Verify Storage Offload Efficiency","obj":"Measure storage cell offload percentage","scenario":"Validate Exadata ROI for new workload","tasks":["Run representative batch query","Compare V$SYSSTAT interconnect vs IO bytes","Calculate offload % = (1 - interconnect/total)*100"],"validation":"Offload efficiency > 70% documented","tag":"lab"},
      {"id":54,"title":"Check Cell Metrics","obj":"Monitor storage cell performance metrics","scenario":"Proactive health check - review all cell metrics","tasks":["DCLI cellcli -e LIST METRICCURRENT WHERE objectType=CELLDISK","Check CD_IO_RQ_R_LG, CD_IO_RQ_W metrics","LIST ALERTHISTORY on all cells"],"validation":"No critical metrics, all cells healthy","tag":"lab"},
      {"id":55,"title":"CellCLI Basic Administration","obj":"Master fundamental CellCLI commands","scenario":"First-time cell administration","tasks":["LIST CELL DETAIL - hardware info","LIST CELLDISK / LIST GRIDDISK","LIST PHYSICALDISK WHERE status != normal"],"validation":"All cell components listed and healthy","tag":"lab"},
    ],
  }},
  "L3": {"label":"L3 – Advanced Operations","color":"#f39c12","icon":"🟡","groups":{
    "Exadata Deep Dive":[
      {"id":56,"title":"Configure IORM Plans","obj":"Set up I/O Resource Manager to prioritize workloads","scenario":"OLTP and batch competing for I/O - enforce priority","tasks":["CellCLI> LIST IORMPLAN DETAIL","ALTER IORMPLAN active=true with OLTP share=8, BATCH share=2","Monitor V$CELL_IOREASON for throttling"],"validation":"OLTP latency maintained during batch run","tag":"lab"},
      {"id":57,"title":"Optimize Flash Cache Strategy","obj":"Tune flash cache for specific workload patterns","scenario":"Mixed OLTP/DW - optimize flash cache usage","tasks":["Analyze flash cache hit ratio by object","Set CELL_FLASH_CACHE for critical objects","Monitor improvement in V$SYSSTAT"],"validation":"Critical object hit ratio > 95%","tag":"lab"},
      {"id":58,"title":"Analyze Storage Index Usage","obj":"Understand and leverage Exadata Storage Indexes","scenario":"Improve range scan queries using storage indexes","tasks":["Enable cell_offload_processing","Run range scan queries and check SI eliminates I/O","Verify via V$SYSSTAT cell index scans"],"validation":"Storage index eliminating > 50% of I/O","tag":"lab"},
      {"id":59,"title":"Diagnose Smart Scan Not Firing","obj":"Troubleshoot why Smart Scan is disabled for a query","scenario":"Large Exadata table query not using Smart Scan","tasks":["Check cell_offload_processing parameter","Verify no rowid access or small table threshold","Check for object encryption or compression issues"],"validation":"Root cause found, Smart Scan enabled","tag":"lab"},
      {"id":60,"title":"Tune Cell Disk I/O","obj":"Identify and resolve storage-level I/O bottlenecks","scenario":"High disk I/O latency reported on specific cells","tasks":["DCLI cellcli -e LIST METRICCURRENT WHERE name=CD_IO_RQMN_RD_LARGE","Identify hot disks and diskgroups","Rebalance or quarantine problematic disk"],"validation":"I/O latency returned to baseline < 2ms","tag":"lab"},
    ],
    "Performance Tuning":[
      {"id":61,"title":"Full AWR Bottleneck Analysis","obj":"Use AWR to identify and resolve system-wide bottleneck","scenario":"Peak hours: DB response slow - comprehensive AWR analysis","tasks":["Compare busy vs normal AWR snapshots","Identify top wait events and SQL","Correlate OS metrics: CPU, memory, I/O"],"validation":"Bottleneck identified and remediation documented","tag":"lab"},
      {"id":62,"title":"Fix Latch Contention","obj":"Diagnose and resolve latch wait events","scenario":"High latch: cache buffers chains wait in AWR","tasks":["Query V$LATCH and V$LATCH_CHILDREN for hot latches","Identify hot blocks via X$BH","Apply fix: segment shrink or storage change"],"validation":"Latch waits reduced by > 80%","tag":"lab"},
      {"id":63,"title":"Resolve High CPU SQL","obj":"Find and tune SQL consuming excessive CPU","scenario":"CPU at 95% - single SQL running thousands of times","tasks":["V$SQL ordered by CPU_TIME","Check parse counts and bind variables","Fix: cursor sharing, bind variables, SQL rewrite"],"validation":"CPU drops to normal baseline","tag":"lab"},
      {"id":64,"title":"Tune Parallel Queries on Exadata","obj":"Optimize parallel execution with Exadata offload","scenario":"Parallel DW query not scaling - analyze efficiency","tasks":["Check DOP and skew in V$PQ_SLAVE","Verify Smart Scan with parallel via V$SYSSTAT","Tune PARALLEL_DEGREE_POLICY and statement queuing"],"validation":"Linear scaling with DOP, no skew","tag":"lab"},
      {"id":65,"title":"Fix Temp Space Exhaustion","obj":"Resolve ORA-01652 and prevent recurrence","scenario":"Large sort/hash join exhausting TEMP tablespace","tasks":["Check V$SORT_USAGE for current consumers","Add tempfile to TEMP tablespace","Tune PGA_AGGREGATE_TARGET to reduce sort spills"],"validation":"TEMP usage normalized, ORA-01652 eliminated","tag":"lab"},
    ],
    "High Availability":[
      {"id":66,"title":"Handle Node Eviction Scenario","obj":"Respond to and recover from involuntary node eviction","scenario":"Node 1 evicted from cluster during peak hours","tasks":["Verify eviction in ocssd.log","Restart CRS and re-join cluster","Root cause: check network, voting disk, I/O timeout"],"validation":"Node rejoins, services auto-start, RCA documented","tag":"lab"},
      {"id":67,"title":"Recover ASM Disk Failure","obj":"Handle failed/offline ASM disk and restore redundancy","scenario":"One HDD shows ERROR in V$ASM_DISK","tasks":["Identify failed disk: V$ASM_DISK WHERE state=ERROR","Determine if recoverable or needs replacement","Replace disk, create celldisk/griddisk, add to DG"],"validation":"ASM DG back to NORMAL redundancy","tag":"lab"},
      {"id":68,"title":"Optimize Rebalance Performance","obj":"Control rebalance speed to minimize impact","scenario":"Rebalance after disk add impacting OLTP performance","tasks":["Monitor with V$ASM_OPERATION","Set REBALANCE POWER based on I/O headroom","Use MODIFY DISKGROUP REBALANCE THROTTLE"],"validation":"Rebalance completes with < 10% OLTP impact","tag":"lab"},
      {"id":69,"title":"Cluster Interconnect Tuning","obj":"Diagnose and tune RAC interconnect on Exadata IB","scenario":"High gc buffer busy waits - interconnect suspected","tasks":["Check IB link stats: ibstat, ifconfig","Query GV$SYSSTAT for gc cr blocks received","Verify InfiniBand configuration with oifcfg"],"validation":"GC waits reduced, interconnect at line rate","tag":"lab"},
      {"id":70,"title":"Test Failover End-to-End","obj":"Simulate and validate complete HA failover","scenario":"Annual DR test: verify RTO < 30 minutes","tasks":["Simulate primary node failure","Verify TAF/FCF reconnects applications","Measure RTO from failure to reconnect"],"validation":"RTO achieved within target, no data loss","tag":"lab"},
    ],
    "Patching & Upgrade":[
      {"id":71,"title":"Apply DB Release Update","obj":"Apply quarterly Release Update to Oracle DB","scenario":"Critical bug fix requires RU 19.22 application","tasks":["Run opatch prereq CheckMinimumComputerRequirements","opatchauto apply RU patch on GI and DB","Validate: opatch lspatches and run utlrp.sql"],"validation":"New RU active, no invalid objects","tag":"demo"},
      {"id":72,"title":"Patch Grid Infrastructure Rolling","obj":"Apply GI patch without cluster downtime","scenario":"Monthly patch cycle: GI patch required","tasks":["opatchauto apply with -rolling flag on node 1","Verify node 1 patched, services moved back","Repeat on node 2"],"validation":"All nodes on same GI version, cluster healthy","tag":"lab"},
      {"id":73,"title":"Patch Exadata Cell Nodes","obj":"Apply storage server software patch","scenario":"Cell node patch for security CVE fix","tasks":["patchmgr prereq check on all cells","patchmgr -cells cellgroup -rolling patch","Verify cell version with cellcli LIST CELL"],"validation":"All cells updated, no storage interruption","tag":"lab"},
      {"id":74,"title":"Rollback a Failed Patch","obj":"Rollback GI or DB patch after failure","scenario":"RU patch caused ORA-600 - emergency rollback","tasks":["opatchauto rollback patch on affected node","Verify previous version restored","Test application connectivity"],"validation":"Previous version restored, application functional","tag":"lab"},
      {"id":75,"title":"Upgrade Database 19c to 23ai","obj":"Perform in-place database upgrade","scenario":"Planned upgrade to Oracle 23ai for new AI features","tasks":["Run preupgrade.jar and fix issues","Perform upgrade using dbupgrade or DBUA","Run postupgrade_fixups.sql and utlrp.sql"],"validation":"DB on 23ai, no invalid objects, apps verified","tag":"demo"},
    ],
    "Security Advanced":[
      {"id":76,"title":"Enable Transparent Data Encryption","obj":"Encrypt tablespaces using TDE","scenario":"Compliance: encrypt PII tablespace at rest","tasks":["Configure software keystore","ADMINISTER KEY MANAGEMENT CREATE KEYSTORE","ALTER TABLESPACE ENCRYPT USING AES256"],"validation":"Tablespace encrypted, performance within 5% overhead","tag":"lab"},
      {"id":77,"title":"Rotate TDE Wallet Keys","obj":"Perform TDE master key rotation without downtime","scenario":"Annual key rotation policy compliance","tasks":["ADMINISTER KEY MANAGEMENT CREATE NEW MASTER ENCRYPTION KEY","Verify old keys backed up","Confirm encryption still active after rotation"],"validation":"New key active, all tablespaces accessible","tag":"lab"},
      {"id":78,"title":"Audit Critical Operations","obj":"Implement fine-grained audit for privileged operations","scenario":"Audit all DDL and privileged DML on FINANCE schema","tasks":["CREATE AUDIT POLICY for DDL on FINANCE","Enable audit for SYS operations","Query UNIFIED_AUDIT_TRAIL for violations"],"validation":"All critical operations captured in audit trail","tag":"lab"},
      {"id":79,"title":"Mask Sensitive Data","obj":"Apply Oracle Data Masking for non-production environments","scenario":"GDPR: mask PII before copying prod to dev","tasks":["Define masking definitions for PII columns","Apply masking using DBMS_REDACT","Verify masked values in dev copy"],"validation":"No real PII visible in masked environment","tag":"lab"},
      {"id":80,"title":"Implement Least Privilege","obj":"Audit and reduce excessive user privileges","scenario":"Security audit found users with DBA role who dont need it","tasks":["Query DBA_SYS_PRIVS and DBA_ROLE_PRIVS","Identify and document over-privileged accounts","REVOKE unnecessary privileges and test"],"validation":"All accounts follow least privilege principle","tag":"lab"},
    ],
    "Automation":[
      {"id":81,"title":"Write DB Health Check Script","obj":"Build comprehensive shell+SQL health check","scenario":"Automate daily health check to replace manual checks","tasks":["Script: cluster status, DG health, backup status","Add Exadata cell checks via DCLI","Output HTML or text report with RAG status"],"validation":"Script runs end-to-end, covers all key checks","tag":"lab"},
      {"id":82,"title":"Automate RMAN Backup","obj":"Create scheduled RMAN backup with error handling","scenario":"Replace manual RMAN with automated daily backup","tasks":["Write RMAN backup script with channels and retention","Add cron/scheduler job","Implement email alert on failure"],"validation":"Backup runs daily, alert fires on failure","tag":"lab"},
      {"id":83,"title":"Use Ansible for DB Tasks","obj":"Automate routine DBA tasks with Ansible playbooks","scenario":"Config drift on 10-node RAC - standardize with Ansible","tasks":["Write playbook for OS parameter tuning","Playbook for sqlnet.ora and listener management","Run against all nodes idempotently"],"validation":"Playbook runs idempotently, config standardized","tag":"demo"},
      {"id":84,"title":"Schedule DBMS_SCHEDULER Jobs","obj":"Create and manage Oracle Scheduler jobs","scenario":"Automate stats gathering and space reporting","tasks":["CREATE SCHEDULE and PROGRAM objects","CREATE JOB linking program to schedule","Monitor with DBA_SCHEDULER_JOB_RUN_DETAILS"],"validation":"Jobs run on schedule, results logged","tag":"lab"},
      {"id":85,"title":"Automate Alerting","obj":"Build proactive alert system for key DB metrics","scenario":"Catch issues before users notice - automated alerts","tasks":["Script to check tablespace, ASM, DG lag, backup","Email alert on threshold breach","Test with simulated threshold breach"],"validation":"Alerts fire within 5 minutes of threshold breach","tag":"lab"},
    ],
  }},
  "L4": {"label":"L4 – Expert / Real-World Scenarios","color":"#e74c3c","icon":"🔴","groups":{
    "Incident Response":[
      {"id":86,"title":"DB Crash: Diagnose ORA-00600","obj":"Investigate and resolve internal Oracle error ORA-00600","scenario":"Production DB crashed with ORA-00600 [kcbgcur_1] at 2am","tasks":["Analyze alert log and trace file for ORA-600 args","Search MOS for matching bug ID","Apply workaround or patch, document RCA"],"validation":"DB stable, RCA documented, SR raised if needed","tag":"lab"},
      {"id":87,"title":"ASM Diskgroup Unexpectedly Dismounted","obj":"Recover dismounted ASM diskgroup","scenario":"DATA diskgroup dismounted during business hours - apps failing","tasks":["Check V$ASM_DISKGROUP for status and errors","Identify failed disks causing dismount","ALTER DISKGROUP DATA MOUNT FORCE and recover"],"validation":"Diskgroup remounted, data consistent, apps reconnected","tag":"lab"},
      {"id":88,"title":"Cell Node Hardware Failure","obj":"Manage complete cell server failure","scenario":"CEL03 unresponsive - all disks offline in ASM","tasks":["Verify cell is truly down (ping, ILOM)","Monitor ASM drops cell disks - watch rebalance","Coordinate hardware replacement, rebuild cell, re-add disks"],"validation":"ASM redundancy restored after cell replacement","tag":"lab"},
      {"id":89,"title":"High I/O Latency Investigation","obj":"Diagnose and resolve sudden I/O latency spike","scenario":"cell single block physical read spiked to 50ms","tasks":["Check cell metrics: CD_IO_RQMN_RD_SM via DCLI","Identify slow cells or disks","Check for IB degradation or cell CPU saturation"],"validation":"Latency back to < 1ms, root cause identified","tag":"lab"},
      {"id":90,"title":"Backup Failure: Gap Recovery","obj":"Recover from backup failure leaving archive log gap","scenario":"Last 3 nights of RMAN backups failed silently","tasks":["LIST ARCHIVELOG to find gap","Verify archivelogs still on disk","Emergency backup of missing archivelogs immediately"],"validation":"Backup chain complete and recoverable","tag":"lab"},
    ],
    "Performance War Rooms":[
      {"id":91,"title":"Batch Job Slow: Smart Scan Not Firing","obj":"Diagnose and fix Smart Scan disabled for batch job","scenario":"Month-end batch running 5x slower - Smart Scan not used","tasks":["Verify cell_offload_processing=true in session","Check if table is direct-path read eligible","Verify no HCC corruption or encryption blocking offload"],"validation":"Smart Scan enabled, batch time reduced by 70%","tag":"lab"},
      {"id":92,"title":"Flash Cache Inefficiency","obj":"Diagnose poor flash cache hit ratio","scenario":"Flash cache hit ratio at 10% - should be > 80%","tasks":["Check object-level flash cache stats","Identify cache churn from large sequential scans","Pin critical objects via CELL_FLASH_CACHE"],"validation":"Hit ratio > 80% for OLTP objects","tag":"lab"},
      {"id":93,"title":"High GC Wait Events","obj":"Resolve Global Cache wait events in RAC","scenario":"gc cr multi block request waits at 30ms","tasks":["Query GV$SYSSTAT for GC block stats","Identify hot objects causing GC contention","Resequence or partition hot objects, review application"],"validation":"GC waits reduced to < 2ms","tag":"lab"},
      {"id":94,"title":"Memory Leak Diagnosis","obj":"Identify and resolve PGA or SGA memory leak","scenario":"SGA usage growing 500MB/day - OOM risk in 2 weeks","tasks":["Monitor V$SGA_DYNAMIC_COMPONENTS growth","Check V$PROCESS for runaway PGA consumers","Identify memory leak in custom Java or PL/SQL code"],"validation":"Memory growth stopped, leak identified and fixed","tag":"lab"},
      {"id":95,"title":"Parallel Query Imbalance","obj":"Fix skewed parallel execution across RAC nodes","scenario":"Parallel query using 32 slaves but only 2 nodes - severe skew","tasks":["Check V$PQ_SLAVE for slave distribution","Identify data skew causing slave imbalance","Fix: redistribute data, DISTRIBUTE hint, or partition"],"validation":"Parallel slaves evenly distributed, linear scaling","tag":"lab"},
    ],
    "Disaster Recovery":[
      {"id":96,"title":"Full DC Outage Simulation","obj":"Simulate complete datacenter loss and recovery procedure","scenario":"Primary DC unavailable - activate DR site","tasks":["Verify standby is in sync (last RTO check)","DGMGRL FAILOVER TO standby","Redirect DNS/load balancer to DR site, verify apps"],"validation":"DR site operational within RTO target","tag":"demo"},
      {"id":97,"title":"DR Failover and Full Validation","obj":"Validate DR environment fully functional post-failover","scenario":"Post-failover: validate every application and data integrity","tasks":["Run application smoke tests on DR","Verify data consistency: rowcount checks","Validate backup continues running on DR"],"validation":"DR environment 100% functional, no data loss","tag":"lab"},
      {"id":98,"title":"Re-sync Standby After Gap","obj":"Recover standby from large redo gap","scenario":"Standby network outage caused 6-hour gap","tasks":["Check gap: V$ARCHIVE_GAP","Ship missing archivelogs manually if needed","Restart MRP and verify gap closes"],"validation":"Standby in sync, apply lag < 30 seconds","tag":"lab"},
      {"id":99,"title":"Test RTO and RPO","obj":"Measure and document actual RTO/RPO in DR test","scenario":"Annual DR test: formally measure and document RTO/RPO","tasks":["Define failure injection method","Time from failure to detection, failover, app reconnect","Measure data loss window (RPO)"],"validation":"RTO and RPO documented and within SLA targets","tag":"lab"},
      {"id":100,"title":"Split Brain Scenario Resolution","obj":"Detect and resolve RAC split-brain condition","scenario":"Network partition causes both nodes to think they are primary","tasks":["Identify split brain from ocssd.log voting disk behavior","Determine which node survived via voting disk","Restart CRS on evicted node and re-join safely"],"validation":"Cluster healthy, no data divergence","tag":"lab"},
    ],
    "Architecture & Optimization":[
      {"id":101,"title":"Design OLTP Workload on Exadata","obj":"Architect Exadata configuration optimized for OLTP","scenario":"New OLTP: 50K TPS, < 5ms response, 24x7","tasks":["Design ASM diskgroup layout NORMAL redundancy","Configure Smart Flash Cache for OLTP hot blocks","Set IORM: OLTP priority, disable batch during peak"],"validation":"Architecture doc with performance targets validated","tag":"demo"},
      {"id":102,"title":"Design DW Workload with HCC","obj":"Architect Exadata for data warehouse with HCC compression","scenario":"2PB data warehouse migration to Exadata X8M","tasks":["Choose HCC level: QUERY HIGH for active, ARCHIVE HIGH for cold","Design partition strategy for Smart Scan eligibility","Calculate compression ratio and storage savings"],"validation":"DW design document with 10x compression target","tag":"demo"},
      {"id":103,"title":"Optimize Hybrid OLTP + DW Workload","obj":"Tune Exadata for mixed workload using IORM and HCC","scenario":"Single Exadata for both OLTP and overnight DW","tasks":["Configure IORM: OLTP share=8 day, DW share=8 night","Implement Resource Manager DB plan","Monitor wait events for both workloads during peak"],"validation":"Both workloads meet SLA, no starvation","tag":"lab"},
      {"id":104,"title":"Capacity Planning for Exadata","obj":"Build capacity model for 18-month growth","scenario":"Database growing 30% YoY - plan next Exadata expansion","tasks":["Collect current storage and CPU utilization trends","Model 18-month projection with growth rate","Identify when half-rack needs expansion to full-rack"],"validation":"Capacity model with expansion timeline","tag":"demo"},
      {"id":105,"title":"Cost vs Performance Tuning Decision","obj":"Evaluate trade-offs between optimization strategies","scenario":"Query runs 2 hours - multiple fix options available","tasks":["Option A: Add index (quick, cheap)","Option B: Rewrite query (medium effort)","Option C: Add cell node (expensive, permanent) - analyze each"],"validation":"Decision matrix with recommendation and justification","tag":"demo"},
    ],
  }},
}

LEVEL_COLORS = {"L1":"#5da8e8","L2":"#5dc888","L3":"#f39c12","L4":"#e74c3c"}
LEVEL_ICONS  = {"L1":"🔵","L2":"🟢","L3":"🟡","L4":"🔴"}
TAG_ICONS    = {"demo":"🔵 DEMO","lab":"🟢 LAB","quiz":"🔴 QUIZ"}

# ── SESSION STATE ────────────────────────────────────────────────────────────
DEFAULTS = {
    "openai_key":"","openai_model":"gpt-4o",
    "rack":"Half Rack","cells":7,"compute":4,
    "dg":"DATA+RECO","role":"DBA","level":"Intermediate",
    "current_level":"L1","current_group":"Database & PDB","current_lab_id":1,
    "messages":[],"tasks_done":set(),
    "score":0,"labs_completed":0,"tasks_completed":0,
}
for k,v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── HELPERS ──────────────────────────────────────────────────────────────────
def env_ctx():
    sw = {"1/8 Rack":1,"Quarter Rack":1,"Half Rack":2,"Full Rack":3}.get(st.session_state.rack,2)
    return (f"Rack={st.session_state.rack}, Cells={st.session_state.cells}, "
            f"Compute={st.session_state.compute}, IB_Switches={sw}, "
            f"DGs={st.session_state.dg}, Role={st.session_state.role}, Level={st.session_state.level}")

def get_current_lab():
    lvl = st.session_state.current_level
    grp = st.session_state.current_group
    lid = st.session_state.current_lab_id
    groups = LAB_CATALOG[lvl]["groups"]
    for lab in groups.get(grp,[]):
        if lab["id"] == lid: return lab
    first_grp = list(groups.keys())[0]
    return groups[first_grp][0]

def system_prompt():
    lab = get_current_lab()
    lvl = st.session_state.current_level
    return f"""You are ExaSimBot — Oracle Exadata X8M DBA/DMA Hands-On Lab Trainer.
ENVIRONMENT: {env_ctx()}
LEVEL: {lvl} | Lab #{lab["id"]}: {lab["title"]}
Objective: {lab["obj"]}
Scenario: {lab["scenario"]}
Tasks: {" | ".join([f"{i+1}. {t}" for i,t in enumerate(lab["tasks"])])}
Validation: {lab["validation"]}

RULES:
1. Commands ALWAYS in triple-backtick code blocks with correct prompt prefix (CellCLI>, SQL>, DGMGRL>, $, #)
2. Show realistic simulated Exadata output after every command
3. LAB steps: demo command then YOUR TURN exercise
4. QUIZ: MCQ A/B/C/D, score CORRECT or WRONG with explanation
5. Depth: Basic=concepts, Intermediate=full procedure, Advanced=internals+edge cases
6. DBA -> SQL/ASM/RMAN/srvctl | DMA -> hardware/firmware/ILOM/patchmgr
7. L4 incident labs: give symptoms first, ask user to diagnose before revealing answer
X8M SPECS: Compute 2x48c, 6TB RAM, 3.2TB PMEM, 2x200Gb IB | Cell 12x7.2TB HDD + 4x6.4TB NVMe + 1.5TB PMEM
Full rack 8+14+3 | Half 4+7+2 | Quarter 2+3+1
CellDisk: CD_00_dm01cel01..CD_15 | GridDisk: DATAC1_CD_00_dm01cel01
DCLI: dcli -g /etc/oracle/cell/network-config/cellgroup -l root cellcli -e "cmd"
Max 500 words. Be practical and example-driven."""

def task_key(lid, tidx): return f"lab{lid}_t{tidx}"
def mark_task_done(lid, tidx):
    k = task_key(lid, tidx)
    if k not in st.session_state.tasks_done:
        st.session_state.tasks_done.add(k)
        st.session_state.tasks_completed += 1
        st.session_state.score += 10

def get_lab_progress(lid, tasks):
    done = sum(1 for i in range(len(tasks)) if task_key(lid,i) in st.session_state.tasks_done)
    return done, len(tasks)

def build_rack_html():
    sw_n = {"1/8 Rack":1,"Quarter Rack":1,"Half Rack":2,"Full Rack":3}.get(st.session_state.rack,2)
    parts = ['<span class="ru ru-infra">PDU</span>','<span class="ru ru-infra">KVM</span>']
    for i in range(1,sw_n+1): parts.append(f'<span class="ru ru-sw">IB-SW{i}</span>')
    for i in range(1,st.session_state.compute+1): parts.append(f'<span class="ru ru-compute">DB{str(i).zfill(2)}</span>')
    for i in range(1,st.session_state.cells+1): parts.append(f'<span class="ru ru-cell">CEL{str(i).zfill(2)}</span>')
    return (f'<div class="rack-box"><div class="rack-lbl">RACK — {st.session_state.rack} · {st.session_state.cells} Storage Cells · {st.session_state.compute} Compute Nodes</div>' +
            f'<div class="rack-units">{" ".join(parts)}</div></div>')

def call_api(user_text, show_user=True):
    if not st.session_state.openai_key:
        st.markdown('<div class="chat-sys">Enter your OpenAI API key in the top config bar to start.</div>', unsafe_allow_html=True)
        return ""
    if show_user:
        st.markdown(f'<div class="chat-user">👤 {user_text}</div>', unsafe_allow_html=True)
    messages = [{"role":"system","content":system_prompt()}]
    for m in st.session_state.messages[-18:]:
        messages.append({"role":m["role"],"content":m["content"]})
    messages.append({"role":"user","content":user_text})
    placeholder = st.empty()
    full_text = ""
    try:
        client = OpenAI(api_key=st.session_state.openai_key)
        stream = client.chat.completions.create(model=st.session_state.openai_model,messages=messages,max_tokens=1500,temperature=0.4,stream=True)
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                full_text += delta
                placeholder.markdown(f'<div class="chat-bot">{full_text}&#9646;</div>', unsafe_allow_html=True)
        placeholder.markdown(f'<div class="chat-bot">{full_text}</div>', unsafe_allow_html=True)
    except Exception as e:
        err = str(e)
        if "401" in err or "Incorrect API key" in err: full_text = "Invalid API key. Check the key in the top config bar."
        elif "429" in err: full_text = "Rate limit. Wait a moment and retry."
        else: full_text = f"OpenAI error: {err}"
        placeholder.markdown(f'<div class="chat-bot">{full_text}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role":"user","content":user_text})
    st.session_state.messages.append({"role":"assistant","content":full_text})
    return full_text

def start_lab(lab):
    st.session_state.messages = []
    prompt = (f"[LAB #{lab['id']}: {lab['title']}] Level: {st.session_state.current_level} | {env_ctx()}\n\n"
              f"Objective: {lab['obj']}\nScenario: {lab['scenario']}\n\n"
              f"Set the scene briefly (2-3 sentences), then begin Task 1 with the demo command "
              f"and realistic Exadata output. End Task 1 with a YOUR TURN exercise.")
    with st.spinner(f"Loading Lab #{lab['id']}: {lab['title']}..."):
        call_api(prompt, show_user=False)

def quick_send(text):
    call_api(text)
    st.rerun()

# ── TOP BANNER ───────────────────────────────────────────────────────────────
api_ok = bool(st.session_state.openai_key)
st.markdown(f"""
<div class="top-banner">
  <div><div class="t-logo">Oracle Exadata</div>
  <div class="t-title">X8M DBA / DMA Hands-On Lab Simulator &nbsp;&middot;&nbsp; 105 Labs · 4 Levels</div></div>
  <div class="t-pills">
    <span class="pill">Labs <b>{st.session_state.labs_completed}</b></span>
    <span class="pill">Tasks <b>{st.session_state.tasks_completed}</b></span>
    <span class="pill">Score <b>{st.session_state.score}</b></span>
    <span class="{"st-ok" if api_ok else "st-err"}">{"✅ OpenAI connected" if api_ok else "⚠️ No API key"}</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── HORIZONTAL CONFIG BAR ────────────────────────────────────────────────────
c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([2.2,1.4,1.1,1.0,1.0,1.1,1.0,1.3,1.0])
with c1:
    k = st.text_input("OpenAI API Key", type="password", value=st.session_state.openai_key, placeholder="sk-...")
    if k: st.session_state.openai_key = k
with c2:
    mdl_opts = ["gpt-4o","gpt-4-turbo","gpt-4o-mini","gpt-3.5-turbo"]
    cur = st.session_state.openai_model if st.session_state.openai_model in mdl_opts else "gpt-4o"
    st.session_state.openai_model = st.selectbox("Model", mdl_opts, index=mdl_opts.index(cur))
with c3:
    rack_opts = ["1/8 Rack","Quarter Rack","Half Rack","Full Rack"]
    rack = st.selectbox("Rack", rack_opts, index=rack_opts.index(st.session_state.rack))
with c4:
    cells = st.selectbox("Cells", [3,7,14,18], index=[3,7,14,18].index(st.session_state.cells))
with c5:
    compute = st.selectbox("Compute", [2,4,8], index=[2,4,8].index(st.session_state.compute))
with c6:
    dg_opts = ["DATA+RECO","DATAC1+RECOC1","+FLASH"]
    cur_dg = st.session_state.dg if st.session_state.dg in dg_opts else "DATA+RECO"
    dg = st.selectbox("ASM DG", dg_opts, index=dg_opts.index(cur_dg))
with c7:
    role = st.selectbox("Role", ["DBA","DMA","Both"], index=["DBA","DMA","Both"].index(st.session_state.role))
with c8:
    level = st.selectbox("Level", ["Basic","Intermediate","Advanced"], index=["Basic","Intermediate","Advanced"].index(st.session_state.level))
with c9:
    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    if st.button("Apply", use_container_width=True, type="primary"):
        st.session_state.rack=rack; st.session_state.cells=cells; st.session_state.compute=compute
        st.session_state.dg=dg; st.session_state.role=role; st.session_state.level=level
        st.session_state.messages=[]; st.session_state.tasks_done=set()
        st.session_state.score=0; st.session_state.labs_completed=0; st.session_state.tasks_completed=0
        st.session_state.messages.append({"role":"assistant","content":f"Config applied: {rack} | {cells} cells | {compute} compute | {dg} | {role} | {level}. Select a lab from the sidebar."})
        st.rerun()

st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📚 Lab Catalog")
    for lvl_key, lvl_data in LAB_CATALOG.items():
        lc = lvl_data["color"]; li = lvl_data["icon"]
        st.markdown(f"<span style='color:{lc};font-size:11px;font-weight:700'>{li} {lvl_data['label']}</span>", unsafe_allow_html=True)
        for grp_name, labs in lvl_data["groups"].items():
            done_in_grp = sum(1 for lab in labs if any(task_key(lab["id"],i) in st.session_state.tasks_done for i in range(len(lab["tasks"]))))
            with st.expander(f"{grp_name} ({done_in_grp}/{len(labs)})", expanded=False):
                for lab in labs:
                    dt, tt = get_lab_progress(lab["id"], lab["tasks"])
                    is_active = (st.session_state.current_lab_id == lab["id"] and st.session_state.current_level == lvl_key)
                    chk = "✅" if dt==tt else ("▶" if is_active else "○")
                    btype = "primary" if is_active else "secondary"
                    if st.button(f"{chk} #{lab['id']} {lab['title']}", key=f"lb_{lvl_key}_{lab['id']}", use_container_width=True, type=btype):
                        st.session_state.current_level=lvl_key; st.session_state.current_group=grp_name; st.session_state.current_lab_id=lab["id"]
                        st.session_state.labs_completed += 1
                        start_lab(lab); st.rerun()

# ── MAIN LAB UI ──────────────────────────────────────────────────────────────
current_lab = get_current_lab()
lvl_key     = st.session_state.current_level
lvl_data    = LAB_CATALOG[lvl_key]
tasks       = current_lab["tasks"]
done_tasks, total_tasks = get_lab_progress(current_lab["id"], tasks)
prog_pct = int(done_tasks/total_tasks*100) if total_tasks else 0
lc = LEVEL_COLORS[lvl_key]

st.markdown(build_rack_html(), unsafe_allow_html=True)

hc1,hc2,hc3 = st.columns([3,1.5,0.8])
with hc1:
    st.markdown(f"<span style='color:{lc};font-size:11px;font-weight:700'>{LEVEL_ICONS[lvl_key]} {lvl_data['label']}</span> <span style='color:#4a7ab5;font-size:11px'>› {st.session_state.current_group}</span>", unsafe_allow_html=True)
    st.markdown(f"#### #{current_lab['id']} — {current_lab['title']}")
with hc2:
    st.markdown(f'<div class="obj-box"><b>Scenario:</b> {current_lab["scenario"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="val-box">✓ Validation: {current_lab["validation"]}</div>', unsafe_allow_html=True)
with hc3:
    st.markdown(f"<div style='text-align:right;font-size:11px;color:#8aadcc'>Tasks {done_tasks}/{total_tasks} ({prog_pct}%)</div>", unsafe_allow_html=True)
    st.markdown(f'<div class="prog-wrap"><div class="prog-bar" style="width:{prog_pct}%"></div></div>', unsafe_allow_html=True)
    tag_color = {"demo":"#5da8e8","lab":"#5dc888","quiz":"#e74c3c"}.get(current_lab["tag"],"#8aadcc")
    st.markdown(f"<span style='color:{tag_color};font-size:11px;font-weight:700'>{TAG_ICONS.get(current_lab['tag'],'')}</span>", unsafe_allow_html=True)

col_t, col_c, col_qa = st.columns([1.1, 3.8, 1.1])

with col_t:
    st.markdown("**Lab Tasks**")
    for i, task in enumerate(tasks):
        is_done = task_key(current_lab["id"], i) in st.session_state.tasks_done
        icon = "✅" if is_done else f"{i+1}."
        if st.button(f"{icon} {task}", key=f"t_{i}", use_container_width=True):
            mark_task_done(current_lab["id"], i)
            call_api(f"[TASK {i+1}: {task}] Lab #{current_lab['id']}: {current_lab['title']} | {env_ctx()}\nDemo this task with real Exadata commands and realistic output. Then give a YOUR TURN exercise.", show_user=False)
            st.rerun()
    st.markdown("---")
    st.markdown(f'<div style="font-size:10px;color:#8aadcc;line-height:1.5">{current_lab["obj"]}</div>', unsafe_allow_html=True)

with col_c:
    st.markdown("**Lab Terminal & Chat**")
    if not st.session_state.messages:
        st.markdown(f'<div class="chat-sys">Lab #{current_lab["id"]} ready. Click a task or use Quick Actions to begin.</div>', unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"]=="user" and not msg["content"].startswith("["):
                st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            elif msg["role"]=="assistant":
                st.markdown(f'<div class="chat-bot">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown("---")
    grp_lower = st.session_state.current_group.lower()
    if "asm" in grp_lower or "storage" in grp_lower or "backup" in grp_lower or "performance" in grp_lower or "security" in grp_lower or "monitor" in grp_lower or "user" in grp_lower:
        sym = "SQL>"
    elif "exadata" in grp_lower or "iorm" in grp_lower or "flash" in grp_lower or "cell" in grp_lower:
        sym = "CellCLI>"
    elif "data guard" in grp_lower:
        sym = "DGMGRL>"
    elif "rac" in grp_lower or "ha" in grp_lower:
        sym = "$"
    else:
        sym = "$"
    st.markdown(f'<div class="term-hdr">⬡ Practice Terminal &nbsp;|&nbsp; <b style="color:#5dc888">{sym}</b></div>', unsafe_allow_html=True)
    pt1,pt2 = st.columns([5,1])
    with pt1:
        cmd = st.text_input("cmd_in", key="pt_cmd", placeholder=f"{sym} type your command here...", label_visibility="collapsed")
    with pt2:
        run_btn = st.button("▶ Run", type="primary", use_container_width=True)
    if run_btn and cmd:
        st.markdown(f'<div class="term-hdr">{sym} {cmd}</div>', unsafe_allow_html=True)
        call_api(f"[PRACTICE TERMINAL] Typed: `{cmd}`\nLab #{current_lab['id']}: {current_lab['title']} | {env_ctx()}\nIn max 120 words: correct for this lab context? Show real Exadata output. Say CORRECT (+10pts) or WRONG with the right command.", show_user=False)
        st.rerun()
    if st.button("💡 Hint", use_container_width=False):
        call_api(f"Give a 1-2 sentence hint (no full answer) for Lab #{current_lab['id']}: {current_lab['title']}. Point them in the right direction.", show_user=False)
        st.rerun()
    user_q = st.chat_input("Ask anything about this lab, type your quiz answer, or request more detail...")
    if user_q:
        call_api(user_q); st.rerun()

with col_qa:
    st.markdown("**Quick Actions**")
    if st.button("▶ Start Lab", use_container_width=True, type="primary"):
        start_lab(current_lab); st.rerun()
    if st.button("▶ Demo Task 1", use_container_width=True):
        quick_send(f"Demo Task 1: {tasks[0]} with full Exadata commands and output.")
    if st.button("⌨ Practice", use_container_width=True):
        quick_send("Show the exact command for the current task, then give me a YOUR TURN exercise.")
    if st.button("? Quiz Me", use_container_width=True):
        quick_send("Quiz me on this lab topic with 3 MCQ questions and score my answers.")
    if st.button("📖 Theory", use_container_width=True):
        quick_send("Explain the theory and concepts behind this lab topic.")
    if st.button("⚠ Errors", use_container_width=True):
        quick_send("Show common errors and how to troubleshoot them for this lab topic.")
    if st.button("✅ Validate", use_container_width=True):
        quick_send(f"Show me how to validate completion of this lab. Criteria: {current_lab['validation']}")
    if st.button("→ Next Lab", use_container_width=True):
        all_labs = []
        for lk, ld in LAB_CATALOG.items():
            for gn, lbs in ld["groups"].items():
                for lb in lbs: all_labs.append((lb["id"],lb,lk,gn))
        cur_idx = next((i for i,(lid,_,_,_) in enumerate(all_labs) if lid==current_lab["id"]),0)
        if cur_idx < len(all_labs)-1:
            nid,nlab,nlvl,ngrp = all_labs[cur_idx+1]
            st.session_state.current_level=nlvl; st.session_state.current_group=ngrp
            st.session_state.current_lab_id=nid; st.session_state.labs_completed+=1
            start_lab(nlab); st.rerun()
    st.markdown("---")
    st.markdown(f"<div style='font-size:10px;color:#4a7ab5'>#{current_lab['id']} · <span style='color:{lc}'>{LEVEL_ICONS[lvl_key]} {lvl_key}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:11px;color:#c8dff0;margin-top:2px'>{current_lab['title']}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='font-size:10px;color:#4a7ab5'>LEVELS</div>", unsafe_allow_html=True)
    for lk2,lc2 in LEVEL_COLORS.items():
        st.markdown(f"<span style='color:{lc2};font-size:11px'>{LEVEL_ICONS[lk2]} {lk2} — {LAB_CATALOG[lk2]['label'].split('–')[1].strip()}</span>", unsafe_allow_html=True)
