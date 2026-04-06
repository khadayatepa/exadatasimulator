import streamlit as st
from openai import AzureOpenAI
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Oracle Exadata X8M Simulator",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Hide default streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Top banner */
.top-banner {
    background: linear-gradient(135deg, #0a1628 0%, #0d2040 100%);
    border-bottom: 3px solid #e74c3c;
    padding: 14px 24px;
    margin: -1rem -1rem 1rem -1rem;
    display: flex; align-items: center; gap: 16px;
}
.top-banner-logo {
    font-size: 11px; color: #e74c3c; letter-spacing: 3px;
    text-transform: uppercase; font-weight: 700; font-family: 'JetBrains Mono', monospace;
}
.top-banner-title {
    font-size: 18px; color: #d0e8f8; font-weight: 600;
}
.top-banner-sub {
    font-size: 12px; color: #8aadcc; margin-top: 2px;
}

/* Rack unit badges */
.rack-container {
    background: #0d1e35; border-radius: 8px; padding: 10px 14px;
    border: 1px solid #1e3a5f; margin-bottom: 12px;
}
.rack-title {
    font-size: 10px; color: #4a7ab5; letter-spacing: 1.5px;
    text-transform: uppercase; margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
}
.rack-units { display: flex; flex-wrap: wrap; gap: 4px; }
.ru { padding: 3px 8px; border-radius: 3px; font-size: 9px;
      font-family: 'JetBrains Mono', monospace; border: 1px solid; display: inline-block; }
.ru-compute { background: #0e2a5a; color: #5da8e8; border-color: #1a4a9a; }
.ru-cell    { background: #0a2a18; color: #5dc888; border-color: #1a5a30; }
.ru-sw      { background: #1a0a3a; color: #a870c8; border-color: #4a1a7a; }
.ru-infra   { background: #2a1a0a; color: #c8a828; border-color: #6a4a18; }

/* Step cards */
.step-card {
    background: #0d1e35; border: 1px solid #1e3a5f; border-radius: 6px;
    padding: 8px 12px; margin-bottom: 6px; cursor: pointer;
    transition: all 0.15s; display: flex; align-items: center; gap: 8px;
}
.step-card:hover { border-color: #2a5080; background: #122240; }
.step-card.active { border-color: #f39c12; background: #1a1400; }
.step-card.done   { border-color: #27ae60; opacity: 0.7; }
.step-num {
    width: 22px; height: 22px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; flex-shrink: 0;
    font-family: 'JetBrains Mono', monospace;
}
.step-num-active  { background: #f39c12; color: #000; }
.step-num-done    { background: #27ae60; color: #fff; }
.step-num-default { background: #122240; color: #4a7ab5; border: 1px solid #1e3a5f; }
.step-name { font-size: 11px; color: #c8dff0; flex: 1; line-height: 1.3; }
.step-tag {
    font-size: 8px; padding: 2px 5px; border-radius: 3px;
    font-family: 'JetBrains Mono', monospace; border: 1px solid;
}
.tag-demo { background: #0a1f2a; color: #5da8e8; border-color: #1a3a5a; }
.tag-lab  { background: #0a1f0a; color: #5dc888; border-color: #1a4a1a; }
.tag-quiz { background: #1f0a0a; color: #e87a5a; border-color: #5a1a1a; }

/* Chat bubbles */
.chat-user {
    background: #150808; border: 1px solid #3a1010;
    border-radius: 10px 10px 3px 10px;
    padding: 10px 14px; margin: 6px 0 6px 60px;
    color: #f0d0d0; font-size: 13px; line-height: 1.6;
}
.chat-assistant {
    background: #0d1e35; border: 1px solid #1e3a5f;
    border-radius: 10px 10px 10px 3px;
    padding: 10px 14px; margin: 6px 60px 6px 0;
    color: #c8dff0; font-size: 13px; line-height: 1.6;
}
.chat-system {
    background: #111108; border: 1px solid #3a3a10;
    border-radius: 6px; padding: 8px 12px; margin: 6px 30px;
    color: #e0d898; font-size: 11px; line-height: 1.5;
    font-family: 'JetBrains Mono', monospace;
}
.chat-avatar {
    width: 28px; height: 28px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; flex-shrink: 0;
}

/* Terminal box */
.terminal-box {
    background: #030810; border: 1px solid #1a4a2a;
    border-radius: 6px; padding: 12px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; color: #5dc888;
    margin: 8px 0; white-space: pre-wrap;
}
.terminal-prompt { color: #5dc888; }
.terminal-output { color: #9ad8b0; }

/* Metric cards */
.metric-row { display: flex; gap: 10px; margin-bottom: 12px; flex-wrap: wrap; }
.metric-card {
    background: #0d1e35; border: 1px solid #1e3a5f;
    border-radius: 6px; padding: 10px 16px; flex: 1; min-width: 80px;
    text-align: center;
}
.metric-val { font-size: 22px; font-weight: 700; color: #f39c12;
              font-family: 'JetBrains Mono', monospace; }
.metric-lbl { font-size: 10px; color: #4a7ab5; text-transform: uppercase;
              letter-spacing: 1px; margin-top: 2px; }

/* Progress bar */
.prog-outer {
    background: #1e3a5f; border-radius: 4px; height: 6px; margin: 8px 0;
}
.prog-inner {
    background: #f39c12; border-radius: 4px; height: 100%;
    transition: width 0.4s ease;
}

/* Sidebar styles */
[data-testid="stSidebar"] {
    background: #070f1e !important;
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] * { color: #8aadcc !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid #1e3a5f !important;
    color: #8aadcc !important;
    text-align: left !important;
    width: 100% !important;
    border-radius: 4px !important;
    font-size: 12px !important;
    padding: 6px 10px !important;
    transition: all 0.1s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #122240 !important;
    border-color: #2a5080 !important;
    color: #c8dff0 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #1a0e0e !important;
    border-color: #e74c3c !important;
    color: #e74c3c !important;
}

/* Main area buttons */
.stButton > button {
    border-radius: 6px !important;
    font-size: 12px !important;
    transition: all 0.15s !important;
}

/* Selectbox, text input dark */
.stSelectbox > div > div, .stTextInput > div > div {
    background: #0d1e35 !important;
    border-color: #1e3a5f !important;
    color: #c8dff0 !important;
}

/* Main background */
.main .block-container {
    background: #0a1628;
    padding-top: 0;
}
.stApp { background: #0a1628; }
</style>
""", unsafe_allow_html=True)


# ── Lab definitions ───────────────────────────────────────────────────────────
LABS = {
    "arch": {
        "title": "X8M Architecture Overview", "icon": "🏗️",
        "steps": [
            {"n": 1, "t": "X8M hardware specs", "tag": "demo"},
            {"n": 2, "t": "PMEM & NVMe architecture", "tag": "demo"},
            {"n": 3, "t": "SQL-to-storage data path", "tag": "demo"},
            {"n": 4, "t": "Quiz: architecture", "tag": "quiz"},
        ]
    },
    "compute": {
        "title": "Compute Nodes X8M-2", "icon": "💻",
        "steps": [
            {"n": 1, "t": "Node specs (CPU/RAM/PMEM)", "tag": "demo"},
            {"n": 2, "t": "Check node via DBMCLI", "tag": "lab"},
            {"n": 3, "t": "ILOM console access", "tag": "lab"},
            {"n": 4, "t": "Quiz: compute nodes", "tag": "quiz"},
        ]
    },
    "cell_svr": {
        "title": "Cell Servers & Storage", "icon": "💾",
        "steps": [
            {"n": 1, "t": "Cell server specs & disk layout", "tag": "demo"},
            {"n": 2, "t": "LIST CELLDISK", "tag": "lab"},
            {"n": 3, "t": "LIST GRIDDISK DETAIL", "tag": "lab"},
            {"n": 4, "t": "DESCRIBE CELLDISK", "tag": "lab"},
            {"n": 5, "t": "Quiz: cell servers", "tag": "quiz"},
        ]
    },
    "ib": {
        "title": "InfiniBand & RDMA", "icon": "🔗",
        "steps": [
            {"n": 1, "t": "IB HDR 100Gb topology", "tag": "demo"},
            {"n": 2, "t": "RDMA storage access", "tag": "demo"},
            {"n": 3, "t": "ibstatus / ibnetdiscover", "tag": "lab"},
            {"n": 4, "t": "Quiz: IB/RDMA", "tag": "quiz"},
        ]
    },
    "disk_add": {
        "title": "🔴 Add Cell Disk (Hot-Add)", "icon": "➕",
        "steps": [
            {"n": 1, "t": "Hot-add workflow overview", "tag": "demo"},
            {"n": 2, "t": "LIST PHYSICALDISK — find new disk", "tag": "lab"},
            {"n": 3, "t": "CREATE CELLDISK", "tag": "lab"},
            {"n": 4, "t": "Verify CELLDISK created", "tag": "lab"},
            {"n": 5, "t": "CREATE GRIDDISK on new celldisk", "tag": "lab"},
            {"n": 6, "t": "ALTER DISKGROUP ADD disk", "tag": "lab"},
            {"n": 7, "t": "Monitor ASM rebalance", "tag": "lab"},
            {"n": 8, "t": "Quiz: full disk add flow", "tag": "quiz"},
        ]
    },
    "griddisk": {
        "title": "Create Grid Disks", "icon": "🗄️",
        "steps": [
            {"n": 1, "t": "CellDisk vs GridDisk concept", "tag": "demo"},
            {"n": 2, "t": "LIST CELLDISK — check free space", "tag": "lab"},
            {"n": 3, "t": "CREATE GRIDDISK with size", "tag": "lab"},
            {"n": 4, "t": "Verify in V$ASM_DISK", "tag": "lab"},
            {"n": 5, "t": "Quiz: grid disks", "tag": "quiz"},
        ]
    },
    "asm_dg": {
        "title": "🔴 ASM Disk Group Admin", "icon": "⚙️",
        "steps": [
            {"n": 1, "t": "DG types & redundancy", "tag": "demo"},
            {"n": 2, "t": "V$ASM_DISKGROUP query", "tag": "lab"},
            {"n": 3, "t": "ALTER DISKGROUP ADD", "tag": "lab"},
            {"n": 4, "t": "Monitor rebalance", "tag": "lab"},
            {"n": 5, "t": "ALTER DISKGROUP DROP", "tag": "lab"},
            {"n": 6, "t": "Mount / Dismount", "tag": "lab"},
            {"n": 7, "t": "Quiz: ASM disk group", "tag": "quiz"},
        ]
    },
    "acfs": {
        "title": "🔴 ACFS Creation", "icon": "📁",
        "steps": [
            {"n": 1, "t": "What is ACFS?", "tag": "demo"},
            {"n": 2, "t": "asmcmd volcreate", "tag": "lab"},
            {"n": 3, "t": "mkfs.acfs format", "tag": "lab"},
            {"n": 4, "t": "srvctl add filesystem", "tag": "lab"},
            {"n": 5, "t": "Mount on all nodes", "tag": "lab"},
            {"n": 6, "t": "Quiz: ACFS", "tag": "quiz"},
        ]
    },
    "acfs_db": {
        "title": "Attach ACFS to DB", "icon": "🔌",
        "steps": [
            {"n": 1, "t": "Use cases for ACFS with DB", "tag": "demo"},
            {"n": 2, "t": "mkdir on ACFS mount", "tag": "lab"},
            {"n": 3, "t": "chown permissions", "tag": "lab"},
            {"n": 4, "t": "CREATE DIRECTORY SQL object", "tag": "lab"},
            {"n": 5, "t": "Test with Data Pump expdp", "tag": "lab"},
            {"n": 6, "t": "Quiz: ACFS with DB", "tag": "quiz"},
        ]
    },
    "cellcli": {
        "title": "CellCLI Deep Dive", "icon": "⌨️",
        "steps": [
            {"n": 1, "t": "CellCLI basics & syntax", "tag": "demo"},
            {"n": 2, "t": "LIST commands", "tag": "lab"},
            {"n": 3, "t": "DESCRIBE objects", "tag": "lab"},
            {"n": 4, "t": "ALTER commands", "tag": "lab"},
            {"n": 5, "t": "Metrics & alerts", "tag": "lab"},
            {"n": 6, "t": "Quiz: CellCLI mastery", "tag": "quiz"},
        ]
    },
    "dcli": {
        "title": "DCLI Parallel Operations", "icon": "🔁",
        "steps": [
            {"n": 1, "t": "DCLI overview", "tag": "demo"},
            {"n": 2, "t": "DCLI syntax & flags", "tag": "lab"},
            {"n": 3, "t": "Run CellCLI across all cells", "tag": "lab"},
            {"n": 4, "t": "DCLI for compute nodes", "tag": "lab"},
            {"n": 5, "t": "Quiz: DCLI", "tag": "quiz"},
        ]
    },
    "dbmcli": {
        "title": "DBMCLI Administration", "icon": "🖥️",
        "steps": [
            {"n": 1, "t": "DBMCLI vs CellCLI", "tag": "demo"},
            {"n": 2, "t": "LIST DBSERVER detail", "tag": "lab"},
            {"n": 3, "t": "LIST PHYSICALDISK", "tag": "lab"},
            {"n": 4, "t": "Configure alerting", "tag": "lab"},
            {"n": 5, "t": "Quiz: DBMCLI", "tag": "quiz"},
        ]
    },
    "smart_scan": {
        "title": "Smart Scan Lab", "icon": "🔍",
        "steps": [
            {"n": 1, "t": "Smart Scan theory", "tag": "demo"},
            {"n": 2, "t": "Enable & verify cell_offload_processing", "tag": "lab"},
            {"n": 3, "t": "Run Smart Scan eligible query", "tag": "lab"},
            {"n": 4, "t": "V$SYSSTAT — offload statistics", "tag": "lab"},
            {"n": 5, "t": "Quiz: Smart Scan", "tag": "quiz"},
        ]
    },
    "hcc": {
        "title": "Hybrid Columnar Compression", "icon": "🗜️",
        "steps": [
            {"n": 1, "t": "4 HCC compression levels", "tag": "demo"},
            {"n": 2, "t": "CREATE TABLE with HCC", "tag": "lab"},
            {"n": 3, "t": "Measure compression ratio", "tag": "lab"},
            {"n": 4, "t": "DML behavior & row migration", "tag": "demo"},
            {"n": 5, "t": "Quiz: HCC", "tag": "quiz"},
        ]
    },
    "iorm": {
        "title": "IORM Setup", "icon": "⚖️",
        "steps": [
            {"n": 1, "t": "IORM concepts", "tag": "demo"},
            {"n": 2, "t": "LIST IORMPLAN", "tag": "lab"},
            {"n": 3, "t": "ALTER IORMPLAN with DB shares", "tag": "lab"},
            {"n": 4, "t": "Monitor V$CELL_IOREASON", "tag": "lab"},
            {"n": 5, "t": "Quiz: IORM", "tag": "quiz"},
        ]
    },
    "flash": {
        "title": "Smart Flash Cache", "icon": "⚡",
        "steps": [
            {"n": 1, "t": "Write-back vs write-through", "tag": "demo"},
            {"n": 2, "t": "LIST FLASHCACHE / FLASHLOG", "tag": "lab"},
            {"n": 3, "t": "CREATE FLASHCACHE ALL", "tag": "lab"},
            {"n": 4, "t": "Monitor flash cache hit ratio", "tag": "lab"},
            {"n": 5, "t": "Quiz: Flash Cache", "tag": "quiz"},
        ]
    },
    "rac": {
        "title": "RAC on Exadata", "icon": "🔄",
        "steps": [
            {"n": 1, "t": "RAC + X8M architecture", "tag": "demo"},
            {"n": 2, "t": "srvctl start/stop/status", "tag": "lab"},
            {"n": 3, "t": "Cache Fusion via RDMA", "tag": "demo"},
            {"n": 4, "t": "Quiz: RAC on Exadata", "tag": "quiz"},
        ]
    },
    "dg": {
        "title": "Data Guard on Exadata", "icon": "🛡️",
        "steps": [
            {"n": 1, "t": "DG architecture on Exadata", "tag": "demo"},
            {"n": 2, "t": "DGMGRL switchover", "tag": "lab"},
            {"n": 3, "t": "Active Data Guard queries", "tag": "lab"},
            {"n": 4, "t": "Quiz: Data Guard", "tag": "quiz"},
        ]
    },
    "patch": {
        "title": "Rolling Patch Exadata", "icon": "🔧",
        "steps": [
            {"n": 1, "t": "Patch types overview", "tag": "demo"},
            {"n": 2, "t": "exachk pre-patch check", "tag": "lab"},
            {"n": 3, "t": "patchmgr for storage cells", "tag": "lab"},
            {"n": 4, "t": "opatchauto for compute nodes", "tag": "lab"},
            {"n": 5, "t": "Post-patch validation", "tag": "lab"},
            {"n": 6, "t": "Quiz: patching", "tag": "quiz"},
        ]
    },
    "health": {
        "title": "Health Checks", "icon": "❤️",
        "steps": [
            {"n": 1, "t": "exachk overview", "tag": "demo"},
            {"n": 2, "t": "Run full exachk", "tag": "lab"},
            {"n": 3, "t": "exadatadiag collection", "tag": "lab"},
            {"n": 4, "t": "OEM Exadata plug-in", "tag": "demo"},
            {"n": 5, "t": "Quiz: health checks", "tag": "quiz"},
        ]
    },
    "trouble": {
        "title": "Troubleshooting Exadata", "icon": "🚨",
        "steps": [
            {"n": 1, "t": "Top 10 Exadata issues", "tag": "demo"},
            {"n": 2, "t": "Cell server offline — diagnose", "tag": "lab"},
            {"n": 3, "t": "Smart Scan disabled — fix", "tag": "lab"},
            {"n": 4, "t": "ASM rebalance stuck", "tag": "lab"},
            {"n": 5, "t": "IB link failure — diagnose", "tag": "lab"},
            {"n": 6, "t": "Live scenario quiz", "tag": "quiz"},
        ]
    },
}

LAB_GROUPS = {
    "🏗️ Architecture": ["arch", "compute", "cell_svr", "ib"],
    "💾 Storage Labs": ["disk_add", "griddisk", "asm_dg", "acfs", "acfs_db"],
    "⌨️ CLI Mastery": ["cellcli", "dcli", "dbmcli"],
    "✨ Exadata Features": ["smart_scan", "hcc", "iorm", "flash"],
    "🚀 Advanced": ["rac", "dg", "patch", "health", "trouble"],
}

STEP_PROMPTS = {
    "demo": "Walk me through this step with full explanation. Show ALL commands in code blocks with the correct Exadata prompt prefix (e.g. CellCLI>, SQL>, $, #). Show realistic simulated output after every command. Use clear section headings.",
    "lab":  "First DEMO this step with the exact command and realistic simulated output. Then end with a clear section:\n\n**YOUR TURN — Practice Exercise:**\nWrite the exact command I should type (in a code block). Ask me to type it in the Practice Terminal below and press Run.",
    "quiz": "Quiz me on this topic. Ask 3 multiple-choice questions (MCQ) one by one:\nFormat each as:\nQ1: [question text]\nA) ...\nB) ...\nC) ...\nD) ...\n\nAfter I answer, tell me CORRECT ✓ or WRONG ✗ with a brief explanation, then ask the next question.",
}


# ── Session state init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "rack": "Full Rack",
        "cells": 14,
        "compute": 4,
        "dg": "DATA + RECO",
        "role": "DBA",
        "level": "Intermediate",
        "current_lab": "arch",
        "current_step": 0,
        "messages": [],
        "steps_done": set(),
        "score": 0,
        "steps_completed": 0,
        "labs_started": 0,
        "practice_history": [],
        "azure_api_key": "",
        "azure_endpoint": "https://azureopenai-dbmod.openai.azure.com/",
        "azure_deployment": "gpt-4.1",
        "azure_api_version": "2024-12-01-preview",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Helpers ───────────────────────────────────────────────────────────────────
def rack_info():
    rack_map = {
        "1/8 Rack": (2, 3, 1),
        "Quarter Rack": (2, 3, 1),
        "Half Rack": (4, 7, 2),
        "Full Rack": (8, 14, 3),
    }
    r = st.session_state.rack
    default = (st.session_state.compute, st.session_state.cells, 3)
    return rack_map.get(r, default)


def env_context():
    return (
        f"ENVIRONMENT: {st.session_state.rack} | "
        f"{st.session_state.cells} storage cells | "
        f"{st.session_state.compute} compute nodes | "
        f"ASM Disk Groups: {st.session_state.dg} | "
        f"Role: {st.session_state.role} | "
        f"Level: {st.session_state.level}"
    )


def system_prompt():
    return f"""You are ExaSimBot — an expert Oracle Exadata X8M DBA/DMA Lab Trainer and Simulator.

{env_context()}
Current Lab: {LABS[st.session_state.current_lab]['title']}
Current Step: {st.session_state.current_step + 1} of {len(LABS[st.session_state.current_lab]['steps'])}

TEACHING RULES:
1. Always show commands in triple-backtick code blocks with the correct prompt prefix
2. Show realistic simulated Exadata output after each command
3. For LAB steps: demo first, then give a "YOUR TURN" exercise
4. For QUIZ steps: ask MCQ questions (A/B/C/D), score answers as CORRECT ✓ or WRONG ✗
5. Adapt depth to level: Basic=concepts, Intermediate=full procedure, Advanced=internals
6. For DBA role: focus on SQL, ASM, RMAN, srvctl, database admin
7. For DMA role: focus on hardware, firmware, ILOM, patchmgr, cell management
8. Keep responses practical, focused, under 500 words unless complexity demands more

REAL X8M SPECIFICATIONS:
- Compute X8M-2: 2× Intel Cascade Lake-SP 8260 (24 cores each = 48 cores total), up to 6TB DDR4 RAM, 3.2TB PMEM per node, 2×200Gb InfiniBand HDR, Oracle Linux 8
- Cell X8M-2 Storage Server: 12× 7.2TB HDD (86.4TB raw HDD) + 4× 6.4TB NVMe PCI (25.6TB flash) + 1.5TB PMEM, 2×10GbE + 2×200Gb IB
- Full rack: 8 compute + 14 cells + 3 IB switches = ~1.2PB raw
- Half rack: 4 compute + 7 cells + 2 switches
- Quarter rack: 2 compute + 3 cells + 1 switch
- Cell disk naming: CD_00_dm01cel01 through CD_15_dm01cel01
- Grid disk naming: DATAC1_CD_00_dm01cel01, RECOC1_CD_00_dm01cel01
- DCLI group file: /etc/oracle/cell/network-config/cellgroup
- CellCLI: run as root on cell server, prompt = CellCLI>
- DBMCLI: run as root on compute node, prompt = DBMCLI>
- ASM instance runs as +ASM1, +ASM2 etc. on compute nodes

Make every session feel like a REAL Exadata lab environment."""


def build_rack_html():
    cells = st.session_state.cells
    compute = st.session_state.compute
    rack = st.session_state.rack
    sw_map = {"1/8 Rack": 1, "Quarter Rack": 1, "Half Rack": 2, "Full Rack": 3}
    switches = sw_map.get(rack, 3)

    units = []
    units.append('<span class="ru ru-infra">PDU</span>')
    units.append('<span class="ru ru-infra">KVM</span>')
    for i in range(1, switches + 1):
        units.append(f'<span class="ru ru-sw">IB-SW{i}</span>')
    for i in range(1, compute + 1):
        units.append(f'<span class="ru ru-compute">DB{str(i).zfill(2)}</span>')
    for i in range(1, cells + 1):
        units.append(f'<span class="ru ru-cell">CEL{str(i).zfill(2)}</span>')

    html = f"""
    <div class="rack-container">
      <div class="rack-title">&#9661; RACK LAYOUT — {rack} · {cells} Storage Cells · {compute} Compute Nodes</div>
      <div class="rack-units">{''.join(units)}</div>
    </div>
    """
    return html


def step_done_key(lab, step_idx):
    return f"{lab}_{step_idx}"


def mark_step_done(lab, step_idx):
    key = step_done_key(lab, step_idx)
    if key not in st.session_state.steps_done:
        st.session_state.steps_done.add(key)
        st.session_state.steps_completed += 1
        st.session_state.score += 10


def get_progress():
    lab = st.session_state.current_lab
    steps = LABS[lab]["steps"]
    done = sum(1 for i in range(len(steps)) if step_done_key(lab, i) in st.session_state.steps_done)
    return done, len(steps)


def get_azure_client():
    """Build Azure OpenAI client from session state."""
    return AzureOpenAI(
        api_key=st.session_state.azure_api_key,
        azure_endpoint=st.session_state.azure_endpoint,
        api_version=st.session_state.azure_api_version,
    )


def stream_response(prompt: str):
    """Stream from Azure OpenAI and return full text."""
    if not st.session_state.azure_api_key:
        return "⚠️ Please enter your Azure OpenAI API key in the sidebar to use the simulator."

    try:
        client = get_azure_client()

        # Build messages list: system + last 16 turns
        messages = [{"role": "system", "content": system_prompt()}]
        for m in st.session_state.messages[-16:]:
            messages.append({"role": m["role"], "content": m["content"]})

        full_text = ""
        placeholder = st.empty()

        stream = client.chat.completions.create(
            model=st.session_state.azure_deployment,
            messages=messages,
            max_tokens=1500,
            temperature=0.4,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                full_text += chunk.choices[0].delta.content
                placeholder.markdown(
                    f'<div class="chat-assistant">{full_text}▌</div>',
                    unsafe_allow_html=True
                )

        placeholder.markdown(
            f'<div class="chat-assistant">{full_text}</div>',
            unsafe_allow_html=True
        )
        return full_text

    except Exception as e:
        err = str(e)
        if "401" in err or "authentication" in err.lower() or "api key" in err.lower():
            return "⚠️ Azure OpenAI authentication failed. Please check your API key and endpoint."
        elif "404" in err or "deployment" in err.lower():
            return f"⚠️ Deployment not found. Check your deployment name (current: `{st.session_state.azure_deployment}`)."
        elif "429" in err:
            return "⚠️ Rate limit reached. Please wait a moment and try again."
        return f"⚠️ Azure OpenAI Error: {err}"


def send_message(user_text: str, auto=False):
    """Add user message, call API, add assistant response."""
    st.session_state.messages.append({"role": "user", "content": user_text})
    if not auto:
        st.markdown(
            f'<div class="chat-user">{user_text}</div>',
            unsafe_allow_html=True
        )
    with st.spinner("ExaSimBot thinking..."):
        reply = stream_response(user_text)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    return reply


def trigger_step(lab_key, step_idx):
    """Build the prompt for a specific step and send it."""
    lab = LABS[lab_key]
    step = lab["steps"][step_idx]
    tag = step["tag"]
    instruction = STEP_PROMPTS[tag]

    prompt = f"""[LAB: {lab['title']}]
[STEP {step['n']}: {step['t']}]
[TYPE: {tag.upper()}]
[{env_context()}]

{instruction}"""

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner(f"Loading Step {step['n']}: {step['t']}..."):
        reply = stream_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    mark_step_done(lab_key, step_idx)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔴 Exadata X8M Simulator")

    # Azure OpenAI Config
    st.markdown("**Azure OpenAI Config**")

    azure_key = st.text_input(
        "API Key", type="password",
        value=st.session_state.azure_api_key,
        placeholder="Azure OpenAI API Key",
        label_visibility="visible"
    )
    if azure_key:
        st.session_state.azure_api_key = azure_key

    azure_endpoint = st.text_input(
        "Endpoint",
        value=st.session_state.azure_endpoint,
        placeholder="https://YOUR-RESOURCE.openai.azure.com/",
        label_visibility="visible"
    )
    if azure_endpoint:
        st.session_state.azure_endpoint = azure_endpoint

    azure_deployment = st.text_input(
        "Deployment Name",
        value=st.session_state.azure_deployment,
        placeholder="gpt-4.1",
        label_visibility="visible"
    )
    if azure_deployment:
        st.session_state.azure_deployment = azure_deployment

    azure_api_version = st.text_input(
        "API Version",
        value=st.session_state.azure_api_version,
        placeholder="2024-12-01-preview",
        label_visibility="visible"
    )
    if azure_api_version:
        st.session_state.azure_api_version = azure_api_version

    # Connection status indicator
    if st.session_state.azure_api_key:
        st.success("✅ Azure OpenAI configured")
    else:
        st.warning("⚠️ Enter API key to start")

    st.markdown("---")

    # Environment config
    st.markdown("**Environment Config**")
    rack = st.selectbox("Rack Size", ["1/8 Rack", "Quarter Rack", "Half Rack", "Full Rack"],
                        index=["1/8 Rack", "Quarter Rack", "Half Rack", "Full Rack"].index(st.session_state.rack))
    cells = st.selectbox("Storage Cells", [3, 7, 14, 18],
                         index=[3, 7, 14, 18].index(st.session_state.cells))
    compute = st.selectbox("Compute Nodes", [2, 4, 8],
                           index=[2, 4, 8].index(st.session_state.compute))
    dg = st.selectbox("ASM Disk Groups", ["DATA + RECO", "DATAC1 + RECOC1", "DATA + RECO + FLASH"],
                      index=["DATA + RECO", "DATAC1 + RECOC1", "DATA + RECO + FLASH"].index(st.session_state.dg))
    role = st.selectbox("Your Role", ["DBA", "DMA", "Both"],
                        index=["DBA", "DMA", "Both"].index(st.session_state.role))
    level = st.selectbox("Experience Level", ["Basic", "Intermediate", "Advanced"],
                         index=["Basic", "Intermediate", "Advanced"].index(st.session_state.level))

    if st.button("⚙️ Apply Config", use_container_width=True, type="primary"):
        st.session_state.rack = rack
        st.session_state.cells = cells
        st.session_state.compute = compute
        st.session_state.dg = dg
        st.session_state.role = role
        st.session_state.level = level
        st.session_state.messages = []
        st.session_state.steps_done = set()
        st.session_state.score = 0
        st.session_state.steps_completed = 0
        st.session_state.labs_started = 0
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"✅ **Environment configured!**\n\n"
                       f"- **Rack:** {rack}\n"
                       f"- **Storage Cells:** {cells}\n"
                       f"- **Compute Nodes:** {compute}\n"
                       f"- **ASM Disk Groups:** {dg}\n"
                       f"- **Role:** {role}\n"
                       f"- **Level:** {level}\n\n"
                       f"Session reset. Click any lab topic below to start your hands-on training!"
        })
        st.rerun()

    st.markdown("---")

    # Score metrics
    st.markdown("**Session Score**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Labs", st.session_state.labs_started)
    col2.metric("Steps", st.session_state.steps_completed)
    col3.metric("Score", st.session_state.score)

    st.markdown("---")

    # Lab navigation
    for group_name, lab_keys in LAB_GROUPS.items():
        st.markdown(f"**{group_name}**")
        for key in lab_keys:
            lab = LABS[key]
            done_steps = sum(1 for i in range(len(lab["steps"])) if step_done_key(key, i) in st.session_state.steps_done)
            total_steps = len(lab["steps"])
            label = f"{lab['icon']} {lab['title']}"
            if done_steps > 0:
                label += f" ({done_steps}/{total_steps})"

            is_current = st.session_state.current_lab == key
            btn_type = "primary" if is_current else "secondary"

            if st.button(label, key=f"lab_btn_{key}", use_container_width=True, type=btn_type):
                if st.session_state.current_lab != key:
                    st.session_state.current_lab = key
                    st.session_state.current_step = 0
                    st.session_state.labs_started += 1
                    st.session_state.messages = []
                    trigger_step(key, 0)
                    st.rerun()


# ── MAIN AREA ─────────────────────────────────────────────────────────────────

# Top banner
st.markdown("""
<div class="top-banner">
  <div>
    <div class="top-banner-logo">Oracle Exadata</div>
    <div class="top-banner-title">X8M DBA / DMA Hands-On Lab Simulator</div>
    <div class="top-banner-sub">Activity-based training with real commands, practice terminal & scored quizzes</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Rack visualizer
st.markdown(build_rack_html(), unsafe_allow_html=True)

# Current lab info
current_lab_data = LABS[st.session_state.current_lab]
done_count, total_count = get_progress()
progress_pct = int(done_count / total_count * 100) if total_count > 0 else 0

col_lab, col_prog = st.columns([3, 1])
with col_lab:
    st.markdown(f"#### {current_lab_data['icon']} {current_lab_data['title']}")
with col_prog:
    st.markdown(f"**Progress: {done_count}/{total_count} steps ({progress_pct}%)**")
    st.progress(progress_pct / 100)

# Steps + Chat layout
col_steps, col_chat = st.columns([1, 2.5])

# ── STEP CARDS ──
with col_steps:
    st.markdown("**Lab Steps**")
    steps = current_lab_data["steps"]

    for i, step in enumerate(steps):
        is_done = step_done_key(st.session_state.current_lab, i) in st.session_state.steps_done
        is_active = i == st.session_state.current_step

        tag_color = {"demo": "🔵", "lab": "🟢", "quiz": "🔴"}.get(step["tag"], "⚪")
        status_icon = "✅" if is_done else ("▶️" if is_active else f"{step['n']}.")

        btn_label = f"{status_icon} {step['t']} {tag_color}"

        if st.button(btn_label, key=f"step_{i}", use_container_width=True):
            st.session_state.current_step = i
            st.session_state.messages = []
            trigger_step(st.session_state.current_lab, i)
            st.rerun()

    st.markdown("---")
    # Quick action chips
    st.markdown("**Quick Actions**")
    if st.button("▶ Demo this step", use_container_width=True):
        send_message("Please demo this step with full commands and realistic Exadata output.")
        st.rerun()
    if st.button("⌨ Practice mode", use_container_width=True):
        send_message("I want to practice this step. Show me the exact command to type, then give me a practice exercise.")
        st.rerun()
    if st.button("? Quiz me", use_container_width=True):
        send_message("Quiz me on this topic with 3 MCQ questions. Score my answers.")
        st.rerun()
    if st.button("📖 Theory", use_container_width=True):
        send_message("Explain the theory and concepts behind this topic in depth.")
        st.rerun()
    if st.button("⚠ Common Errors", use_container_width=True):
        send_message("Show me common errors and how to troubleshoot them for this topic.")
        st.rerun()
    if st.button("🔄 Next Step →", use_container_width=True):
        next_step = min(st.session_state.current_step + 1, len(steps) - 1)
        st.session_state.current_step = next_step
        st.session_state.messages = []
        trigger_step(st.session_state.current_lab, next_step)
        st.rerun()

# ── CHAT AREA ──
with col_chat:
    st.markdown("**Lab Terminal & Chat**")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
<div class="chat-system">
ExaSimBot Online — Select a lab from the sidebar or click a step card to begin.
Use the Quick Actions on the left to Demo, Practice, or Quiz yourself on any step.
</div>
""", unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user" and not msg["content"].startswith("[LAB:"):
                    st.markdown(
                        f'<div class="chat-user">👤 {msg["content"]}</div>',
                        unsafe_allow_html=True
                    )
                elif msg["role"] == "assistant":
                    st.markdown(
                        f'<div class="chat-assistant">🤖 {msg["content"]}</div>',
                        unsafe_allow_html=True
                    )

    st.markdown("---")

    # Practice Terminal
    st.markdown("**Practice Terminal**")
    current_step_data = steps[st.session_state.current_step] if steps else None
    if current_step_data:
        tag = current_step_data["tag"]
        prompt_map = {
            "cellcli": "CellCLI>",
            "dcli": "$",
            "dbmcli": "DBMCLI>",
            "asm_dg": "SQL>",
            "disk_add": "CellCLI>",
            "griddisk": "CellCLI>",
            "acfs": "[root@exadb01]#",
            "acfs_db": "SQL>",
            "smart_scan": "SQL>",
            "hcc": "SQL>",
            "iorm": "CellCLI>",
            "flash": "CellCLI>",
            "rac": "$",
            "dg": "$",
            "patch": "$",
            "health": "$",
            "trouble": "$",
        }
        prompt_sym = prompt_map.get(st.session_state.current_lab, "$")

        pt_col1, pt_col2 = st.columns([4, 1])
        with pt_col1:
            cmd_input = st.text_input(
                f"{prompt_sym}",
                key="pt_input",
                placeholder=f"Type your command here and click Run...",
                label_visibility="visible"
            )
        with pt_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            run_clicked = st.button("▶ Run", type="primary", use_container_width=True)

        if run_clicked and cmd_input:
            eval_prompt = f"""[PRACTICE TERMINAL INPUT]
User typed: `{cmd_input}`
Context: Step {current_step_data['n']} — {current_step_data['t']} (Lab: {current_lab_data['title']})
{env_context()}

Evaluate in under 150 words:
1. Is this command correct for this step? 
2. Show the realistic Exadata output they would see
3. Say CORRECT ✓ (+10 pts) or WRONG ✗ with the correct command
Keep it concise and practical."""

            st.markdown(
                f'<div class="terminal-box">{prompt_sym} {cmd_input}</div>',
                unsafe_allow_html=True
            )
            send_message(eval_prompt, auto=True)
            mark_step_done(st.session_state.current_lab, st.session_state.current_step)
            st.rerun()

    # Free-text input
    st.markdown("**Ask anything**")
    user_input = st.chat_input("Ask a question about this lab, request more detail, or type your quiz answer...")
    if user_input:
        send_message(user_input)
        st.rerun()
