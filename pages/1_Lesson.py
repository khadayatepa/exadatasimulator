"""
Lesson Workspace — dedicated page for a single lesson.
Sections: Overview, Why, How, Syntax, Demo (AI), Practice Terminal (AI),
Real-World Scenario (AI), Quiz (AI). Plus a free-chat with ExaSimBot.
"""
import streamlit as st
import sys, os
# Ensure parent dir is importable for exasim_core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exasim_core import (
    GLOBAL_CSS, init_state, find_lesson, system_prompt, get_client,
    stream_response, RACK_SPECS
)

st.set_page_config(
    page_title="Lesson Workspace",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
init_state()

# =============================================================================
# Guard: must have an active lesson
# =============================================================================
lesson_id = st.session_state.get("active_lesson_id")
if not lesson_id:
    st.markdown('<div class="brand-title">▸ NO LESSON SELECTED</div>', unsafe_allow_html=True)
    st.warning("Please return to the Home page and click **Open Lesson** on any lesson.")
    if st.button("← Back to Home"):
        st.switch_page("app.py")
    st.stop()

mkey, mod, lesson = find_lesson(lesson_id)
if not lesson:
    st.error(f"Lesson {lesson_id} not found.")
    st.stop()

# Per-lesson chat state
if lesson_id not in st.session_state.chat:
    st.session_state.chat[lesson_id] = []
if lesson_id not in st.session_state.quiz_state:
    st.session_state.quiz_state[lesson_id] = {"score": 0, "asked": 0}

# =============================================================================
# HEADER + BACK BUTTON
# =============================================================================
col_back, col_title = st.columns([1, 5])
with col_back:
    if st.button("← Home", use_container_width=True):
        st.switch_page("app.py")
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

# Environment summary strip
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

# =============================================================================
# SECTION TABS
# =============================================================================
tab_why, tab_how, tab_syntax, tab_demo, tab_practice, tab_scenario, tab_quiz, tab_chat = st.tabs([
    "🎯 Why Use It",
    "🏗 How It Works",
    "📜 Syntax",
    "▶ Live Demo (AI)",
    "⌨ Hands-On Practice",
    "🚨 Real-World Scenario",
    "❓ Quiz",
    "💬 Free Chat",
])

# ---------------------------------------------------------------------------
# WHY
# ---------------------------------------------------------------------------
with tab_why:
    st.markdown('<div class="section-header">Why This Matters</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="why-box">{lesson["why"]}</div>', unsafe_allow_html=True)
    st.caption("Understanding *why* a tool exists is the single biggest predictor of long-term retention. "
               "Don't skip this section — even senior DBAs coming from non-Exadata backgrounds miss the 'why' "
               "and end up using Exadata as an expensive commodity database.")

# ---------------------------------------------------------------------------
# HOW
# ---------------------------------------------------------------------------
with tab_how:
    st.markdown('<div class="section-header">How It Works — Architecture</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="how-box">{lesson["how"]}</div>', unsafe_allow_html=True)
    st.caption("This is the mechanical model you should be able to draw on a whiteboard in an interview.")

# ---------------------------------------------------------------------------
# SYNTAX
# ---------------------------------------------------------------------------
with tab_syntax:
    st.markdown('<div class="section-header">Syntax & Commands Reference</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="syntax-box">{lesson["syntax"]}</div>', unsafe_allow_html=True)
    st.caption("Copy these commands. Modify them for your environment. Run them in the Demo tab to "
               "see simulated output, or try your own variant in the Practice tab.")

# ---------------------------------------------------------------------------
# DEMO — AI simulated walkthrough
# ---------------------------------------------------------------------------
with tab_demo:
    st.markdown('<div class="section-header">Live AI-Simulated Demo</div>', unsafe_allow_html=True)
    st.caption("ExaSimBot will walk through this lesson step-by-step with realistic simulated output "
               "tuned to your environment (rack size, cell count, disk groups).")

    demo_key = f"demo_{lesson_id}"
    if demo_key not in st.session_state:
        st.session_state[demo_key] = ""

    col_d1, col_d2 = st.columns([1, 5])
    with col_d1:
        run_demo = st.button("▶ Run Demo", key=f"rundemo_{lesson_id}",
                             use_container_width=True)
    with col_d2:
        if st.button("↻ Regenerate", key=f"regen_{lesson_id}"):
            st.session_state[demo_key] = ""
            run_demo = True

    if run_demo:
        client = get_client()
        if not client:
            st.error("⚠ Enter your OpenAI API key on the Home page.")
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

# ---------------------------------------------------------------------------
# PRACTICE — terminal-style input + AI evaluation
# ---------------------------------------------------------------------------
with tab_practice:
    st.markdown('<div class="section-header">Hands-On Practice Terminal</div>', unsafe_allow_html=True)
    st.caption("Type a command you think fits this lesson's task. ExaSimBot will evaluate correctness "
               "and show realistic simulated output.")

    st.markdown(f'<div class="how-box"><b>Your task:</b> {lesson["practice"]}</div>',
                unsafe_allow_html=True)

    hist_key = f"practice_hist_{lesson_id}"
    if hist_key not in st.session_state:
        st.session_state[hist_key] = []

    # Auto-choose a prompt symbol from the lesson context
    title_lc = lesson["title"].lower()
    module_lc = mod["title"].lower()
    if "cellcli" in module_lc or "cellcli" in title_lc or "flash" in title_lc:
        sym = "CellCLI>"
    elif "dcli" in module_lc:
        sym = "$"
    elif "asm" in module_lc and "asm" in title_lc:
        sym = "SQL>"
    elif "data guard" in module_lc or "dgmgrl" in title_lc or "switchover" in title_lc:
        sym = "DGMGRL>"
    elif "rman" in module_lc:
        sym = "RMAN>"
    elif "srvctl" in title_lc or "crsctl" in title_lc or "cluster" in module_lc.lower():
        sym = "$"
    else:
        sym = "SQL>"

    # Terminal display
    term_html = '<div style="background:#030a14;border:1px solid #1a4a2a;border-radius:6px;padding:14px;font-family:\'Share Tech Mono\',monospace;color:#00ff88;font-size:13px;line-height:1.6;max-height:360px;overflow-y:auto;">'
    term_html += '<div style="color:#f39c12">[ ExaSimBot Practice Terminal — type a command below ]</div><br>'
    for entry in st.session_state[hist_key][-10:]:
        term_html += f'<div><span style="color:#f39c12;font-weight:700">{entry["sym"]}</span> <span style="color:#c8dff8">{entry["cmd"]}</span></div>'
        if entry.get("out"):
            # Escape the output for HTML
            safe_out = entry["out"].replace("<", "&lt;").replace(">", "&gt;")
            term_html += f'<div style="color:#66c2ff;margin:4px 0 10px 0;white-space:pre-wrap;">{safe_out}</div>'
    term_html += f'<div><span style="color:#f39c12;font-weight:700">{sym}</span> <span style="color:#f39c12">_</span></div>'
    term_html += '</div>'
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
            st.error("⚠ Enter your OpenAI API key on the Home page.")
        else:
            try:
                eval_req = (
                    f"User typed this command for the practice task:\n"
                    f"`{cmd}`\n\n"
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

# ---------------------------------------------------------------------------
# REAL-WORLD SCENARIO
# ---------------------------------------------------------------------------
with tab_scenario:
    st.markdown('<div class="section-header">Real-World Scenario</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="real-box"><b>The situation:</b> {lesson["real_world"]}</div>',
                unsafe_allow_html=True)
    st.caption("ExaSimBot will role-play this scenario, present symptoms, and guide you through "
               "diagnosis step-by-step. You must ask questions and reason — it won't hand you the answer.")

    scn_key = f"scenario_{lesson_id}"
    if scn_key not in st.session_state:
        st.session_state[scn_key] = []

    if st.button("▶ Start Scenario", key=f"startscn_{lesson_id}"):
        client = get_client()
        if not client:
            st.error("⚠ Enter your OpenAI API key on the Home page.")
        else:
            try:
                placeholder = st.empty()
                user_msg = (
                    f"Start the scenario. Present the initial symptoms/alerts only — do NOT "
                    f"reveal the root cause. Ask me: 'What do you check first?' at the end."
                )
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

    # Show scenario conversation
    for msg in st.session_state[scn_key][1:]:  # skip the internal start message
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

# ---------------------------------------------------------------------------
# QUIZ
# ---------------------------------------------------------------------------
with tab_quiz:
    st.markdown('<div class="section-header">Knowledge Check — MCQ Quiz</div>', unsafe_allow_html=True)
    st.caption(f"3-question multiple choice quiz on: **{lesson['quiz_topic']}**. "
               "ExaSimBot scores each answer and tells you why.")

    qz_key = f"quiz_{lesson_id}"
    if qz_key not in st.session_state:
        st.session_state[qz_key] = []

    col_q1, col_q2 = st.columns([1, 4])
    with col_q1:
        if st.button("▶ Start Quiz", key=f"startqz_{lesson_id}", use_container_width=True):
            st.session_state[qz_key] = []
            client = get_client()
            if not client:
                st.error("⚠ Enter your OpenAI API key on the Home page.")
            else:
                try:
                    placeholder = st.empty()
                    out = stream_response(
                        client,
                        [
                            {"role": "system", "content": system_prompt(lesson, "quiz")},
                            {"role": "user", "content": f"Start the quiz. Ask question 1 of 3 on the topic: {lesson['quiz_topic']}. Present only Q1 with 4 options A/B/C/D. Wait for my answer."},
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

# ---------------------------------------------------------------------------
# FREE CHAT
# ---------------------------------------------------------------------------
with tab_chat:
    st.markdown('<div class="section-header">Ask ExaSimBot Anything</div>', unsafe_allow_html=True)
    st.caption("Free-form chat scoped to this lesson. Ask follow-up questions, request deeper dives, "
               "or get clarification on any command.")

    for msg in st.session_state.chat[lesson_id]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_q = st.chat_input("Ask about this lesson...", key=f"chat_in_{lesson_id}")
    if user_q:
        client = get_client()
        if not client:
            st.error("⚠ Enter your OpenAI API key on the Home page.")
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
