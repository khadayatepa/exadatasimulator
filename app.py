"""
Home page — Oracle Exadata X8M Lab Simulator
Shows: config bar, live architecture diagram, curriculum modules, lesson catalog.
Clicking a lesson opens the Lesson page (pages/1_Lesson.py).
"""
import streamlit as st
from exasim_core import (
    RACK_SPECS, CURRICULUM, GLOBAL_CSS, init_state, build_diagram
)
"""
Oracle Exadata X8M Lab Simulator
================================
Single-file Streamlit app with internal view routing (no multi-page tricks).
Author: Prashant | Oracle ACE (Apprentice) | prashantoracledba.wordpress.com

Run:
    pip install -r requirements.txt
    streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="Exadata X8M Simulator",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from exasim_core import (
    RACK_SPECS, CURRICULUM, GLOBAL_CSS, init_state, build_diagram,
    find_lesson, system_prompt, get_client, stream_response,
)

init_state()
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Initialise routing state
if "view" not in st.session_state:
    st.session_state.view = "home"


# =============================================================================
# HOME VIEW
# =============================================================================
def view_home():
    st.markdown("""
    <div style="border-bottom:1px solid #1a2c47;padding-bottom:12px;margin-bottom:18px;">
      <div class="brand-title">▸ ORACLE EXADATA X8M — LAB SIMULATOR</div>
      <div class="brand-sub">STRUCTURED DBA/DMA CURRICULUM • EXASIMBOT (OPENAI) • PRASHANT | ORACLE ACE (APPRENTICE)</div>
    </div>
    """, unsafe_allow_html=True)

    # Config bar
    c1, c2, c3, c4, c5, c6 = st.columns([2, 1.2, 1.2, 1.4, 1, 1])
    with c1:
        st.session_state.openai_key = st.text_input(
            "OpenAI API Key", value=st.session_state.openai_key,
            type="password", placeholder="sk-...")
    with c2:
        st.session_state.openai_model = st.selectbox(
            "Model", ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini", "gpt-3.5-turbo"],
            index=["gpt-4o","gpt-4-turbo","gpt-4o-mini","gpt-3.5-turbo"].index(st.session_state.openai_model))
    with c3:
        st.session_state.rack = st.selectbox(
            "Rack Size", list(RACK_SPECS.keys()),
            index=list(RACK_SPECS.keys()).index(st.session_state.rack))
    with c4:
        st.session_state.dg = st.selectbox(
            "ASM Disk Groups", ["DATA+RECO", "DATAC1+RECOC1", "DATAC1+RECOC1+FLASH"],
            index=["DATA+RECO","DATAC1+RECOC1","DATAC1+RECOC1+FLASH"].index(st.session_state.dg))
    with c5:
        st.session_state.role = st.selectbox(
            "Role", ["DBA", "DMA", "Both"],
            index=["DBA","DMA","Both"].index(st.session_state.role))
    with c6:
        st.session_state.level = st.selectbox(
            "Level", ["Basic", "Intermediate", "Advanced"],
            index=["Basic","Intermediate","Advanced"].index(st.session_state.level))

    specs = RACK_SPECS[st.session_state.rack]
    COMPUTE, CELLS, IB = specs["compute"], specs["cells"], specs["ib"]

    # Architecture + metrics
    left, right = st.columns([2.4, 1])
    with left:
        st.markdown('<div class="panel"><div class="panel-title">Live Rack Topology</div>',
                    unsafe_allow_html=True)
        st.markdown(build_diagram(COMPUTE, CELLS, IB, st.session_state.rack),
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        total_cores = COMPUTE * 48
        total_hdd = CELLS * 86.4
        total_flash = CELLS * 25.6
        total_cell_pmem = CELLS * 1.5
        hdd_disp = f"{total_hdd/1000:.2f} PB" if total_hdd >= 1000 else f"{total_hdd:.1f} TB"
        st.markdown(f'''
        <div class="panel">
          <div class="panel-title">Configuration Totals</div>
          <div class="metric-pill">Compute <span class="v">{COMPUTE}</span></div>
          <div class="metric-pill">Cells <span class="v">{CELLS}</span></div>
          <div class="metric-pill">IB SW <span class="v">{IB}</span></div><br>
          <div class="metric-pill">Cores <span class="v">{total_cores}</span></div>
          <div class="metric-pill">HDD <span class="v">{hdd_disp}</span></div><br>
          <div class="metric-pill">NVMe <span class="v">{total_flash:.1f} TB</span></div>
          <div class="metric-pill">PMEM <span class="v">{total_cell_pmem:.1f} TB</span></div><br>
          <div class="metric-pill">DG <span class="v">{st.session_state.dg}</span></div><br>
          <div class="metric-pill">Role <span class="v">{st.session_state.role}</span></div>
          <div class="metric-pill">Level <span class="v">{st.session_state.level}</span></div>
        </div>
        ''', unsafe_allow_html=True)

    # Curriculum overview
    st.markdown('<div class="section-header">Curriculum — Utility-Focused Path</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div style="color:#8ab4d8;font-size:14px;margin-bottom:14px;">'
        'Start with <b style="color:#f39c12">Module 0</b> (architecture foundations), then progress '
        'through each utility. Every lesson has 8 sections: '
        '<i>Why • How • Syntax • Demo • Practice • Scenario • Quiz • Free Chat</i>. '
        'Click <b>Open Lesson</b> to launch a dedicated workspace view.</div>',
        unsafe_allow_html=True
    )

    mod_keys = list(CURRICULUM.keys())
    for i in range(0, len(mod_keys), 3):
        cols = st.columns(3)
        for j, mkey in enumerate(mod_keys[i:i+3]):
            mod = CURRICULUM[mkey]
            with cols[j]:
                st.markdown(f'''
                <div class="module-card">
                  <h3>{mod["icon"]} {mkey} — {mod["title"]}</h3>
                  <div class="mdesc">{mod["desc"]}</div>
                  <div class="mcount">{len(mod["lessons"])} lessons</div>
                </div>
                ''', unsafe_allow_html=True)

    # Lesson catalog tabs
    st.markdown('<div class="section-header">Lessons</div>', unsafe_allow_html=True)
    st.caption("Select a module tab below, then click **Open Lesson** to launch the training workspace.")

    tab_labels = [f"{CURRICULUM[k]['icon']} {k}" for k in mod_keys]
    tabs = st.tabs(tab_labels)
    for tab, mkey in zip(tabs, mod_keys):
        mod = CURRICULUM[mkey]
        with tab:
            st.markdown(f"**{mod['title']}** — {mod['desc']}")
            for lesson in mod["lessons"]:
                col_a, col_b = st.columns([6, 1.2])
                with col_a:
                    st.markdown(f'''
                    <div class="lesson-row">
                      <div>
                        <span class="lid">{lesson["id"]}</span> &nbsp;
                        <span class="ltitle">{lesson["title"]}</span> &nbsp;
                        <span class="level-{lesson["level"]}">{lesson["level"]}</span>
                      </div>
                    </div>
                    ''', unsafe_allow_html=True)
                with col_b:
                    if st.button("Open Lesson", key=f"btn_{lesson['id']}",
                                 use_container_width=True):
                        st.session_state.active_lesson_id = lesson["id"]
                        st.session_state.view = "lesson"
                        st.rerun()

    # Footer
    st.markdown("""
    <div style="text-align:center;color:#6a8faa;font-size:11px;
                letter-spacing:2px;margin-top:30px;padding:14px;
                border-top:1px solid #1a2c47;">
    EXADATA X8M SIMULATOR • STREAMLIT + OPENAI GPT-4o<br>
    PRASHANT | ORACLE ACE (APPRENTICE) | PRASHANTORACLEDBA.WORDPRESS.COM
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# LESSON VIEW
# =============================================================================
def view_lesson():
    lesson_id = st.session_state.get("active_lesson_id")
    if not lesson_id:
        st.warning("No lesson selected.")
        if st.button("← Back to Home"):
            st.session_state.view = "home"
            st.rerun()
        return

    mkey, mod, lesson = find_lesson(lesson_id)
    if not lesson:
        st.error(f"Lesson {lesson_id} not found.")
        if st.button("← Back to Home"):
            st.session_state.view = "home"
            st.rerun()
        return

    # Per-lesson state
    if lesson_id not in st.session_state.chat:
        st.session_state.chat[lesson_id] = []

    # Header + back
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Home", use_container_width=True):
            st.session_state.view = "home"
            st.rerun()
    with col_title:
        st.markdown(f'''
        <div style="border-bottom:1px solid #1a2c47;padding-bottom:10px;">
          <div class="brand-title">{mod["icon"]} {lesson["id"]} — {lesson["title"]}</div>
          <div class="brand-sub">
            MODULE: {mkey} • {mod["title"]} &nbsp;•&nbsp;
            <span class="level-{lesson["level"]}" style="padding:2px 10px;border-radius:10px;">
              {lesson["level"]}
            </span>
          </div>
        </div>
        ''', unsafe_allow_html=True)

    specs = RACK_SPECS[st.session_state.rack]
    st.markdown(f'''
    <div style="margin-top:10px;">
      <div class="metric-pill">Rack <span class="v">{st.session_state.rack}</span></div>
      <div class="metric-pill">Compute <span class="v">{specs["compute"]}</span></div>
      <div class="metric-pill">Cells <span class="v">{specs["cells"]}</span></div>
      <div class="metric-pill">DG <span class="v">{st.session_state.dg}</span></div>
      <div class="metric-pill">Role <span class="v">{st.session_state.role}</span></div>
      <div class="metric-pill">Level <span class="v">{st.session_state.level}</span></div>
      <div class="metric-pill">Model <span class="v">{st.session_state.openai_model}</span></div>
    </div>
    ''', unsafe_allow_html=True)

    tab_why, tab_how, tab_syntax, tab_demo, tab_practice, tab_scenario, tab_quiz, tab_chat = st.tabs([
        "🎯 Why", "🏗 How", "📜 Syntax", "▶ Demo", "⌨ Practice",
        "🚨 Scenario", "❓ Quiz", "💬 Chat",
    ])

    # ---- WHY ----
    with tab_why:
        st.markdown('<div class="section-header">Why This Matters</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="why-box">{lesson["why"]}</div>', unsafe_allow_html=True)
        st.caption("Understanding the *why* is the single biggest predictor of long-term retention. "
                   "Don't skip this — even senior DBAs who skip the rationale end up using Exadata "
                   "as an expensive commodity database.")

    # ---- HOW ----
    with tab_how:
        st.markdown('<div class="section-header">How It Works — Architecture</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="how-box">{lesson["how"]}</div>', unsafe_allow_html=True)
        st.caption("This is the mechanical model you should be able to draw on a whiteboard.")

    # ---- SYNTAX ----
    with tab_syntax:
        st.markdown('<div class="section-header">Syntax & Commands Reference</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="syntax-box">{lesson["syntax"]}</div>', unsafe_allow_html=True)
        st.caption("Copy these commands. Modify for your environment. Try them in Demo or Practice.")

    # ---- DEMO ----
    with tab_demo:
        st.markdown('<div class="section-header">Live AI-Simulated Demo</div>', unsafe_allow_html=True)
        st.caption("ExaSimBot walks through this lesson with realistic simulated output tuned to your environment.")

        demo_key = f"demo_{lesson_id}"
        if demo_key not in st.session_state:
            st.session_state[demo_key] = ""

        col_d1, col_d2 = st.columns([1, 5])
        run_demo = False
        with col_d1:
            if st.button("▶ Run Demo", key=f"rundemo_{lesson_id}", use_container_width=True):
                run_demo = True
        with col_d2:
            if st.button("↻ Regenerate", key=f"regen_{lesson_id}"):
                st.session_state[demo_key] = ""
                run_demo = True

        if run_demo:
            client = get_client()
            if not client:
                st.error("⚠ Enter your OpenAI API key in the Home view.")
            else:
                placeholder = st.empty()
                try:
                    out = stream_response(
                        client,
                        [
                            {"role": "system", "content": system_prompt(lesson, "demo")},
                            {"role": "user", "content": lesson["demo_prompt"]},
                        ],
                        placeholder,
                    )
                    st.session_state[demo_key] = out
                except Exception as e:
                    st.error(f"OpenAI error: {e}")
        elif st.session_state[demo_key]:
            st.markdown(st.session_state[demo_key])

    # ---- PRACTICE ----
    with tab_practice:
        st.markdown('<div class="section-header">Hands-On Practice Terminal</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="how-box"><b>Your task:</b> {lesson["practice"]}</div>',
                    unsafe_allow_html=True)

        hist_key = f"practice_hist_{lesson_id}"
        if hist_key not in st.session_state:
            st.session_state[hist_key] = []

        title_lc = lesson["title"].lower()
        module_lc = mod["title"].lower()
        if "cellcli" in module_lc or "cellcli" in title_lc or "flash" in title_lc:
            sym = "CellCLI>"
        elif "dcli" in module_lc:
            sym = "$"
        elif "asm" in module_lc:
            sym = "SQL>"
        elif "data guard" in module_lc or "dgmgrl" in title_lc or "switchover" in title_lc:
            sym = "DGMGRL>"
        elif "rman" in module_lc:
            sym = "RMAN>"
        elif "srvctl" in title_lc or "crsctl" in title_lc or "cluster" in module_lc:
            sym = "$"
        else:
            sym = "SQL>"

        # Terminal display
        term_html = ('<div style="background:#030a14;border:1px solid #1a4a2a;border-radius:6px;'
                     'padding:14px;font-family:\'Share Tech Mono\',monospace;color:#00ff88;'
                     'font-size:13px;line-height:1.6;max-height:360px;overflow-y:auto;">')
        term_html += '<div style="color:#f39c12">[ ExaSimBot Practice Terminal — type a command below ]</div><br>'
        for entry in st.session_state[hist_key][-10:]:
            term_html += (f'<div><span style="color:#f39c12;font-weight:700">{entry["sym"]}</span> '
                          f'<span style="color:#c8dff8">{entry["cmd"]}</span></div>')
            if entry.get("out"):
                safe_out = entry["out"].replace("<", "&lt;").replace(">", "&gt;")
                term_html += (f'<div style="color:#66c2ff;margin:4px 0 10px 0;'
                              f'white-space:pre-wrap;">{safe_out}</div>')
        term_html += (f'<div><span style="color:#f39c12;font-weight:700">{sym}</span> '
                      f'<span style="color:#f39c12">_</span></div></div>')
        st.markdown(term_html, unsafe_allow_html=True)

        col_p1, col_p2, col_p3 = st.columns([5, 1, 1])
        with col_p1:
            cmd = st.text_input("Command", key=f"cmd_{lesson_id}",
                                placeholder=f"{sym} type your command and press Evaluate",
                                label_visibility="collapsed")
        with col_p2:
            eval_btn = st.button("Evaluate", key=f"eval_{lesson_id}", use_container_width=True)
        with col_p3:
            clear_btn = st.button("Clear", key=f"clear_{lesson_id}", use_container_width=True)

        if clear_btn:
            st.session_state[hist_key] = []
            st.rerun()

        if eval_btn and cmd:
            client = get_client()
            if not client:
                st.error("⚠ Enter your OpenAI API key in the Home view.")
            else:
                try:
                    eval_req = (
                        f"User typed this command for the practice task:\n`{cmd}`\n\n"
                        f"The task was: {lesson['practice']}\n\n"
                        f"Evaluate it in under 150 words. Show realistic simulated output. "
                        f"End with CORRECT ✓ (+10 pts) or WRONG ✗ and the right command."
                    )
                    resp = client.chat.completions.create(
                        model=st.session_state.openai_model,
                        messages=[
                            {"role": "system", "content": system_prompt(lesson, "practice")},
                            {"role": "user", "content": eval_req},
                        ],
                        max_tokens=600,
                        temperature=0.3,
                    )
                    output = resp.choices[0].message.content
                    st.session_state[hist_key].append({"sym": sym, "cmd": cmd, "out": output})
                    st.rerun()
                except Exception as e:
                    st.error(f"OpenAI error: {e}")

    # ---- SCENARIO ----
    with tab_scenario:
        st.markdown('<div class="section-header">Real-World Scenario</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="real-box"><b>The situation:</b> {lesson["real_world"]}</div>',
                    unsafe_allow_html=True)
        st.caption("ExaSimBot will role-play this incident, present symptoms, and guide you through diagnosis.")

        scn_key = f"scenario_{lesson_id}"
        if scn_key not in st.session_state:
            st.session_state[scn_key] = []

        if st.button("▶ Start / Restart Scenario", key=f"startscn_{lesson_id}"):
            client = get_client()
            if not client:
                st.error("⚠ Enter your OpenAI API key in the Home view.")
            else:
                try:
                    placeholder = st.empty()
                    user_msg = ("Start the scenario. Present the initial symptoms/alerts only — "
                                "do NOT reveal the root cause. Ask me: 'What do you check first?' at the end.")
                    out = stream_response(
                        client,
                        [
                            {"role": "system", "content": system_prompt(lesson, "scenario")},
                            {"role": "user", "content": user_msg},
                        ],
                        placeholder,
                    )
                    st.session_state[scn_key] = [
                        {"role": "user", "content": user_msg},
                        {"role": "assistant", "content": out},
                    ]
                except Exception as e:
                    st.error(f"OpenAI error: {e}")

        for msg in st.session_state[scn_key][1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state[scn_key]:
            scn_input = st.chat_input("Your diagnostic action or question...",
                                      key=f"scn_in_{lesson_id}")
            if scn_input:
                client = get_client()
                if client:
                    st.session_state[scn_key].append({"role": "user", "content": scn_input})
                    with st.chat_message("user"):
                        st.markdown(scn_input)
                    try:
                        placeholder = st.empty()
                        with st.chat_message("assistant"):
                            messages = [{"role": "system", "content": system_prompt(lesson, "scenario")}]
                            messages.extend(st.session_state[scn_key][-12:])
                            out = stream_response(client, messages, placeholder)
                        st.session_state[scn_key].append({"role": "assistant", "content": out})
                    except Exception as e:
                        st.error(f"OpenAI error: {e}")

    # ---- QUIZ ----
    with tab_quiz:
        st.markdown('<div class="section-header">Knowledge Check — MCQ Quiz</div>', unsafe_allow_html=True)
        st.caption(f"3-question multiple choice quiz on: **{lesson['quiz_topic']}**.")

        qz_key = f"quiz_{lesson_id}"
        if qz_key not in st.session_state:
            st.session_state[qz_key] = []

        if st.button("▶ Start / Restart Quiz", key=f"startqz_{lesson_id}"):
            client = get_client()
            if not client:
                st.error("⚠ Enter your OpenAI API key in the Home view.")
            else:
                try:
                    placeholder = st.empty()
                    out = stream_response(
                        client,
                        [
                            {"role": "system", "content": system_prompt(lesson, "quiz")},
                            {"role": "user", "content": (f"Start the quiz. Ask question 1 of 3 on the topic: "
                                                          f"{lesson['quiz_topic']}. Present only Q1 with 4 "
                                                          f"options A/B/C/D. Wait for my answer.")},
                        ],
                        placeholder,
                    )
                    st.session_state[qz_key] = [
                        {"role": "user", "content": "Start quiz"},
                        {"role": "assistant", "content": out},
                    ]
                except Exception as e:
                    st.error(f"OpenAI error: {e}")

        for msg in st.session_state[qz_key][1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state[qz_key]:
            ans = st.chat_input("Your answer (A/B/C/D)...", key=f"qz_in_{lesson_id}")
            if ans:
                client = get_client()
                if client:
                    st.session_state[qz_key].append({"role": "user", "content": ans})
                    with st.chat_message("user"):
                        st.markdown(ans)
                    try:
                        placeholder = st.empty()
                        with st.chat_message("assistant"):
                            messages = [{"role": "system", "content": system_prompt(lesson, "quiz")}]
                            messages.extend(st.session_state[qz_key][-12:])
                            out = stream_response(client, messages, placeholder)
                        st.session_state[qz_key].append({"role": "assistant", "content": out})
                    except Exception as e:
                        st.error(f"OpenAI error: {e}")

    # ---- FREE CHAT ----
    with tab_chat:
        st.markdown('<div class="section-header">Ask ExaSimBot Anything</div>', unsafe_allow_html=True)
        st.caption("Free-form chat scoped to this lesson.")

        for msg in st.session_state.chat[lesson_id]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_q = st.chat_input("Ask about this lesson...", key=f"chat_in_{lesson_id}")
        if user_q:
            client = get_client()
            if not client:
                st.error("⚠ Enter your OpenAI API key in the Home view.")
            else:
                st.session_state.chat[lesson_id].append({"role": "user", "content": user_q})
                with st.chat_message("user"):
                    st.markdown(user_q)
                try:
                    placeholder = st.empty()
                    with st.chat_message("assistant"):
                        messages = [{"role": "system", "content": system_prompt(lesson, "chat")}]
                        messages.extend(st.session_state.chat[lesson_id][-16:])
                        out = stream_response(client, messages, placeholder)
                    st.session_state.chat[lesson_id].append({"role": "assistant", "content": out})
                except Exception as e:
                    st.error(f"OpenAI error: {e}")


# =============================================================================
# ROUTER
# =============================================================================
if st.session_state.view == "home":
    view_home()
elif st.session_state.view == "lesson":
    view_lesson()
else:
    st.session_state.view = "home"
    view_home()
st.set_page_config(
    page_title="Exadata X8M Simulator",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
init_state()

# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div style="border-bottom:1px solid #1a2c47;padding-bottom:12px;margin-bottom:18px;">
  <div class="brand-title">▸ ORACLE EXADATA X8M — LAB SIMULATOR</div>
  <div class="brand-sub">STRUCTURED DBA/DMA CURRICULUM • EXASIMBOT (OPENAI) • PRASHANT | ORACLE ACE (APPRENTICE)</div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# CONFIG BAR
# =============================================================================
c1, c2, c3, c4, c5, c6 = st.columns([2, 1.2, 1.2, 1.4, 1, 1])
with c1:
    st.session_state.openai_key = st.text_input(
        "OpenAI API Key", value=st.session_state.openai_key,
        type="password", placeholder="sk-...")
with c2:
    st.session_state.openai_model = st.selectbox(
        "Model", ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini", "gpt-3.5-turbo"],
        index=["gpt-4o","gpt-4-turbo","gpt-4o-mini","gpt-3.5-turbo"].index(st.session_state.openai_model))
with c3:
    st.session_state.rack = st.selectbox(
        "Rack Size", list(RACK_SPECS.keys()),
        index=list(RACK_SPECS.keys()).index(st.session_state.rack))
with c4:
    st.session_state.dg = st.selectbox(
        "ASM Disk Groups", ["DATA+RECO", "DATAC1+RECOC1", "DATAC1+RECOC1+FLASH"],
        index=["DATA+RECO","DATAC1+RECOC1","DATAC1+RECOC1+FLASH"].index(st.session_state.dg))
with c5:
    st.session_state.role = st.selectbox(
        "Role", ["DBA", "DMA", "Both"],
        index=["DBA","DMA","Both"].index(st.session_state.role))
with c6:
    st.session_state.level = st.selectbox(
        "Level", ["Basic", "Intermediate", "Advanced"],
        index=["Basic","Intermediate","Advanced"].index(st.session_state.level))

specs = RACK_SPECS[st.session_state.rack]
COMPUTE, CELLS, IB = specs["compute"], specs["cells"], specs["ib"]

# =============================================================================
# ARCHITECTURE + METRICS
# =============================================================================
left, right = st.columns([2.4, 1])

with left:
    st.markdown('<div class="panel"><div class="panel-title">Live Rack Topology</div>',
                unsafe_allow_html=True)
    st.markdown(build_diagram(COMPUTE, CELLS, IB, st.session_state.rack),
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    total_cores = COMPUTE * 48
    total_hdd = CELLS * 86.4
    total_flash = CELLS * 25.6
    total_cell_pmem = CELLS * 1.5
    hdd_disp = f"{total_hdd/1000:.2f} PB" if total_hdd >= 1000 else f"{total_hdd:.1f} TB"
    st.markdown(f'''
    <div class="panel">
      <div class="panel-title">Configuration Totals</div>
      <div class="metric-pill">Compute <span class="v">{COMPUTE}</span></div>
      <div class="metric-pill">Cells <span class="v">{CELLS}</span></div>
      <div class="metric-pill">IB SW <span class="v">{IB}</span></div><br>
      <div class="metric-pill">Cores <span class="v">{total_cores}</span></div>
      <div class="metric-pill">HDD <span class="v">{hdd_disp}</span></div><br>
      <div class="metric-pill">NVMe <span class="v">{total_flash:.1f} TB</span></div>
      <div class="metric-pill">PMEM <span class="v">{total_cell_pmem:.1f} TB</span></div><br>
      <div class="metric-pill">DG <span class="v">{st.session_state.dg}</span></div><br>
      <div class="metric-pill">Role <span class="v">{st.session_state.role}</span></div>
      <div class="metric-pill">Level <span class="v">{st.session_state.level}</span></div>
    </div>
    ''', unsafe_allow_html=True)

# =============================================================================
# CURRICULUM OVERVIEW
# =============================================================================
st.markdown('<div class="section-header">Curriculum — Utility-Focused Path</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div style="color:#8ab4d8;font-size:14px;margin-bottom:14px;">'
    'Start with <b style="color:#f39c12">Module 0</b> (architecture foundations), then progress '
    'through each utility. Every lesson has 7 sections: '
    '<i>Why • How • Syntax • Demo • Practice • Scenario • Quiz</i>. '
    'Click <b>Open Lesson</b> to launch it in a dedicated workspace.</div>',
    unsafe_allow_html=True
)

# Render module cards in a grid
mod_keys = list(CURRICULUM.keys())
for i in range(0, len(mod_keys), 3):
    cols = st.columns(3)
    for j, mkey in enumerate(mod_keys[i:i+3]):
        mod = CURRICULUM[mkey]
        with cols[j]:
            st.markdown(f'''
            <div class="module-card">
              <h3>{mod["icon"]} {mkey} — {mod["title"]}</h3>
              <div class="mdesc">{mod["desc"]}</div>
              <div class="mcount">{len(mod["lessons"])} lessons</div>
            </div>
            ''', unsafe_allow_html=True)

# =============================================================================
# LESSON CATALOG — ONE TAB PER MODULE
# =============================================================================
st.markdown('<div class="section-header">Lessons</div>', unsafe_allow_html=True)
st.caption("Select a module tab below, then click **Open Lesson** to launch the training workspace.")

tab_labels = [f"{CURRICULUM[k]['icon']} {k}" for k in mod_keys]
tabs = st.tabs(tab_labels)

for tab, mkey in zip(tabs, mod_keys):
    mod = CURRICULUM[mkey]
    with tab:
        st.markdown(f"**{mod['title']}** — {mod['desc']}")
        for lesson in mod["lessons"]:
            col_a, col_b = st.columns([6, 1.2])
            with col_a:
                st.markdown(f'''
                <div class="lesson-row">
                  <div>
                    <span class="lid">{lesson["id"]}</span> &nbsp;
                    <span class="ltitle">{lesson["title"]}</span> &nbsp;
                    <span class="level-{lesson["level"]}">{lesson["level"]}</span>
                  </div>
                </div>
                ''', unsafe_allow_html=True)
            with col_b:
                if st.button("Open Lesson", key=f"btn_{lesson['id']}",
                             use_container_width=True):
                    st.session_state.active_lesson_id = lesson["id"]
                    st.switch_page("pages/1_Lesson.py")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div style="text-align:center;color:#6a8faa;font-size:11px;
            letter-spacing:2px;margin-top:30px;padding:14px;
            border-top:1px solid #1a2c47;">
EXADATA X8M SIMULATOR • STREAMLIT + OPENAI GPT-4o<br>
PRASHANT | ORACLE ACE (APPRENTICE) | PRASHANTORACLEDBA.WORDPRESS.COM
</div>
""", unsafe_allow_html=True)
