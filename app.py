"""
Oracle Exadata X8M DBA/DMA Lab Simulator
=========================================
Author : Prashant | Oracle ACE (Apprentice) | Database Architect
Blog   : prashantoracledba.wordpress.com
Stack  : Streamlit + OpenAI (GPT-4o)

Self-contained: only imports streamlit and openai.
All lab data lives inline in LAB_CATALOG.
"""

import streamlit as st
from openai import OpenAI

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Exadata X8M Simulator",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# GLOBAL CSS — Mission-control dark theme
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap');

.stApp {
    background: radial-gradient(ellipse at top, #081424 0%, #04080f 100%);
    color: #c8dff8;
    font-family: 'Rajdhani', sans-serif;
}
h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 1.5px; }
.brand-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 28px; font-weight: 700; letter-spacing: 3px;
    background: linear-gradient(90deg, #e74c3c, #f39c12);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.brand-sub { color: #6a8faa; font-size: 13px; letter-spacing: 2px; }
.panel {
    background: #0a1220; border: 1px solid #1a2c47; border-radius: 10px;
    padding: 16px; margin-bottom: 14px;
}
.panel-title {
    font-family: 'Orbitron', sans-serif; color: #f39c12;
    font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
    border-bottom: 1px solid #1a2c47; padding-bottom: 6px; margin-bottom: 10px;
}
.terminal {
    background: #030a14; border: 1px solid #1a4a2a; border-radius: 6px;
    padding: 14px; font-family: 'Share Tech Mono', monospace;
    color: #00ff88; font-size: 13px; line-height: 1.55;
    max-height: 420px; overflow-y: auto;
    box-shadow: inset 0 0 40px rgba(0,255,136,0.05);
}
.terminal .prompt { color: #f39c12; font-weight: 700; }
.terminal .cmd { color: #c8dff8; }
.terminal .ai { color: #66c2ff; }
.metric-pill {
    display: inline-block; background: #0f1a2e; border: 1px solid #1a2c47;
    padding: 4px 10px; border-radius: 12px; font-family: 'Share Tech Mono', monospace;
    font-size: 11px; color: #c8dff8; margin-right: 6px;
}
.metric-pill .v { color: #00ff88; font-weight: 700; }
.lab-card {
    background: #0f1a2e; border-left: 3px solid #f39c12;
    padding: 10px 14px; border-radius: 4px; margin: 6px 0; font-size: 13px;
}
.lab-card .id { color: #f39c12; font-family: 'Share Tech Mono', monospace; font-weight: 700; }
.lab-card .ttl { color: #c8dff8; font-weight: 600; }
.tag-demo { background:#0088ff22; color:#66c2ff; padding:1px 8px; border-radius:8px; font-size:10px; }
.tag-lab  { background:#00ff8822; color:#00ff88; padding:1px 8px; border-radius:8px; font-size:10px; }
.tag-quiz { background:#f39c1222; color:#f39c12; padding:1px 8px; border-radius:8px; font-size:10px; }
div[data-testid="stSelectbox"] label, div[data-testid="stTextInput"] label {
    color: #6a8faa !important; font-size: 11px !important;
    text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600;
}
.stButton > button {
    background: linear-gradient(90deg, #c0392b, #e74c3c);
    color: white; border: none; font-family: 'Rajdhani', sans-serif;
    font-weight: 700; letter-spacing: 1px; border-radius: 6px;
}
.stButton > button:hover { background: linear-gradient(90deg, #e74c3c, #f39c12); }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# RACK MODEL SPECS
# =============================================================================
RACK_SPECS = {
    "Eighth Rack": {"compute": 2, "cells": 3, "ib": 2},
    "Quarter Rack": {"compute": 2, "cells": 3, "ib": 2},
    "Half Rack":    {"compute": 4, "cells": 7, "ib": 2},
    "Full Rack":    {"compute": 8, "cells": 14, "ib": 3},
}

X8M_SPECS_TEXT = """
COMPUTE NODE (X8M-2): 2x Xeon 8260 = 48 cores, up to 1.5TB DDR4,
3.2TB Optane PMEM, 2x200Gb IB HDR, Oracle Linux 8.
STORAGE CELL (X8M-2): 12x7.2TB HDD = 86.4TB, 4x6.4TB NVMe = 25.6TB,
1.5TB PMEM write-back, 2x200Gb IB HDR, cellsrv/MS/RS.
IB FABRIC: 200 Gb/s HDR, fat-tree, RDMA sub-microsecond.
"""

# =============================================================================
# LAB CATALOG (representative labs — expand as needed up to 105)
# =============================================================================
LAB_CATALOG = {
    "L1 — Basic Operations": [
        {"id": 1, "title": "Create a PDB", "tag": "demo",
         "obj": "Create a new pluggable database from seed",
         "scenario": "Dev team needs a fresh PDB called DEVPDB for testing.",
         "tasks": ["Connect to CDB$ROOT", "CREATE PLUGGABLE DATABASE DEVPDB", "Open PDB read write"],
         "validation": "SELECT name, open_mode FROM v$pdbs;"},
        {"id": 2, "title": "Check Cluster Status", "tag": "lab",
         "obj": "Verify RAC cluster is healthy across all compute nodes",
         "scenario": "Morning health check — confirm CRS, cluster, and DB resources are online.",
         "tasks": ["Run crsctl check cluster -all", "Run srvctl status database -d ORCL", "Check asmcmd lsdg"],
         "validation": "All instances ONLINE, no offline resources in crsctl stat res -t."},
        {"id": 3, "title": "List Exadata Cells", "tag": "demo",
         "obj": "Use CellCLI to inventory storage cells",
         "scenario": "You just SSH'd into cel01 and want to see cluster-wide cell status.",
         "tasks": ["cellcli -e list cell detail", "dcli across cellgroup", "Check IB link status"],
         "validation": "All cells show status=online, no alerts."},
        {"id": 4, "title": "Quiz — Exadata Basics", "tag": "quiz",
         "obj": "Test fundamental Exadata knowledge",
         "scenario": "3 MCQ questions on Smart Scan, IB, and storage indexes.",
         "tasks": ["Answer 3 MCQ questions"],
         "validation": "Score 3/3 to pass."},
    ],
    "L2 — Intermediate Operations": [
        {"id": 27, "title": "Add Disk to Diskgroup", "tag": "lab",
         "obj": "Expand DATAC1 by adding new grid disks from an added cell",
         "scenario": "DATAC1 diskgroup at 78% — add capacity from new grid disks on cel04.",
         "tasks": ["Create celldisks on new cell", "Create grid disks with correct naming",
                   "ALTER DISKGROUP DATAC1 ADD DISK", "Monitor rebalance via V$ASM_OPERATION"],
         "validation": "V$ASM_DISKGROUP shows increased total_mb, rebalance completes."},
        {"id": 42, "title": "Data Guard Switchover", "tag": "demo",
         "obj": "Perform a graceful role reversal between primary and standby",
         "scenario": "Planned DC maintenance — switchover ORCL_PRI to ORCL_STBY.",
         "tasks": ["DGMGRL> show configuration",
                   "DGMGRL> switchover to ORCL_STBY",
                   "Verify new primary is open read-write"],
         "validation": "show configuration displays SUCCESS with roles reversed."},
        {"id": 48, "title": "RMAN Incremental Backup", "tag": "lab",
         "obj": "Run a level-1 incremental backup to FRA",
         "scenario": "Nightly incremental after Sunday's level-0.",
         "tasks": ["rman target /", "BACKUP INCREMENTAL LEVEL 1 DATABASE", "List backups"],
         "validation": "LIST BACKUP SUMMARY shows new incremental backupset."},
    ],
    "L3 — Advanced Operations": [
        {"id": 57, "title": "Smart Scan Verification", "tag": "lab",
         "obj": "Prove a query is offloaded to the cells",
         "scenario": "A full-table scan on SALES isn't fast — verify Smart Scan is active.",
         "tasks": ["Run query with /*+ FULL(t) */",
                   "Check V$SQL cell offload efficiency",
                   "Check cell_physical_IO_bytes_saved_by_storage_index"],
         "validation": "offload efficiency > 80%, bytes saved by SI > 0."},
        {"id": 73, "title": "Rolling Cell Patch", "tag": "demo",
         "obj": "Apply a storage cell image update with zero downtime",
         "scenario": "Patch cel01 to latest image while DB stays online.",
         "tasks": ["alter griddisk all inactive (on one cell)",
                   "patchmgr -cells cel01 -patch",
                   "alter griddisk all active and validate rebalance"],
         "validation": "All grid disks ONLINE, no data loss, image version updated."},
    ],
    "L4 — Expert / Real-World": [
        {"id": 88, "title": "IORM Runaway Workload", "tag": "lab",
         "obj": "Use I/O Resource Manager to contain a noisy neighbor",
         "scenario": "ETL job is starving OLTP — latency spiked to 80ms. Fix it now.",
         "tasks": ["Diagnose using V$IOSTAT_FILE and cell metrics",
                   "Create IORM plan limiting ETL DB",
                   "ALTER IORMPLAN and validate"],
         "validation": "OLTP avg latency returns below 5ms."},
        {"id": 97, "title": "Cell Failure Recovery", "tag": "demo",
         "obj": "Recover from total cell loss with HIGH redundancy",
         "scenario": "cel03 powered off unexpectedly. DATAC1 is HIGH redundancy — no data loss expected.",
         "tasks": ["Confirm ASM auto-drops offline disks after DISK_REPAIR_TIME",
                   "Replace cell, rebuild celldisks/griddisks",
                   "ALTER DISKGROUP ADD DISK and rebalance"],
         "validation": "DATAC1 returns to HIGH redundancy, no corruption."},
    ],
}

# =============================================================================
# SESSION STATE
# =============================================================================
defaults = {
    "openai_key": "",
    "openai_model": "gpt-4o",
    "rack": "Half Rack",
    "dg": "DATAC1+RECOC1",
    "role": "DBA",
    "level": "Intermediate",
    "current_lab": None,
    "chat": [],
    "term_history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Try secrets
try:
    if not st.session_state.openai_key:
        st.session_state.openai_key = st.secrets.get("openai_key", "")
except Exception:
    pass

# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div style="border-bottom:1px solid #1a2c47;padding-bottom:12px;margin-bottom:18px;">
  <div class="brand-title">▸ ORACLE EXADATA X8M — LAB SIMULATOR</div>
  <div class="brand-sub">DBA/DMA Hands-On Trainer • ExaSimBot (GPT-4o) • Prashant | Oracle ACE (Apprentice)</div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# CONFIG BAR
# =============================================================================
with st.container():
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
# DYNAMIC ARCHITECTURE DIAGRAM (SVG)
# =============================================================================
def build_diagram(compute, cells, ib, rack_name):
    W, H = 900, 520
    # Compute row
    cw = min(110, (W - 80) // compute - 14)
    cw_total = compute * (cw + 14) - 14
    cx0 = (W - cw_total) // 2
    cy = 70
    ch = 55

    # IB row
    iw = 150
    iw_total = ib * (iw + 24) - 24
    ix0 = (W - iw_total) // 2
    iy = 200
    ih = 44

    # Cells row
    sw = min(90, (W - 80) // cells - 10)
    sw_total = cells * (sw + 10) - 10
    sx0 = (W - sw_total) // 2
    sy = 310
    sh = 72

    svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">']
    svg.append('''
    <defs>
      <linearGradient id="gc" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0a4a8a"/><stop offset="100%" stop-color="#062547"/>
      </linearGradient>
      <linearGradient id="gs" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#005a35"/><stop offset="100%" stop-color="#002818"/>
      </linearGradient>
      <linearGradient id="gi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#4a2288"/><stop offset="100%" stop-color="#1e0a42"/>
      </linearGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="2.5"/></filter>
    </defs>
    ''')

    # Title bar
    svg.append(f'<rect x="0" y="0" width="{W}" height="32" fill="#0a1220"/>')
    svg.append(f'<text x="{W//2}" y="21" text-anchor="middle" font-family="Orbitron" '
               f'font-size="13" fill="#f39c12" letter-spacing="3">'
               f'[ {rack_name.upper()} — {compute} COMPUTE • {cells} CELLS • {ib} IB HDR ]</text>')

    # Section labels
    svg.append('<text x="20" y="60" font-family="Rajdhani" font-size="11" '
               'fill="#6a8faa" letter-spacing="2">DATABASE TIER (X8M-2)</text>')
    svg.append('<text x="20" y="190" font-family="Rajdhani" font-size="11" '
               'fill="#6a8faa" letter-spacing="2">INFINIBAND HDR FABRIC — 200 Gb/s</text>')
    svg.append('<text x="20" y="300" font-family="Rajdhani" font-size="11" '
               'fill="#6a8faa" letter-spacing="2">STORAGE TIER (X8M-2 CELLS)</text>')

    # Compute nodes
    comp_centers = []
    for i in range(compute):
        x = cx0 + i * (cw + 14)
        cxc = x + cw // 2
        comp_centers.append((cxc, cy + ch))
        svg.append(f'<rect x="{x}" y="{cy}" width="{cw}" height="{ch}" rx="5" '
                   f'fill="url(#gc)" stroke="#0088ff" stroke-width="1.5"/>')
        svg.append(f'<text x="{cxc}" y="{cy+20}" text-anchor="middle" font-family="Orbitron" '
                   f'font-size="11" fill="#66c2ff" font-weight="700">exadb0{i+1}</text>')
        svg.append(f'<text x="{cxc}" y="{cy+35}" text-anchor="middle" '
                   f'font-family="Share Tech Mono" font-size="9" fill="#c8dff8">48c • 1.5TB</text>')
        svg.append(f'<text x="{cxc}" y="{cy+47}" text-anchor="middle" '
                   f'font-family="Share Tech Mono" font-size="8" fill="#8ab4d8">+ASM{i+1} ORCL{i+1}</text>')
        svg.append(f'<circle cx="{x+8}" cy="{cy+8}" r="3" fill="#00ff88">'
                   f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>')

    # IB switches
    ib_centers = []
    for i in range(ib):
        x = ix0 + i * (iw + 24)
        ixc = x + iw // 2
        ib_centers.append((ixc, iy, iy + ih))
        svg.append(f'<rect x="{x}" y="{iy}" width="{iw}" height="{ih}" rx="4" '
                   f'fill="url(#gi)" stroke="#8844ff" stroke-width="1.5"/>')
        svg.append(f'<text x="{ixc}" y="{iy+18}" text-anchor="middle" font-family="Orbitron" '
                   f'font-size="11" fill="#c8a0ff" font-weight="700">IB HDR SW{i+1}</text>')
        svg.append(f'<text x="{ixc}" y="{iy+33}" text-anchor="middle" '
                   f'font-family="Share Tech Mono" font-size="9" fill="#c8dff8">200 Gb/s • RDMA</text>')

    # Cells
    cell_centers = []
    for i in range(cells):
        x = sx0 + i * (sw + 10)
        sxc = x + sw // 2
        cell_centers.append((sxc, sy))
        svg.append(f'<rect x="{x}" y="{sy}" width="{sw}" height="{sh}" rx="4" '
                   f'fill="url(#gs)" stroke="#00ff88" stroke-width="1.2"/>')
        svg.append(f'<text x="{sxc}" y="{sy+16}" text-anchor="middle" font-family="Orbitron" '
                   f'font-size="10" fill="#66ffb0" font-weight="700">cel{str(i+1).zfill(2)}</text>')
        svg.append(f'<text x="{sxc}" y="{sy+32}" text-anchor="middle" '
                   f'font-family="Share Tech Mono" font-size="8" fill="#c8dff8">86.4TB HDD</text>')
        svg.append(f'<text x="{sxc}" y="{sy+45}" text-anchor="middle" '
                   f'font-family="Share Tech Mono" font-size="8" fill="#c8dff8">25.6TB NVMe</text>')
        svg.append(f'<text x="{sxc}" y="{sy+58}" text-anchor="middle" '
                   f'font-family="Share Tech Mono" font-size="7" fill="#8ab4d8">1.5TB PMEM</text>')
        svg.append(f'<circle cx="{x+8}" cy="{sy+8}" r="2.5" fill="#00ff88">'
                   f'<animate attributeName="opacity" values="1;0.2;1" dur="{1.5+i*0.1}s" repeatCount="indefinite"/></circle>')

    # Links: compute -> IB
    for cxc, cyc in comp_centers:
        for ixc, iyt, _ in ib_centers:
            svg.append(f'<line x1="{cxc}" y1="{cyc}" x2="{ixc}" y2="{iyt}" '
                       f'stroke="#8844ff" stroke-width="1" stroke-opacity="0.5"/>')
    # Links: IB -> cells
    for ixc, _, iyb in ib_centers:
        for sxc, syt in cell_centers:
            svg.append(f'<line x1="{ixc}" y1="{iyb}" x2="{sxc}" y2="{syt}" '
                       f'stroke="#8844ff" stroke-width="0.8" stroke-opacity="0.35"/>')

    # Animated RDMA packets
    for k in range(min(4, compute)):
        c = comp_centers[k % len(comp_centers)]
        ibx, iyt, iyb = ib_centers[k % len(ib_centers)]
        cc = cell_centers[(k * 2) % len(cell_centers)]
        path = f"M{c[0]},{c[1]} L{ibx},{iyt} L{ibx},{iyb} L{cc[0]},{cc[1]}"
        svg.append(f'<circle r="3.5" fill="#f39c12" filter="url(#glow)">'
                   f'<animateMotion dur="{2+k*0.4}s" repeatCount="indefinite" '
                   f'path="{path}"/></circle>')

    # Bottom status bar
    total_hdd = cells * 86.4
    total_flash = cells * 25.6
    hdd_str = f"{total_hdd/1000:.2f}PB" if total_hdd >= 1000 else f"{total_hdd:.0f}TB"
    svg.append(f'<rect x="0" y="{H-30}" width="{W}" height="30" fill="#0a1220"/>')
    svg.append(f'<text x="20" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#00ff88">● CLUSTER: ONLINE</text>')
    svg.append(f'<text x="180" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#c8dff8">ASM RAW: {hdd_str}</text>')
    svg.append(f'<text x="360" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#f39c12">FLASH: {total_flash:.1f}TB</text>')
    svg.append(f'<text x="530" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#8844ff">IB: {ib}× 200Gb HDR</text>')
    svg.append(f'<text x="700" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#c8dff8">CORES: {compute*48}</text>')

    svg.append('</svg>')
    return "".join(svg)

# =============================================================================
# LAYOUT: architecture (left) + specs (right)
# =============================================================================
left, right = st.columns([2.4, 1])

with left:
    st.markdown('<div class="panel"><div class="panel-title">▸ Live Rack Topology</div>',
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
      <div class="panel-title">▸ Configuration Totals</div>
      <div class="metric-pill">Compute <span class="v">{COMPUTE}</span></div>
      <div class="metric-pill">Cells <span class="v">{CELLS}</span></div>
      <div class="metric-pill">IB SW <span class="v">{IB}</span></div><br><br>
      <div class="metric-pill">Cores <span class="v">{total_cores}</span></div>
      <div class="metric-pill">HDD <span class="v">{hdd_disp}</span></div><br><br>
      <div class="metric-pill">NVMe <span class="v">{total_flash:.1f} TB</span></div>
      <div class="metric-pill">PMEM <span class="v">{total_cell_pmem:.1f} TB</span></div><br><br>
      <div class="metric-pill">DG <span class="v">{st.session_state.dg}</span></div><br><br>
      <div class="metric-pill">Role <span class="v">{st.session_state.role}</span></div>
      <div class="metric-pill">Level <span class="v">{st.session_state.level}</span></div>
    </div>
    ''', unsafe_allow_html=True)

# =============================================================================
# LAB SELECTION + CHAT + PRACTICE TERMINAL
# =============================================================================
st.markdown('<div class="panel"><div class="panel-title">▸ Lab Catalog</div>',
            unsafe_allow_html=True)

tab_names = list(LAB_CATALOG.keys())
tabs = st.tabs(tab_names)
for tab, group in zip(tabs, tab_names):
    with tab:
        for lab in LAB_CATALOG[group]:
            tag_cls = f"tag-{lab['tag']}"
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.markdown(
                    f'<div class="lab-card"><span class="id">LAB #{lab["id"]:03d}</span> '
                    f'<span class="ttl">{lab["title"]}</span> '
                    f'<span class="{tag_cls}">{lab["tag"].upper()}</span><br>'
                    f'<span style="color:#8ab4d8;font-size:12px">{lab["obj"]}</span></div>',
                    unsafe_allow_html=True)
            with col_b:
                if st.button("Start", key=f"start_{lab['id']}"):
                    st.session_state.current_lab = lab
                    st.session_state.chat = []
                    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# SYSTEM PROMPT BUILDER
# =============================================================================
def system_prompt():
    lab = st.session_state.current_lab
    env = (f"Rack={st.session_state.rack}, Cells={CELLS}, Compute={COMPUTE}, "
           f"IB_Switches={IB}, DGs={st.session_state.dg}, "
           f"Role={st.session_state.role}, Level={st.session_state.level}")
    lab_block = ""
    if lab:
        lab_block = (
            f"CURRENT LAB #{lab['id']}: {lab['title']} [{lab['tag'].upper()}]\n"
            f"Objective: {lab['obj']}\n"
            f"Scenario: {lab['scenario']}\n"
            f"Tasks: {' | '.join(lab['tasks'])}\n"
            f"Validation: {lab['validation']}\n"
        )
    return f"""You are ExaSimBot — Oracle Exadata X8M DBA/DMA Hands-On Lab Trainer.
Senior Exadata DBA with 15+ years experience. Direct, practical, technical.

ENVIRONMENT: {env}
{lab_block}
RULES:
1. Commands ALWAYS in triple-backtick code blocks with correct prompt prefix
   (CellCLI>, SQL>, DGMGRL>, $, #).
2. Show realistic simulated Exadata output after every command.
3. LAB tag: demo first, then "YOUR TURN" exercise for the practice terminal.
4. QUIZ tag: ask 3 MCQ questions A/B/C/D, score CORRECT ✓ / WRONG ✗.
5. Depth: Basic=concepts, Intermediate=full procedure, Advanced=internals.
6. DBA = SQL/ASM/RMAN/srvctl/crsctl/DGMGRL. DMA = hardware/firmware/ILOM/patchmgr.
7. L4 incident labs: present symptoms first, ask the user to diagnose.
8. Max 500 words per response.

X8M SPECS: {X8M_SPECS_TEXT}
"""

# =============================================================================
# CHAT INTERFACE
# =============================================================================
st.markdown('<div class="panel"><div class="panel-title">▸ ExaSimBot — AI Trainer</div>',
            unsafe_allow_html=True)

if st.session_state.current_lab:
    lab = st.session_state.current_lab
    st.markdown(f"**Active Lab:** #{lab['id']} — {lab['title']} "
                f"({lab['tag'].upper()})")
else:
    st.info("Select a lab above, or ask ExaSimBot anything about Exadata.")

# Show history
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask ExaSimBot or type a command...")

if user_input:
    if not st.session_state.openai_key:
        st.error("⚠ Enter your OpenAI API key in the top config bar.")
    else:
        st.session_state.chat.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            client = OpenAI(api_key=st.session_state.openai_key)
            messages = [{"role": "system", "content": system_prompt()}]
            messages.extend(st.session_state.chat[-18:])

            with st.chat_message("assistant"):
                placeholder = st.empty()
                full = ""
                stream = client.chat.completions.create(
                    model=st.session_state.openai_model,
                    messages=messages,
                    max_tokens=1500,
                    temperature=0.4,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    full += delta
                    placeholder.markdown(full + "▌")
                placeholder.markdown(full)
            st.session_state.chat.append({"role": "assistant", "content": full})
        except Exception as e:
            st.error(f"OpenAI error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# PRACTICE TERMINAL
# =============================================================================
st.markdown('<div class="panel"><div class="panel-title">▸ Practice Terminal</div>',
            unsafe_allow_html=True)

# Dynamic prompt
def get_prompt_sym():
    if not st.session_state.current_lab:
        return "$"
    title = st.session_state.current_lab["title"].lower()
    if "cell" in title or "griddisk" in title or "flash" in title:
        return "CellCLI>"
    if "data guard" in title or "switchover" in title or "standby" in title:
        return "DGMGRL>"
    if "pdb" in title or "smart scan" in title or "diskgroup" in title or "rman" in title:
        return "SQL>"
    return "$"

sym = get_prompt_sym()

# Render terminal history
term_html = '<div class="terminal">'
term_html += '<div style="color:#f39c12">[ExaSimBot Practice Terminal — type commands below]</div>'
for entry in st.session_state.term_history[-20:]:
    term_html += f'<div><span class="prompt">{entry["p"]}</span> <span class="cmd">{entry["c"]}</span></div>'
    if entry.get("out"):
        term_html += f'<div class="ai">{entry["out"]}</div>'
term_html += f'<div><span class="prompt">{sym}</span> <span style="color:#f39c12">_</span></div>'
term_html += '</div>'
st.markdown(term_html, unsafe_allow_html=True)

col_t1, col_t2 = st.columns([5, 1])
with col_t1:
    cmd = st.text_input("Command", key="pt_cmd",
                        placeholder=f"{sym} enter a command and press Evaluate",
                        label_visibility="collapsed")
with col_t2:
    evaluate = st.button("Evaluate", use_container_width=True)

if evaluate and cmd:
    if not st.session_state.openai_key:
        st.error("⚠ Enter your OpenAI API key.")
    elif not st.session_state.current_lab:
        st.warning("Select a lab first.")
    else:
        try:
            client = OpenAI(api_key=st.session_state.openai_key)
            lab = st.session_state.current_lab
            eval_prompt = (
                f"[PRACTICE TERMINAL] User typed: `{cmd}`\n"
                f"Lab #{lab['id']}: {lab['title']}\n"
                f"Objective: {lab['obj']}\n\n"
                f"In max 120 words: Is this correct for this lab context? "
                f"Show the realistic Exadata output. "
                f"End with CORRECT (+10 pts) or WRONG and show the right command."
            )
            resp = client.chat.completions.create(
                model=st.session_state.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt()},
                    {"role": "user", "content": eval_prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )
            output = resp.choices[0].message.content
            st.session_state.term_history.append({"p": sym, "c": cmd, "out": output})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div style="text-align:center;color:#6a8faa;font-size:11px;
            letter-spacing:2px;margin-top:20px;padding:12px;
            border-top:1px solid #1a2c47;">
EXADATA X8M SIMULATOR v2.0 • BUILT WITH STREAMLIT + OPENAI GPT-4o<br>
PRASHANT | ORACLE ACE (APPRENTICE) | PRASHANTORACLEDBA.WORDPRESS.COM
</div>
""", unsafe_allow_html=True)
