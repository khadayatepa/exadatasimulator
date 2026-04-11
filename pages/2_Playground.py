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

PROMPT_CONTEXTS = ["CellCLI>", "SQL>", "$", "RMAN>", "DGMGRL>", "asmcmd>", "#"]

def get_ex(ex_id):
    for ex in PLAYGROUND_EXERCISES:
        if ex["id"] == ex_id:
            return ex
    return None

def h(s):
    """HTML-escape a string for safe embedding in HTML text nodes."""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

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
attempted  = len({hh["id"] for hh in st.session_state.pg_history})
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
# WORKSPACE — shown FIRST when an exercise is selected
# ─────────────────────────────────────────────────────────────────────────────

ex_id = st.session_state.pg_ex_id
if ex_id:
    ex = get_ex(ex_id)
    if ex:
        cat_meta = CATEGORIES.get(ex["category"], {"icon": "•", "color": "#c8dff8"})
        hist_key = f"pg_term_{ex_id}"
        if hist_key not in st.session_state:
            st.session_state[hist_key] = []

        st.markdown(
            f'<div class="section-header">{cat_meta["icon"]} Workspace — '
            f'{h(ex["id"])}: {h(ex["title"])}</div>',
            unsafe_allow_html=True,
        )

        # ── Info + hints ────────────────────────────────────────────────────
        info_col, ctrl_col = st.columns([3, 1])
        with info_col:
            st.markdown(
                f'<div class="real-box"><b>Scenario:</b><br>{h(ex["scenario"])}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="how-box" style="margin-top:8px;">'
                f'<b>Task:</b> {h(ex["task"])}</div>',
                unsafe_allow_html=True,
            )
            # Hints
            hints_shown = st.session_state.pg_hints_shown.get(ex_id, 0)
            h1c, h2c = st.columns(2)
            with h1c:
                if hints_shown < 1:
                    if st.button("💡 Hint 1  (−2 pts)", key=f"h1_{ex_id}",
                                 use_container_width=True):
                        st.session_state.pg_hints_shown[ex_id] = 1
                        st.rerun()
                else:
                    st.markdown(
                        f'<div class="why-box" style="font-size:12px;">'
                        f'<b>Hint 1:</b> {h(ex["hints"][0])}</div>',
                        unsafe_allow_html=True,
                    )
            with h2c:
                if len(ex["hints"]) > 1:
                    if hints_shown < 2:
                        if st.button("💡 Hint 2  (−2 pts)", key=f"h2_{ex_id}",
                                     use_container_width=True,
                                     disabled=(hints_shown < 1)):
                            st.session_state.pg_hints_shown[ex_id] = 2
                            st.rerun()
                    else:
                        st.markdown(
                            f'<div class="why-box" style="font-size:12px;">'
                            f'<b>Hint 2:</b> {h(ex["hints"][1])}</div>',
                            unsafe_allow_html=True,
                        )

        with ctrl_col:
            hints_used = st.session_state.pg_hints_shown.get(ex_id, 0)
            max_pts    = max(10 - hints_used * 2, 2)
            tags_html  = " ".join(
                f'<span style="background:#1a2c47;color:#6a8faa;font-size:10px;'
                f'padding:2px 8px;border-radius:8px;margin:2px 2px 2px 0;'
                f'display:inline-block;">{h(t)}</span>'
                for t in ex.get("tags", [])
            )
            st.markdown(f'''
            <div style="background:#0a1220;border:1px solid #1a2c47;
                 border-radius:6px;padding:12px;">
              <div style="color:#f39c12;font-size:11px;letter-spacing:1px;
                   margin-bottom:10px;">EXERCISE INFO</div>
              <div class="metric-pill">ID <span class="v">{h(ex["id"])}</span></div>
              <div class="metric-pill">Level <span class="v">{h(ex["level"])}</span></div>
              <div class="metric-pill">Max pts <span class="v">{max_pts}</span></div>
              <div style="margin-top:10px;line-height:2.2;">{tags_html}</div>
            </div>
            ''', unsafe_allow_html=True)

        # ── Prompt context dropdown ──────────────────────────────────────────
        st.markdown('<div style="margin-top:14px;"></div>', unsafe_allow_html=True)
        ctx_col, _ = st.columns([2, 8])
        with ctx_col:
            default_idx = (
                PROMPT_CONTEXTS.index(ex["context"])
                if ex["context"] in PROMPT_CONTEXTS else 0
            )
            sym = st.selectbox(
                "Prompt context",
                PROMPT_CONTEXTS,
                index=default_idx,
                key=f"pg_ctx_{ex_id}",
                help="Select the shell/tool prompt matching this exercise. "
                     "Defaults to the exercise's expected context.",
            )
        sym_h = h(sym)   # HTML-safe version: CellCLI> → CellCLI&gt;

        # ── Terminal display ─────────────────────────────────────────────────
        term_lines = (
            f'<div style="background:#030a14;border:1px solid #1a4a2a;border-radius:6px;'
            f'padding:14px;font-family:\'Share Tech Mono\',monospace;color:#00ff88;'
            f'font-size:13px;line-height:1.7;max-height:360px;overflow-y:auto;">'
            f'<div style="color:#f39c12">[ ExaSimBot Playground Terminal — {h(ex["id"])} ]'
            f'</div><br>'
        )
        for entry in st.session_state[hist_key][-12:]:
            safe_cmd  = h(entry["cmd"])
            entry_sym = h(entry["sym"])
            term_lines += (
                f'<div><span style="color:#f39c12;font-weight:700">{entry_sym}</span> '
                f'<span style="color:#c8dff8">{safe_cmd}</span></div>'
            )
            if entry.get("out"):
                # Strip the VERDICT: line from display output
                display_out = "\n".join(
                    l for l in entry["out"].split("\n")
                    if not l.strip().startswith("VERDICT:")
                ).strip()
                safe_out = h(display_out)
                term_lines += (
                    f'<div style="color:#66c2ff;margin:4px 0 4px 0;'
                    f'white-space:pre-wrap;">{safe_out}</div>'
                )
            if entry.get("verdict"):
                v  = entry["verdict"]
                vc = "#00ff88" if "CORRECT" in v else ("#f39c12" if "PARTIAL" in v else "#ff6b6b")
                pts_label = f" (+{entry.get('pts', 0)} pts)" if entry.get("pts") else ""
                term_lines += (
                    f'<div style="color:{vc};font-weight:700;margin-bottom:12px;">'
                    f'{h(v)}{h(pts_label)}</div>'
                )
        term_lines += (
            f'<div><span style="color:#f39c12;font-weight:700">{sym_h}</span> '
            f'<span style="color:#f39c12">▌</span></div></div>'
        )
        st.markdown(term_lines, unsafe_allow_html=True)

        # ── Command input row ────────────────────────────────────────────────
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

        # ── AI Evaluation ────────────────────────────────────────────────────
        if eval_btn and cmd:
            client = get_client()
            if not client:
                st.error("⚠ Enter your OpenAI API key on the Home page and click Validate.")
            else:
                hints_used = st.session_state.pg_hints_shown.get(ex_id, 0)
                eval_prompt = (
                    f"Exercise: {ex['id']} — {ex['title']}\n"
                    f"Category: {ex['category']} | Level: {ex['level']}\n"
                    f"Scenario: {ex['scenario']}\n"
                    f"Task: {ex['task']}\n"
                    f"Reference correct command(s): {ex['ref_command']}\n\n"
                    f"User typed: `{cmd}`\n"
                    f"Hints used: {hints_used}\n\n"
                    f"In ≤130 words:\n"
                    f"1. Show realistic Exadata/Oracle terminal output for the typed command.\n"
                    f"2. Evaluate: CORRECT = exact or equivalent, "
                    f"PARTIAL = right idea but incomplete/minor error, WRONG = incorrect.\n"
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

                        # Keep best score on retry
                        prev = st.session_state.pg_result.get(ex_id)
                        if not prev or pts >= prev.get("pts", 0):
                            st.session_state.pg_result[ex_id] = {
                                "verdict": verdict,
                                "feedback": output,
                                "pts": pts,
                                "correct_cmd": ex["ref_command"],
                            }

                        # Category scores
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

                        st.session_state.pg_history.append({
                            "id": ex_id, "cmd": cmd, "verdict": verdict,
                            "pts": pts, "ts": datetime.now().strftime("%H:%M:%S"),
                        })
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
                {h(v)} &nbsp;— &nbsp;{result["pts"]} pts earned
              </div>
              <div style="color:#f39c12;font-size:11px;letter-spacing:1px;margin-bottom:4px;">
                REFERENCE COMMAND
              </div>
              <div class="syntax-box" style="font-size:12px;margin-bottom:12px;">{h(result["correct_cmd"])}</div>
              <div style="background:#0a1a0a;border-left:3px solid #00ff88;padding:10px;
                   border-radius:4px;color:#a0d0a0;font-size:13px;line-height:1.6;">
                <b>Explanation:</b> {h(ex["explanation"])}
              </div>
            </div>
            ''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# BROWSE EXERCISES  (below workspace so it doesn't push content down)
# ─────────────────────────────────────────────────────────────────────────────

browse_label = "Browse Exercises" if not ex_id else "Change Exercise"
st.markdown(f'<div class="section-header">{browse_label}</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns([2, 1.5, 3])
with f1:
    sel_cat = st.selectbox("Category", ["All"] + list(CATEGORIES.keys()), key="pg_cat_filter")
with f2:
    sel_level = st.selectbox("Level", ["All"] + LEVELS, key="pg_level_filter")
with f3:
    search_term = st.text_input(
        "Search", placeholder="Search by title or tag (e.g. flashcache, asm, rman)…",
        key="pg_search", label_visibility="collapsed",
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
                    badge = '<span style="color:#00ff88;font-size:10px;font-weight:700"> ✓</span>'
                elif "PARTIAL" in v:
                    badge = '<span style="color:#f39c12;font-size:10px;font-weight:700"> ~</span>'
                else:
                    badge = '<span style="color:#e74c3c;font-size:10px;font-weight:700"> ✗</span>'
            else:
                badge = ""

            border = cat_meta["color"] if is_sel else "#1a2c47"
            with col:
                st.markdown(f'''
                <div style="background:#0f1a2e;border:1px solid {border};
                     border-left:3px solid {cat_meta["color"]};border-radius:6px;
                     padding:10px;margin-bottom:4px;min-height:90px;">
                  <div style="color:{cat_meta["color"]};font-size:10px;letter-spacing:1px;">
                    {cat_meta["icon"]} {h(ex["category"])}{badge}
                  </div>
                  <div style="color:#f39c12;font-family:\'Share Tech Mono\',monospace;
                       font-size:11px;margin:3px 0;">{h(ex["id"])}</div>
                  <div style="color:#c8dff8;font-size:12px;font-weight:600;
                       margin-bottom:4px;">{h(ex["title"])}</div>
                  <span class="level-{ex["level"]}">{ex["level"]}</span>
                </div>
                ''', unsafe_allow_html=True)
                if st.button("Open", key=f"pgsel_{ex['id']}", use_container_width=True):
                    st.session_state.pg_ex_id = ex["id"]
                    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# SCOREBOARD
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.pg_scores:
    st.markdown('<div class="section-header">Progress by Category</div>', unsafe_allow_html=True)
    score_cols = st.columns(max(len(st.session_state.pg_scores), 1))
    for col, (cat, scores) in zip(score_cols, st.session_state.pg_scores.items()):
        cat_meta = CATEGORIES.get(cat, {"icon": "•", "color": "#c8dff8"})
        with col:
            st.markdown(f'''
            <div style="background:#0f1a2e;border:1px solid #1a2c47;
                 border-left:3px solid {cat_meta["color"]};border-radius:6px;
                 padding:12px;text-align:center;">
              <div style="color:{cat_meta["color"]};font-size:20px;margin-bottom:4px;">
                {cat_meta["icon"]}
              </div>
              <div style="color:#c8dff8;font-size:10px;letter-spacing:1px;">{h(cat)}</div>
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
# RECENT ATTEMPTS LOG
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.pg_history:
    st.markdown('<div class="section-header">Recent Attempts</div>', unsafe_allow_html=True)
    for entry in reversed(st.session_state.pg_history[-15:]):
        ex_e  = get_ex(entry["id"])
        title = ex_e["title"] if ex_e else entry["id"]
        v     = entry["verdict"]
        vc    = "#00ff88" if "CORRECT" in v else ("#f39c12" if "PARTIAL" in v else "#e74c3c")
        cmd_display = entry["cmd"][:50] + ("…" if len(entry["cmd"]) > 50 else "")
        st.markdown(f'''
        <div style="background:#0f1a2e;border-left:3px solid {vc};border-radius:4px;
             padding:8px 14px;margin:4px 0;font-family:\'Share Tech Mono\',monospace;
             font-size:12px;display:flex;gap:20px;flex-wrap:wrap;">
          <span style="color:#f39c12;white-space:nowrap;">{h(entry["ts"])}</span>
          <span style="color:#c8dff8;white-space:nowrap;">{h(entry["id"])} — {h(title)}</span>
          <span style="color:#8ab4d8;font-style:italic;">{h(cmd_display)}</span>
          <span style="color:{vc};font-weight:700;white-space:nowrap;">{h(v)} +{entry["pts"]}pts</span>
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
