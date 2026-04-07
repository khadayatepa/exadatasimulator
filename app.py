"""
Home page — Oracle Exadata X8M Lab Simulator
Shows: config bar, live architecture diagram, curriculum modules, lesson catalog.
Clicking a lesson opens the Lesson page (pages/1_Lesson.py).
"""
import streamlit as st
from exasim_core import (
    RACK_SPECS, CURRICULUM, GLOBAL_CSS, init_state, build_diagram
)

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
