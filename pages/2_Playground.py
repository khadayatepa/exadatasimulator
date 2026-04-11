"""
pages/2_Playground.py — DBA Playground
50 hands-on exercises across 8 categories (Basic → Advanced).
AI-evaluated commands with score tracking, hints, and explanations.
"""
import streamlit as st
import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exasim_core import GLOBAL_CSS, init_state, get_client, RACK_SPECS
from playground_data import PLAYGROUND_EXERCISES, CATEGORIES, LEVELS

st.set_page_config(
    page_title="DBA Playground",
    page_icon="⌨",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
init_state()

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def get_ex(ex_id):
    for ex in PLAYGROUND_EXERCISES:
        if ex["id"] == ex_id:
            return ex
    return None

EVAL_SYS = (
    "You are ExaSimBot evaluating a DBA playground command exercise on Oracle Exadata X8M. "
    "Be strict but fair. Always show realistic Exadata terminal output for the typed command "
    "(even if wrong — show what would actually happen). "
    "End your response with exactly one of these three lines:\n"
    "VERDICT: CORRECT\n"
    "VERDICT: PARTIAL\n"
    "VERDICT: WRONG"
)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────

col_back, col_title = st.columns([1, 7])
with col_back:
    if st.button("← Home", use_container_width=True):
        st.switch_page("app.py")
with col_title:
    st.markdown("""
    <div style="border-bottom:1px solid #1a2c47;padding-bottom:10px;">
      <div class="brand-title">⌨ DBA PLAYGROUND — 50 HANDS-ON EXERCISES</div>
      <div class="brand-sub">COMMAND PRACTICE • AI-EVALUATED • SCORE TRACKING • 8 CATEGORIES • BASIC → ADVANCED</div>
    </div>
    """, unsafe_allow_html=True)

# Score strip
total_pts  = st.session_state.pg_total_pts
attempted  = len({h["id"] for h in st.session_state.pg_history})
correct_ct = sum(1 for r in st.session_state.pg_result.values() if "CORRECT" in r.get("verdict", ""))
st.markdown(f'''
<div style="margin:10px 0 16px 0;">
  <div class="metric-pill">Total Points <span class="v">{total_pts}</span></div>
  <div class="metric-pill">Attempted <span class="v">{attempted} / 50</span></div>
  <div class="metric-pill">Correct <span class="v">{correct_ct}</span></div>
  <div class="metric-pill">Model <span class="v">{st.session_state.openai_model}</span></div>
</div>
''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FILTER BAR
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<div class="section-header">Browse Exercises</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns([2, 1.5, 3])
with f1:
    sel_cat = st.selectbox("Category", ["All"] + list(CATEGORIES.keys()), key="pg_cat_filter")
with f2:
    sel_level = st.selectbox("Level", ["All"] + LEVELS, key="pg_level_filter")
with f3:
    search_term = st.text_input(
        "Search", placeholder="Search by title or tag (e.g. flashcache, asm, rman)…",
        key="pg_search", label_visibility="collapsed"
    )

# Apply filters
filtered = PLAYGROUND_EXERCISES
if sel_cat != "All":
    filtered = [e for e in filtered if e["category"] == sel_cat]
if sel_level != "All":
    filtered = [e for e in filtered if e["level"] == sel_level]
if search_term:
    q = search_term.lower()
    filtered = [
        e for e in filtered
        if q in e["title"].lower() or any(q in t for t in e.get("tags", []))
    ]

# ─────────────────────────────────────────────────────────────────────────────
# EXERCISE GRID
# ─────────────────────────────────────────────────────────────────────────────

if not filtered:
    st.info("No exercises match the current filters.")
else:
    for row_start in range(0, len(filtered), 4):
        row_exs = filtered[row_start : row_start + 4]
        cols = st.columns(4)
        for col, ex in zip(cols, row_exs):
            cat_meta = CATEGORIES.get(ex["category"], {"icon": "•", "color": "#c8dff8"})
            result   = st.session_state.pg_result.get(ex["id"])
            is_sel   = st.session_state.pg_ex_id == ex["id"]

            if result:
                v = result.get("verdict", "")
                if "CORRECT" in v:
                    badge = '<span style="color:#00ff88;font-size:10px;font-weight:700"> ✓ DONE</span>'
                elif "PARTIAL" in v:
                    badge = '<span style="color:#f39c12;font-size:10px;font-weight:700"> ~ PARTIAL</span>'
                else:
                    badge = '<span style="color:#e74c3c;font-size:10px;font-weight:700"> ✗ WRONG</span>'
            else:
                badge = ""

            border = cat_meta["color"] if is_sel else "#1a2c47"
            with col:
                st.markdown(f'''
                <div style="background:#0f1a2e;border:1px solid {border};
                     border-left:3px solid {cat_meta["color"]};border-radius:6px;
                     padding:10px;margin-bottom:4px;min-height:95px;">
                  <div style="font-size:10px;color:{cat_meta["color"]};
                       letter-spacing:1px;margin-bottom:4px;">
                    {cat_meta["icon"]} {ex["category"]}{badge}
                  </div>
                  <div style="color:#f39c12;font-family:\'Share Tech Mono\',monospace;
                       font-size:11px;">{ex["id"]}</div>
                  <div style="color:#c8dff8;font-size:12px;font-weight:600;
                       margin:3px 0 4px 0;">{ex["title"]}</div>
                  <span class="level-{ex["level"]}">{ex["level"]}</span>
                </div>
                ''', unsafe_allow_html=True)
                if st.button("Open", key=f"pgsel_{ex['id']}", use_container_width=True):
                    st.session_state.pg_ex_id = ex["id"]
                    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# EXERCISE WORKSPACE
# ─────────────────────────────────────────────────────────────────────────────

ex_id = st.session_state.pg_ex_id
if ex_id:
    ex = get_ex(ex_id)
    if not ex:
        st.warning("Exercise not found.")
    else:
        cat_meta   = CATEGORIES.get(ex["category"], {"icon": "•", "color": "#c8dff8"})
        sym        = ex["context"]
        hist_key   = f"pg_term_{ex_id}"
        if hist_key not in st.session_state:
            st.session_state[hist_key] = []

        st.markdown(
            f'<div class="section-header">{cat_meta["icon"]} Workspace — '
            f'{ex["id"]}: {ex["title"]}</div>',
            unsafe_allow_html=True,
        )

        info_col, meta_col = st.columns([3, 1])
        with info_col:
            st.markdown(
                f'<div class="real-box"><b>Scenario:</b><br>{ex["scenario"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="how-box" style="margin-top:8px;">'
                f'<b>Task:</b> {ex["task"]}</div>',
                unsafe_allow_html=True,
            )

            # Hints
            hints_shown = st.session_state.pg_hints_shown.get(ex_id, 0)
            h1_col, h2_col = st.columns(2)
            with h1_col:
                if hints_shown < 1:
                    if st.button("💡 Reveal Hint 1  (−2 pts)", key=f"h1_{ex_id}",
                                 use_container_width=True):
                        st.session_state.pg_hints_shown[ex_id] = 1
                        st.rerun()
                else:
                    st.markdown(
                        f'<div class="why-box" style="font-size:12px;">'
                        f'<b>Hint 1:</b> {ex["hints"][0]}</div>',
                        unsafe_allow_html=True,
                    )
            with h2_col:
                if len(ex["hints"]) > 1:
                    if hints_shown < 2:
                        if st.button("💡 Reveal Hint 2  (−2 pts)", key=f"h2_{ex_id}",
                                     use_container_width=True,
                                     disabled=(hints_shown < 1)):
                            st.session_state.pg_hints_shown[ex_id] = 2
                            st.rerun()
                    else:
                        st.markdown(
                            f'<div class="why-box" style="font-size:12px;">'
                            f'<b>Hint 2:</b> {ex["hints"][1]}</div>',
                            unsafe_allow_html=True,
                        )

        with meta_col:
            tags_html = " ".join(
                f'<span style="background:#1a2c47;color:#6a8faa;font-size:10px;'
                f'padding:2px 8px;border-radius:8px;margin:2px 2px 2px 0;'
                f'display:inline-block;">{t}</span>'
                for t in ex.get("tags", [])
            )
            hints_used = st.session_state.pg_hints_shown.get(ex_id, 0)
            max_pts    = max(10 - hints_used * 2, 2)
            st.markdown(f'''
            <div style="background:#0a1220;border:1px solid #1a2c47;
                 border-radius:6px;padding:12px;">
              <div style="color:#f39c12;font-size:11px;letter-spacing:1px;
                   margin-bottom:10px;">EXERCISE DETAILS</div>
              <div class="metric-pill">ID <span class="v">{ex["id"]}</span></div>
              <div class="metric-pill">Prompt <span class="v">{sym}</span></div>
              <div class="metric-pill">Max pts <span class="v">{max_pts}</span></div>
              <br><br>
              <div style="margin-top:8px;line-height:2;">{tags_html}</div>
            </div>
            ''', unsafe_allow_html=True)

        # ── Terminal display ──────────────────────────────────────────────────
        term_lines = (
            f'<div style="background:#030a14;border:1px solid #1a4a2a;border-radius:6px;'
            f'padding:14px;font-family:\'Share Tech Mono\',monospace;color:#00ff88;'
            f'font-size:13px;line-height:1.7;max-height:380px;overflow-y:auto;">'
            f'<div style="color:#f39c12">[ ExaSimBot Playground Terminal — {ex["id"]} ]'
            f'</div><br>'
        )
        for entry in st.session_state[hist_key][-12:]:
            safe_cmd = entry["cmd"].replace("<", "&lt;").replace(">", "&gt;")
            term_lines += (
                f'<div><span style="color:#f39c12;font-weight:700">{entry["sym"]}</span> '
                f'<span style="color:#c8dff8">{safe_cmd}</span></div>'
            )
            if entry.get("out"):
                safe_out = entry["out"].replace("<", "&lt;").replace(">", "&gt;")
                # strip the verdict line from the displayed output
                display_out = "\n".join(
                    l for l in safe_out.split("\n") if not l.startswith("VERDICT:")
                ).strip()
                term_lines += (
                    f'<div style="color:#66c2ff;margin:4px 0 4px 0;'
                    f'white-space:pre-wrap;">{display_out}</div>'
                )
            if entry.get("verdict"):
                v = entry["verdict"]
                vc = "#00ff88" if "CORRECT" in v else ("#f39c12" if "PARTIAL" in v else "#ff6b6b")
                pts_str = f" (+{entry.get('pts',0)} pts)" if entry.get("pts") else ""
                term_lines += (
                    f'<div style="color:{vc};font-weight:700;margin-bottom:12px;">'
                    f'{v}{pts_str}</div>'
                )
        term_lines += (
            f'<div><span style="color:#f39c12;font-weight:700">{sym}</span> '
            f'<span style="color:#f39c12">▌</span></div></div>'
        )
        st.markdown(term_lines, unsafe_allow_html=True)

        # ── Command input row ─────────────────────────────────────────────────
        tc1, tc2, tc3 = st.columns([5, 1, 1])
        with tc1:
            cmd = st.text_input(
                "cmd", key=f"pgcmd_{ex_id}",
                placeholder=f"{sym}  type your command here…",
                label_visibility="collapsed",
            )
        with tc2:
            eval_btn = st.button("Evaluate", key=f"pgeval_{ex_id}", use_container_width=True)
        with tc3:
            clear_btn = st.button("Clear", key=f"pgclr_{ex_id}", use_container_width=True)

        if clear_btn:
            st.session_state[hist_key] = []
            st.rerun()

        # ── Evaluate ─────────────────────────────────────────────────────────
        if eval_btn and cmd:
            client = get_client()
            if not client:
                st.error("⚠ Enter your OpenAI API key on the Home page.")
            else:
                hints_used = st.session_state.pg_hints_shown.get(ex_id, 0)
                eval_prompt = (
                    f"Exercise: {ex['id']} — {ex['title']}\n"
                    f"Category: {ex['category']} | Level: {ex['level']}\n"
                    f"Scenario: {ex['scenario']}\n"
                    f"Task: {ex['task']}\n"
                    f"Reference correct command(s): {ex['ref_command']}\n\n"
                    f"User typed: `{cmd}`\n"
                    f"Hints used by user: {hints_used}\n\n"
                    f"In ≤130 words:\n"
                    f"1. Show realistic Exadata/Oracle terminal output for the typed command.\n"
                    f"2. Evaluate correctness (CORRECT = exact or equivalent, "
                    f"PARTIAL = right direction but incomplete/minor error, WRONG = incorrect).\n"
                    f"3. If not CORRECT, show the reference command.\n"
                    f"End with exactly one of:\nVERDICT: CORRECT\nVERDICT: PARTIAL\nVERDICT: WRONG"
                )
                with st.spinner("ExaSimBot evaluating…"):
                    try:
                        resp = client.chat.completions.create(
                            model=st.session_state.openai_model,
                            messages=[
                                {"role": "system", "content": EVAL_SYS},
                                {"role": "user",   "content": eval_prompt},
                            ],
                            max_tokens=500,
                            temperature=0.2,
                        )
                        output = resp.choices[0].message.content

                        # Parse verdict
                        if "VERDICT: CORRECT" in output:
                            verdict = "CORRECT ✓"
                            pts     = max(10 - hints_used * 2, 2)
                        elif "VERDICT: PARTIAL" in output:
                            verdict = "PARTIAL ~"
                            pts     = max(5 - hints_used, 1)
                        else:
                            verdict = "WRONG ✗"
                            pts     = 0

                        # Persist result (keep best score if re-attempted)
                        prev = st.session_state.pg_result.get(ex_id)
                        if not prev or pts >= prev.get("pts", 0):
                            st.session_state.pg_result[ex_id] = {
                                "verdict": verdict,
                                "feedback": output,
                                "pts": pts,
                                "correct_cmd": ex["ref_command"],
                            }

                        # Update category scores
                        cat = ex["category"]
                        if cat not in st.session_state.pg_scores:
                            st.session_state.pg_scores[cat] = {
                                "correct": 0, "partial": 0, "wrong": 0, "pts": 0
                            }
                        if "CORRECT" in verdict:
                            st.session_state.pg_scores[cat]["correct"] += 1
                        elif "PARTIAL" in verdict:
                            st.session_state.pg_scores[cat]["partial"] += 1
                        else:
                            st.session_state.pg_scores[cat]["wrong"] += 1
                        st.session_state.pg_scores[cat]["pts"] += pts
                        st.session_state.pg_total_pts += pts

                        # History log
                        st.session_state.pg_history.append({
                            "id": ex_id, "cmd": cmd, "verdict": verdict,
                            "pts": pts,
                            "ts": datetime.now().strftime("%H:%M:%S"),
                        })

                        # Terminal history entry
                        st.session_state[hist_key].append({
                            "sym": sym, "cmd": cmd,
                            "out": output, "verdict": verdict, "pts": pts,
                        })
                        st.rerun()

                    except Exception as e:
                        st.error(f"OpenAI error: {e}")

        # ── Result panel ─────────────────────────────────────────────────────
        result = st.session_state.pg_result.get(ex_id)
        if result:
            v  = result.get("verdict", "")
            vc = "#00ff88" if "CORRECT" in v else ("#f39c12" if "PARTIAL" in v else "#e74c3c")
            st.markdown(f'''
            <div style="background:#0a1220;border:1px solid #1a2c47;border-radius:6px;
                 padding:14px;margin-top:12px;">
              <div style="color:{vc};font-size:14px;font-weight:700;margin-bottom:10px;">
                {v} &nbsp;—&nbsp; {result["pts"]} pts earned
              </div>
              <div style="color:#f39c12;font-size:11px;letter-spacing:1px;margin-bottom:4px;">
                REFERENCE COMMAND
              </div>
              <div class="syntax-box" style="font-size:12px;margin-bottom:12px;">{result["correct_cmd"]}</div>
              <div style="background:#0a1a0a;border-left:3px solid #00ff88;padding:10px;
                   border-radius:4px;color:#a0d0a0;font-size:13px;line-height:1.6;">
                <b>Explanation:</b> {ex["explanation"]}
              </div>
            </div>
            ''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCOREBOARD
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.pg_scores:
    st.markdown('<div class="section-header">Progress by Category</div>', unsafe_allow_html=True)
    n_cats = len(st.session_state.pg_scores)
    score_cols = st.columns(max(n_cats, 1))
    for col, (cat, scores) in zip(score_cols, st.session_state.pg_scores.items()):
        cat_meta = CATEGORIES.get(cat, {"icon": "•", "color": "#c8dff8"})
        with col:
            st.markdown(f'''
            <div style="background:#0f1a2e;border:1px solid #1a2c47;
                 border-left:3px solid {cat_meta["color"]};border-radius:6px;
                 padding:12px;text-align:center;">
              <div style="color:{cat_meta["color"]};font-size:22px;margin-bottom:4px;">
                {cat_meta["icon"]}
              </div>
              <div style="color:#c8dff8;font-size:10px;letter-spacing:1px;">{cat}</div>
              <div style="color:#00ff88;font-size:20px;font-weight:700;margin:4px 0;">
                {scores["pts"]} pts
              </div>
              <div style="color:#8ab4d8;font-size:11px;">
                <span style="color:#00ff88">✓{scores["correct"]}</span>
                &nbsp;
                <span style="color:#f39c12">~{scores["partial"]}</span>
                &nbsp;
                <span style="color:#e74c3c">✗{scores["wrong"]}</span>
              </div>
            </div>
            ''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# RECENT HISTORY LOG
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.pg_history:
    st.markdown('<div class="section-header">Recent Attempts</div>', unsafe_allow_html=True)
    rows = list(reversed(st.session_state.pg_history[-15:]))
    for entry in rows:
        ex_e = get_ex(entry["id"])
        title = ex_e["title"] if ex_e else entry["id"]
        v   = entry["verdict"]
        vc  = "#00ff88" if "CORRECT" in v else ("#f39c12" if "PARTIAL" in v else "#e74c3c")
        st.markdown(f'''
        <div style="background:#0f1a2e;border-left:3px solid {vc};border-radius:4px;
             padding:8px 14px;margin:4px 0;font-family:\'Share Tech Mono\',monospace;
             font-size:12px;display:flex;justify-content:space-between;">
          <span style="color:#f39c12">{entry["ts"]}</span>
          <span style="color:#c8dff8">{entry["id"]} — {title}</span>
          <span style="color:#8ab4d8;font-style:italic;">{entry["cmd"][:50]}…</span>
          <span style="color:{vc};font-weight:700">{v} +{entry["pts"]}pts</span>
        </div>
        ''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center;color:#6a8faa;font-size:11px;letter-spacing:2px;
            margin-top:30px;padding:14px;border-top:1px solid #1a2c47;">
EXADATA X8M DBA PLAYGROUND • 50 EXERCISES • AI-EVALUATED BY EXASIMBOT<br>
PRASHANT | ORACLE ACE (APPRENTICE) | PRASHANTORACLEDBA.WORDPRESS.COM
</div>
""", unsafe_allow_html=True)
