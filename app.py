import streamlit as st
from openai import OpenAI

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Oracle Exadata X8M Simulator",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.top-banner {
    background: #060e1c; border-bottom: 2px solid #e74c3c;
    padding: 10px 18px 6px 18px; margin: -1rem -1rem 0.5rem -1rem;
    display: flex; align-items: center; gap: 16px;
}
.t-logo  { font-size:9px; color:#e74c3c; letter-spacing:3px; text-transform:uppercase;
           font-weight:700; font-family:'JetBrains Mono',monospace; }
.t-title { font-size:15px; color:#d0e8f8; font-weight:600; }
.t-pills { margin-left:auto; display:flex; gap:8px; align-items:center; }
.pill { background:#0d1e35; border:1px solid #1e3a5f; border-radius:20px;
        padding:3px 11px; font-size:11px; color:#8aadcc;
        font-family:'JetBrains Mono',monospace; }
.pill b { color:#f39c12; }
.st-ok  { font-size:11px; padding:3px 10px; border-radius:4px;
          background:#0a2a18; color:#5dc888; border:1px solid #1a5a30; }
.st-err { font-size:11px; padding:3px 10px; border-radius:4px;
          background:#2a0a0a; color:#e87a5a; border:1px solid #5a1a1a; }

.rack-box { background:#0d1e35; border-radius:6px; padding:8px 14px;
            border:1px solid #1e3a5f; margin-bottom:8px; }
.rack-lbl { font-size:9px; color:#4a7ab5; letter-spacing:1.5px; text-transform:uppercase;
            margin-bottom:5px; font-family:'JetBrains Mono',monospace; }
.rack-units { display:flex; flex-wrap:wrap; gap:3px; }
.ru { padding:2px 7px; border-radius:3px; font-size:9px; border:1px solid;
      font-family:'JetBrains Mono',monospace; display:inline-block; }
.ru-compute { background:#0e2a5a; color:#5da8e8; border-color:#1a4a9a; }
.ru-cell    { background:#0a2a18; color:#5dc888; border-color:#1a5a30; }
.ru-sw      { background:#1a0a3a; color:#a870c8; border-color:#4a1a7a; }
.ru-infra   { background:#2a1a0a; color:#c8a828; border-color:#6a4a18; }

.chat-user {
    background:#150808; border:1px solid #3a1010;
    border-radius:10px 10px 3px 10px;
    padding:9px 13px; margin:5px 0 5px 60px;
    color:#f0d0d0; font-size:13px; line-height:1.6;
}
.chat-bot {
    background:#0d1e35; border:1px solid #1e3a5f;
    border-radius:10px 10px 10px 3px;
    padding:9px 13px; margin:5px 0;
    color:#c8dff0; font-size:13px; line-height:1.65;
    font-family:'JetBrains Mono',monospace; white-space:pre-wrap;
}
.chat-sys {
    background:#111108; border:1px solid #3a3a10; border-radius:6px;
    padding:7px 12px; margin:5px 10px;
    color:#e0d898; font-size:11px; font-family:'JetBrains Mono',monospace;
}
.term-hdr {
    background:#020810; border:1px solid #1a4a2a; border-radius:5px 5px 0 0;
    padding:5px 12px; font-family:'JetBrains Mono',monospace;
    font-size:11px; color:#5dc888; margin-bottom:0;
}
.prog-wrap { background:#1e3a5f; border-radius:3px; height:5px; margin:4px 0 10px; }
.prog-bar  { background:#f39c12; border-radius:3px; height:100%; transition:width .3s; }

[data-testid="stSidebar"] {
    background:#070f1e !important;
    border-right:1px solid #1e3a5f;
    min-width:210px !important; max-width:210px !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span { color:#8aadcc !important; font-size:11px !important; }
[data-testid="stSidebar"] .stButton > button {
    background:transparent !important; border:1px solid #1e3a5f !important;
    color:#8aadcc !important; text-align:left !important;
    width:100% !important; border-radius:4px !important;
    font-size:11px !important; padding:5px 9px !important; margin-bottom:2px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background:#122240 !important; border-color:#2a5080 !important; color:#c8dff0 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background:#1a0a0a !important; border-color:#e74c3c !important; color:#e74c3c !important;
}

.stTextInput label, .stSelectbox label { color:#8aadcc !important; font-size:11px !important; }
.stTextInput input, .stSelectbox > div > div {
    background:#0d1e35 !important; border-color:#1e3a5f !important;
    color:#c8dff0 !important; font-size:12px !important;
}
.main .block-container { background:#0a1628; padding-top:0; max-width:100% !important; }
.stApp { background:#0a1628; }
hr { border-color:#1e3a5f !important; margin:6px 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# LAB DATA
# ─────────────────────────────────────────────────────────────────────────────
LABS = {
    "arch":      {"title":"X8M Architecture Overview",    "icon":"🏗️", "steps":[
        {"n":1,"t":"X8M hardware specs","tag":"demo"},
        {"n":2,"t":"PMEM & NVMe architecture","tag":"demo"},
        {"n":3,"t":"SQL-to-storage data path","tag":"demo"},
        {"n":4,"t":"Quiz: architecture","tag":"quiz"}]},
    "compute":   {"title":"Compute Nodes X8M-2",          "icon":"💻", "steps":[
        {"n":1,"t":"Node specs (CPU/RAM/PMEM)","tag":"demo"},
        {"n":2,"t":"Check node via DBMCLI","tag":"lab"},
        {"n":3,"t":"ILOM console access","tag":"lab"},
        {"n":4,"t":"Quiz: compute nodes","tag":"quiz"}]},
    "cell_svr":  {"title":"Cell Servers & Storage",       "icon":"💾", "steps":[
        {"n":1,"t":"Cell server specs & disk layout","tag":"demo"},
        {"n":2,"t":"LIST CELLDISK","tag":"lab"},
        {"n":3,"t":"LIST GRIDDISK DETAIL","tag":"lab"},
        {"n":4,"t":"DESCRIBE CELLDISK","tag":"lab"},
        {"n":5,"t":"Quiz: cell servers","tag":"quiz"}]},
    "ib":        {"title":"InfiniBand & RDMA",            "icon":"🔗", "steps":[
        {"n":1,"t":"IB HDR 100Gb topology","tag":"demo"},
        {"n":2,"t":"RDMA storage access","tag":"demo"},
        {"n":3,"t":"ibstatus / ibnetdiscover","tag":"lab"},
        {"n":4,"t":"Quiz: IB/RDMA","tag":"quiz"}]},
    "disk_add":  {"title":"Add Cell Disk (Hot-Add)",      "icon":"➕", "steps":[
        {"n":1,"t":"Hot-add workflow overview","tag":"demo"},
        {"n":2,"t":"LIST PHYSICALDISK — find disk","tag":"lab"},
        {"n":3,"t":"CREATE CELLDISK","tag":"lab"},
        {"n":4,"t":"Verify CELLDISK created","tag":"lab"},
        {"n":5,"t":"CREATE GRIDDISK on new celldisk","tag":"lab"},
        {"n":6,"t":"ALTER DISKGROUP ADD disk","tag":"lab"},
        {"n":7,"t":"Monitor ASM rebalance","tag":"lab"},
        {"n":8,"t":"Quiz: full disk add flow","tag":"quiz"}]},
    "griddisk":  {"title":"Create Grid Disks",            "icon":"🗄️", "steps":[
        {"n":1,"t":"CellDisk vs GridDisk concept","tag":"demo"},
        {"n":2,"t":"LIST CELLDISK — check free space","tag":"lab"},
        {"n":3,"t":"CREATE GRIDDISK with size","tag":"lab"},
        {"n":4,"t":"Verify in V$ASM_DISK","tag":"lab"},
        {"n":5,"t":"Quiz: grid disks","tag":"quiz"}]},
    "asm_dg":    {"title":"ASM Disk Group Admin",         "icon":"⚙️", "steps":[
        {"n":1,"t":"DG types & redundancy","tag":"demo"},
        {"n":2,"t":"V$ASM_DISKGROUP query","tag":"lab"},
        {"n":3,"t":"ALTER DISKGROUP ADD","tag":"lab"},
        {"n":4,"t":"Monitor rebalance","tag":"lab"},
        {"n":5,"t":"ALTER DISKGROUP DROP","tag":"lab"},
        {"n":6,"t":"Mount / Dismount","tag":"lab"},
        {"n":7,"t":"Quiz: ASM disk group","tag":"quiz"}]},
    "acfs":      {"title":"ACFS Creation",                "icon":"📁", "steps":[
        {"n":1,"t":"What is ACFS?","tag":"demo"},
        {"n":2,"t":"asmcmd volcreate","tag":"lab"},
        {"n":3,"t":"mkfs.acfs format","tag":"lab"},
        {"n":4,"t":"srvctl add filesystem","tag":"lab"},
        {"n":5,"t":"Mount on all nodes","tag":"lab"},
        {"n":6,"t":"Quiz: ACFS","tag":"quiz"}]},
    "acfs_db":   {"title":"Attach ACFS to DB",            "icon":"🔌", "steps":[
        {"n":1,"t":"Use cases for ACFS with DB","tag":"demo"},
        {"n":2,"t":"mkdir on ACFS mount","tag":"lab"},
        {"n":3,"t":"chown permissions","tag":"lab"},
        {"n":4,"t":"CREATE DIRECTORY SQL object","tag":"lab"},
        {"n":5,"t":"Test with Data Pump expdp","tag":"lab"},
        {"n":6,"t":"Quiz: ACFS with DB","tag":"quiz"}]},
    "cellcli":   {"title":"CellCLI Deep Dive",            "icon":"⌨️", "steps":[
        {"n":1,"t":"CellCLI basics & syntax","tag":"demo"},
        {"n":2,"t":"LIST commands","tag":"lab"},
        {"n":3,"t":"DESCRIBE objects","tag":"lab"},
        {"n":4,"t":"ALTER commands","tag":"lab"},
        {"n":5,"t":"Metrics & alerts","tag":"lab"},
        {"n":6,"t":"Quiz: CellCLI mastery","tag":"quiz"}]},
    "dcli":      {"title":"DCLI Parallel Operations",     "icon":"🔁", "steps":[
        {"n":1,"t":"DCLI overview","tag":"demo"},
        {"n":2,"t":"DCLI syntax & flags","tag":"lab"},
        {"n":3,"t":"Run CellCLI across all cells","tag":"lab"},
        {"n":4,"t":"DCLI for compute nodes","tag":"lab"},
        {"n":5,"t":"Quiz: DCLI","tag":"quiz"}]},
    "dbmcli":    {"title":"DBMCLI Administration",        "icon":"🖥️", "steps":[
        {"n":1,"t":"DBMCLI vs CellCLI","tag":"demo"},
        {"n":2,"t":"LIST DBSERVER detail","tag":"lab"},
        {"n":3,"t":"LIST PHYSICALDISK","tag":"lab"},
        {"n":4,"t":"Configure alerting","tag":"lab"},
        {"n":5,"t":"Quiz: DBMCLI","tag":"quiz"}]},
    "smart_scan":{"title":"Smart Scan Lab",               "icon":"🔍", "steps":[
        {"n":1,"t":"Smart Scan theory","tag":"demo"},
        {"n":2,"t":"Enable cell_offload_processing","tag":"lab"},
        {"n":3,"t":"Run Smart Scan eligible query","tag":"lab"},
        {"n":4,"t":"V$SYSSTAT offload stats","tag":"lab"},
        {"n":5,"t":"Quiz: Smart Scan","tag":"quiz"}]},
    "hcc":       {"title":"Hybrid Columnar Compression",  "icon":"🗜️", "steps":[
        {"n":1,"t":"4 HCC compression levels","tag":"demo"},
        {"n":2,"t":"CREATE TABLE with HCC","tag":"lab"},
        {"n":3,"t":"Measure compression ratio","tag":"lab"},
        {"n":4,"t":"DML behavior & row migration","tag":"demo"},
        {"n":5,"t":"Quiz: HCC","tag":"quiz"}]},
    "iorm":      {"title":"IORM Setup",                   "icon":"⚖️", "steps":[
        {"n":1,"t":"IORM concepts","tag":"demo"},
        {"n":2,"t":"LIST IORMPLAN","tag":"lab"},
        {"n":3,"t":"ALTER IORMPLAN with DB shares","tag":"lab"},
        {"n":4,"t":"Monitor V$CELL_IOREASON","tag":"lab"},
        {"n":5,"t":"Quiz: IORM","tag":"quiz"}]},
    "flash":     {"title":"Smart Flash Cache",            "icon":"⚡", "steps":[
        {"n":1,"t":"Write-back vs write-through","tag":"demo"},
        {"n":2,"t":"LIST FLASHCACHE / FLASHLOG","tag":"lab"},
        {"n":3,"t":"CREATE FLASHCACHE ALL","tag":"lab"},
        {"n":4,"t":"Monitor flash cache hit ratio","tag":"lab"},
        {"n":5,"t":"Quiz: Flash Cache","tag":"quiz"}]},
    "rac":       {"title":"RAC on Exadata",               "icon":"🔄", "steps":[
        {"n":1,"t":"RAC + X8M architecture","tag":"demo"},
        {"n":2,"t":"srvctl start/stop/status","tag":"lab"},
        {"n":3,"t":"Cache Fusion via RDMA","tag":"demo"},
        {"n":4,"t":"Quiz: RAC on Exadata","tag":"quiz"}]},
    "dg":        {"title":"Data Guard on Exadata",        "icon":"🛡️", "steps":[
        {"n":1,"t":"DG architecture on Exadata","tag":"demo"},
        {"n":2,"t":"DGMGRL switchover","tag":"lab"},
        {"n":3,"t":"Active Data Guard queries","tag":"lab"},
        {"n":4,"t":"Quiz: Data Guard","tag":"quiz"}]},
    "patch":     {"title":"Rolling Patch Exadata",        "icon":"🔧", "steps":[
        {"n":1,"t":"Patch types overview","tag":"demo"},
        {"n":2,"t":"exachk pre-patch check","tag":"lab"},
        {"n":3,"t":"patchmgr for storage cells","tag":"lab"},
        {"n":4,"t":"opatchauto for compute nodes","tag":"lab"},
        {"n":5,"t":"Post-patch validation","tag":"lab"},
        {"n":6,"t":"Quiz: patching","tag":"quiz"}]},
    "health":    {"title":"Health Checks",                "icon":"❤️", "steps":[
        {"n":1,"t":"exachk overview","tag":"demo"},
        {"n":2,"t":"Run full exachk","tag":"lab"},
        {"n":3,"t":"exadatadiag collection","tag":"lab"},
        {"n":4,"t":"OEM Exadata plug-in","tag":"demo"},
        {"n":5,"t":"Quiz: health checks","tag":"quiz"}]},
    "trouble":   {"title":"Troubleshooting Exadata",      "icon":"🚨", "steps":[
        {"n":1,"t":"Top 10 Exadata issues","tag":"demo"},
        {"n":2,"t":"Cell server offline — diagnose","tag":"lab"},
        {"n":3,"t":"Smart Scan disabled — fix","tag":"lab"},
        {"n":4,"t":"ASM rebalance stuck","tag":"lab"},
        {"n":5,"t":"IB link failure — diagnose","tag":"lab"},
        {"n":6,"t":"Live scenario quiz","tag":"quiz"}]},
}

LAB_GROUPS = {
    "🏗️ Architecture":    ["arch","compute","cell_svr","ib"],
    "💾 Storage Labs":     ["disk_add","griddisk","asm_dg","acfs","acfs_db"],
    "⌨️ CLI Mastery":      ["cellcli","dcli","dbmcli"],
    "✨ Exadata Features": ["smart_scan","hcc","iorm","flash"],
    "🚀 Advanced":         ["rac","dg","patch","health","trouble"],
}

STEP_PROMPTS = {
    "demo": (
        "Walk me through this step with full explanation.\n"
        "- ALL commands in triple-backtick code blocks with correct Exadata prompt "
        "(CellCLI>, SQL>, DBMCLI>, $, # etc.)\n"
        "- Show realistic simulated Exadata output after every command\n"
        "- Use clear section headings. Keep it practical."
    ),
    "lab": (
        "First DEMO this step:\n"
        "- Exact command in a code block with correct prompt prefix\n"
        "- Realistic simulated output\n"
        "- Explain what each part does\n\n"
        "Then end with:\n---\n"
        "**YOUR TURN — Practice Exercise:**\n"
        "Show the exact command to type (in a code block). "
        "Tell me to type it in the Practice Terminal and press Run ▶"
    ),
    "quiz": (
        "Quiz me on this topic with 3 MCQ questions, one by one.\n"
        "Format:\nQ1: [question]\nA) ...\nB) ...\nC) ...\nD) ...\n\n"
        "After I answer each, say CORRECT ✓ or WRONG ✗ with brief explanation, then next question."
    ),
}

PROMPT_SYMS = {
    "cellcli":"CellCLI>","disk_add":"CellCLI>","griddisk":"CellCLI>",
    "iorm":"CellCLI>","flash":"CellCLI>",
    "asm_dg":"SQL>","acfs_db":"SQL>","smart_scan":"SQL>","hcc":"SQL>",
    "dbmcli":"DBMCLI>","compute":"DBMCLI>",
    "acfs":"[root@exadb01]#",
}


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = {
    "openai_key":"", "openai_model":"gpt-4o",
    "rack":"Full Rack", "cells":14, "compute":4,
    "dg":"DATA+RECO", "role":"DBA", "level":"Intermediate",
    "current_lab":"arch", "current_step":0,
    "messages":[], "steps_done":set(),
    "score":0, "steps_completed":0, "labs_started":0,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def env_ctx():
    sw = {"1/8 Rack":1,"Quarter Rack":1,"Half Rack":2,"Full Rack":3}.get(st.session_state.rack,3)
    return (f"Rack={st.session_state.rack}, Cells={st.session_state.cells}, "
            f"Compute={st.session_state.compute}, IB_Switches={sw}, "
            f"DGs={st.session_state.dg}, Role={st.session_state.role}, "
            f"Level={st.session_state.level}")

def system_prompt():
    lab  = LABS[st.session_state.current_lab]
    step = lab["steps"][st.session_state.current_step]
    return f"""You are ExaSimBot — expert Oracle Exadata X8M DBA/DMA Hands-On Lab Trainer.

ENVIRONMENT: {env_ctx()}
Lab: {lab['title']} | Step {step['n']}: {step['t']} ({step['tag'].upper()})

RULES:
1. Commands always in triple-backtick code blocks with correct prompt prefix shown
2. Show realistic simulated Exadata output after every command
3. LAB steps: demo first, then clear "YOUR TURN" exercise
4. QUIZ steps: MCQ A/B/C/D, score as CORRECT ✓ or WRONG ✗
5. Depth: Basic=concepts, Intermediate=full procedure, Advanced=internals+edge cases
6. DBA → SQL/ASM/RMAN/srvctl; DMA → hardware/firmware/ILOM/patchmgr

X8M SPECS:
- Compute X8M-2: 2x Intel Cascade Lake-SP 8260 (48 cores total), 6TB DDR4, 3.2TB PMEM/node, 2x200Gb IB HDR
- Cell X8M-2: 12x7.2TB HDD + 4x6.4TB NVMe + 1.5TB PMEM, 2x200Gb IB
- Full rack: 8 compute+14 cells+3 IB switches; Half: 4+7+2; Quarter/1-8th: 2+3+1
- CellDisk: CD_00_dm01cel01..CD_15_dm01cel01
- GridDisk: DATAC1_CD_00_dm01cel01, RECOC1_CD_00_dm01cel01
- DCLI group: /etc/oracle/cell/network-config/cellgroup
- CellCLI> prompt on cell server (as root); DBMCLI> on compute node (as root)
Max ~450 words unless complexity demands more."""

def step_key(lab, idx): return f"{lab}_{idx}"

def mark_done(lab, idx):
    k = step_key(lab, idx)
    if k not in st.session_state.steps_done:
        st.session_state.steps_done.add(k)
        st.session_state.steps_completed += 1
        st.session_state.score += 10

def get_progress():
    lab   = st.session_state.current_lab
    steps = LABS[lab]["steps"]
    done  = sum(1 for i in range(len(steps)) if step_key(lab,i) in st.session_state.steps_done)
    return done, len(steps)

def build_rack_html():
    sw_n = {"1/8 Rack":1,"Quarter Rack":1,"Half Rack":2,"Full Rack":3}.get(st.session_state.rack,3)
    parts = ['<span class="ru ru-infra">PDU</span>',
             '<span class="ru ru-infra">KVM</span>']
    for i in range(1, sw_n+1):
        parts.append(f'<span class="ru ru-sw">IB-SW{i}</span>')
    for i in range(1, st.session_state.compute+1):
        parts.append(f'<span class="ru ru-compute">DB{str(i).zfill(2)}</span>')
    for i in range(1, st.session_state.cells+1):
        parts.append(f'<span class="ru ru-cell">CEL{str(i).zfill(2)}</span>')
    return (f'<div class="rack-box"><div class="rack-lbl">RACK — '
            f'{st.session_state.rack} · {st.session_state.cells} Storage Cells · '
            f'{st.session_state.compute} Compute Nodes</div>'
            f'<div class="rack-units">{"".join(parts)}</div></div>')


# ─────────────────────────────────────────────────────────────────────────────
# API — OpenAI streamed
# ─────────────────────────────────────────────────────────────────────────────
def call_api(user_text: str, show_user: bool = True) -> str:
    if not st.session_state.openai_key:
        msg = "⚠️ Enter your OpenAI API key in the top config bar to start."
        st.markdown(f'<div class="chat-sys">{msg}</div>', unsafe_allow_html=True)
        return msg

    if show_user:
        st.markdown(f'<div class="chat-user">👤 {user_text}</div>', unsafe_allow_html=True)

    # Build message history
    messages = [{"role": "system", "content": system_prompt()}]
    for m in st.session_state.messages[-18:]:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_text})

    placeholder = st.empty()
    full_text   = ""
    try:
        client = OpenAI(api_key=st.session_state.openai_key)
        stream = client.chat.completions.create(
            model=st.session_state.openai_model,
            messages=messages,
            max_tokens=1500,
            temperature=0.4,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                full_text += delta
                placeholder.markdown(
                    f'<div class="chat-bot">{full_text}▌</div>',
                    unsafe_allow_html=True
                )
        placeholder.markdown(f'<div class="chat-bot">{full_text}</div>', unsafe_allow_html=True)

    except Exception as e:
        err = str(e)
        if "401" in err or "Incorrect API key" in err:
            full_text = "⚠️ Invalid API key. Check the key in the top config bar."
        elif "429" in err:
            full_text = "⚠️ Rate limit hit. Wait a moment and retry."
        elif "model" in err.lower() or "404" in err:
            full_text = f"⚠️ Model not found — try gpt-4o or gpt-4-turbo. Detail: {err}"
        else:
            full_text = f"⚠️ OpenAI error: {err}"
        placeholder.markdown(f'<div class="chat-bot">{full_text}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "user",      "content": user_text})
    st.session_state.messages.append({"role": "assistant", "content": full_text})
    return full_text

def trigger_step(lab_key: str, step_idx: int):
    lab  = LABS[lab_key]
    step = lab["steps"][step_idx]
    prompt = (f"[LAB:{lab['title']}][STEP {step['n']}:{step['t']}]"
              f"[{step['tag'].upper()}][{env_ctx()}]\n\n{STEP_PROMPTS[step['tag']]}")
    with st.spinner(f"Loading Step {step['n']}: {step['t']}…"):
        call_api(prompt, show_user=False)
    mark_done(lab_key, step_idx)

def quick_send(text: str):
    call_api(text)
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ══ TOP BANNER ══
# ─────────────────────────────────────────────────────────────────────────────
done_cnt, total_cnt = get_progress()
prog_pct = int(done_cnt / total_cnt * 100) if total_cnt else 0
api_ok   = bool(st.session_state.openai_key)

st.markdown(f"""
<div class="top-banner">
  <div>
    <div class="t-logo">Oracle Exadata</div>
    <div class="t-title">X8M DBA / DMA Hands-On Lab Simulator</div>
  </div>
  <div class="t-pills">
    <span class="pill">Labs <b>{st.session_state.labs_started}</b></span>
    <span class="pill">Steps <b>{st.session_state.steps_completed}</b></span>
    <span class="pill">Score <b>{st.session_state.score}</b></span>
    <span class="{'st-ok' if api_ok else 'st-err'}">
      {'✅ OpenAI connected' if api_ok else '⚠️ No API key'}
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ══ HORIZONTAL CONFIG BAR ══
# ─────────────────────────────────────────────────────────────────────────────
c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([2.2, 1.3, 1.1, 1.1, 1.1, 1.1, 1.1, 1.3, 1.1])

with c1:
    k = st.text_input("OpenAI API Key", type="password",
                      value=st.session_state.openai_key, placeholder="sk-…")
    if k: st.session_state.openai_key = k

with c2:
    mdl_opts = ["gpt-4o","gpt-4-turbo","gpt-4o-mini","gpt-3.5-turbo"]
    cur_mdl  = st.session_state.openai_model if st.session_state.openai_model in mdl_opts else "gpt-4o"
    model    = st.selectbox("Model", mdl_opts, index=mdl_opts.index(cur_mdl))
    st.session_state.openai_model = model

with c3:
    rack = st.selectbox("Rack", ["1/8 Rack","Quarter Rack","Half Rack","Full Rack"],
                        index=["1/8 Rack","Quarter Rack","Half Rack","Full Rack"].index(st.session_state.rack))

with c4:
    cells = st.selectbox("Cells", [3,7,14,18],
                         index=[3,7,14,18].index(st.session_state.cells))

with c5:
    compute = st.selectbox("Compute", [2,4,8],
                           index=[2,4,8].index(st.session_state.compute))

with c6:
    dg_opts = ["DATA+RECO","DATAC1+RECOC1","+FLASH"]
    cur_dg  = st.session_state.dg if st.session_state.dg in dg_opts else "DATA+RECO"
    dg      = st.selectbox("ASM DG", dg_opts, index=dg_opts.index(cur_dg))

with c7:
    role = st.selectbox("Role", ["DBA","DMA","Both"],
                        index=["DBA","DMA","Both"].index(st.session_state.role))

with c8:
    level = st.selectbox("Level", ["Basic","Intermediate","Advanced"],
                         index=["Basic","Intermediate","Advanced"].index(st.session_state.level))

with c9:
    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    if st.button("⚙ Apply", use_container_width=True, type="primary"):
        st.session_state.rack=rack; st.session_state.cells=cells
        st.session_state.compute=compute; st.session_state.dg=dg
        st.session_state.role=role; st.session_state.level=level
        st.session_state.messages=[]; st.session_state.steps_done=set()
        st.session_state.score=0; st.session_state.steps_completed=0
        st.session_state.labs_started=0
        st.session_state.messages.append({"role":"assistant","content":
            f"✅ Environment set: {rack} | {cells} cells | {compute} compute | "
            f"{dg} | Role:{role} | Level:{level}\n\nSelect a lab from the left sidebar."})
        st.rerun()

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ══ SIDEBAR — lab navigation only ══
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📚 Lab Topics")
    for grp, keys in LAB_GROUPS.items():
        st.markdown(f"**{grp}**")
        for key in keys:
            lab     = LABS[key]
            ds      = sum(1 for i in range(len(lab["steps"])) if step_key(key,i) in st.session_state.steps_done)
            ts      = len(lab["steps"])
            suffix  = f" ✓{ds}/{ts}" if ds else ""
            label   = f"{lab['icon']} {lab['title']}{suffix}"
            active  = st.session_state.current_lab == key
            if st.button(label, key=f"lb_{key}", use_container_width=True,
                         type="primary" if active else "secondary"):
                if not active:
                    st.session_state.current_lab  = key
                    st.session_state.current_step = 0
                    st.session_state.labs_started += 1
                    st.session_state.messages     = []
                    trigger_step(key, 0)
                    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# ══ MAIN LAB UI — full width, 3 columns ══
# ─────────────────────────────────────────────────────────────────────────────
current_lab_data = LABS[st.session_state.current_lab]
steps            = current_lab_data["steps"]

# Rack + progress header
st.markdown(build_rack_html(), unsafe_allow_html=True)

hc1, hc2 = st.columns([4, 1])
with hc1:
    st.markdown(f"#### {current_lab_data['icon']} {current_lab_data['title']}")
with hc2:
    st.markdown(
        f"<div style='text-align:right;font-size:12px;color:#8aadcc;margin-top:10px'>"
        f"Progress {done_cnt}/{total_cnt} ({prog_pct}%)</div>",
        unsafe_allow_html=True
    )
st.markdown(
    f'<div class="prog-wrap"><div class="prog-bar" style="width:{prog_pct}%"></div></div>',
    unsafe_allow_html=True
)

# Three columns: Steps | Chat | Quick Actions
col_steps, col_chat, col_qa = st.columns([1.1, 3.8, 1.1])

# ── STEP CARDS ───────────────────────────────────────────────────────────────
with col_steps:
    st.markdown("**Lab Steps**")
    tag_icon = {"demo":"🔵","lab":"🟢","quiz":"🔴"}
    for i, step in enumerate(steps):
        is_done   = step_key(st.session_state.current_lab, i) in st.session_state.steps_done
        is_active = i == st.session_state.current_step
        si        = "✅" if is_done else ("▶️" if is_active else f"{step['n']}.")
        ti        = tag_icon.get(step["tag"],"⚪")
        btype     = "primary" if is_active and not is_done else "secondary"
        if st.button(f"{si} {step['t']} {ti}", key=f"s_{i}",
                     use_container_width=True, type=btype):
            st.session_state.current_step = i
            st.session_state.messages     = []
            trigger_step(st.session_state.current_lab, i)
            st.rerun()

# ── CHAT + PRACTICE TERMINAL ─────────────────────────────────────────────────
with col_chat:
    st.markdown("**Lab Terminal & Chat**")

    # Render chat history
    if not st.session_state.messages:
        st.markdown(
            '<div class="chat-sys">ExaSimBot ready — click a step or Quick Action to begin.</div>',
            unsafe_allow_html=True
        )
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user" and not msg["content"].startswith("[LAB:"):
                st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>',
                            unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f'<div class="chat-bot">{msg["content"]}</div>',
                            unsafe_allow_html=True)

    st.markdown("---")

    # Practice terminal
    sym = PROMPT_SYMS.get(st.session_state.current_lab, "$")
    st.markdown(
        f'<div class="term-hdr">⬡ Practice Terminal &nbsp;|&nbsp; '
        f'<b style="color:#5dc888">{sym}</b></div>',
        unsafe_allow_html=True
    )

    pt1, pt2 = st.columns([5, 1])
    with pt1:
        cmd = st.text_input("cmd_in", key="pt_cmd",
                            placeholder=f"{sym} type your command here…",
                            label_visibility="collapsed")
    with pt2:
        run_btn = st.button("▶ Run", type="primary", use_container_width=True)

    if run_btn and cmd:
        st.markdown(
            f'<div class="term-hdr">{sym} {cmd}</div>',
            unsafe_allow_html=True
        )
        step_data = steps[st.session_state.current_step]
        eval_p = (
            f"[PRACTICE TERMINAL] Typed: `{cmd}`\n"
            f"Step {step_data['n']}: {step_data['t']} | Lab: {current_lab_data['title']}\n"
            f"{env_ctx()}\n\n"
            f"In max 120 words: correct for this step? Show real Exadata output. "
            f"Say CORRECT ✓ (+10 pts) or WRONG ✗ with the right command."
        )
        call_api(eval_p, show_user=False)
        mark_done(st.session_state.current_lab, st.session_state.current_step)
        st.rerun()

    # Free-text input
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    user_q = st.chat_input("Ask a question, type your quiz answer, or request more detail…")
    if user_q:
        call_api(user_q)
        st.rerun()

# ── QUICK ACTIONS ─────────────────────────────────────────────────────────────
with col_qa:
    st.markdown("**Quick Actions**")
    if st.button("▶ Demo step",     use_container_width=True):
        quick_send("Demo this step with full Exadata commands and realistic output.")
    if st.button("⌨ Practice",      use_container_width=True):
        quick_send("Show me the exact command for this step, then give me a YOUR TURN exercise.")
    if st.button("? Quiz me",        use_container_width=True):
        quick_send("Quiz me on this topic with 3 MCQ questions and score my answers.")
    if st.button("📖 Theory",        use_container_width=True):
        quick_send("Explain the theory and concepts behind this topic in depth.")
    if st.button("⚠ Common Errors",  use_container_width=True):
        quick_send("Show common errors and troubleshooting for this topic.")
    if st.button("🔄 Next Step →",   use_container_width=True):
        nxt = min(st.session_state.current_step + 1, len(steps) - 1)
        st.session_state.current_step = nxt
        st.session_state.messages     = []
        trigger_step(st.session_state.current_lab, nxt)
        st.rerun()

    st.markdown("---")
    st.markdown("**Legend**")
    st.markdown("🔵 Demo &nbsp; 🟢 Lab &nbsp; 🔴 Quiz", unsafe_allow_html=True)
    st.markdown("---")
    cur_step = steps[st.session_state.current_step]
    st.markdown(f"**Step {cur_step['n']}:** {cur_step['t']}")
    st.markdown(f"**Prompt:** `{sym}`")
    st.markdown(f"**Mode:** {cur_step['tag'].upper()}")
