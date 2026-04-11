"""
exasim_core.py — Shared data and helpers for Exadata X8M Simulator.
Imported by Home (app.py) and pages/1_Lesson.py.
Only external imports: streamlit, openai.
"""
import streamlit as st
from openai import OpenAI

# =============================================================================
# RACK MODELS
# =============================================================================
RACK_SPECS = {
    "Eighth Rack":  {"compute": 2, "cells": 3,  "ib": 2},
    "Quarter Rack": {"compute": 2, "cells": 3,  "ib": 2},
    "Half Rack":    {"compute": 4, "cells": 7,  "ib": 2},
    "Full Rack":    {"compute": 8, "cells": 14, "ib": 3},
}

X8M_SPECS_TEXT = (
    "COMPUTE NODE (X8M-2): 2x Xeon Cascade Lake 8260 = 48 cores, up to 1.5TB DDR4, "
    "3.2TB Optane PMEM, 2x200Gb IB HDR, Oracle Linux 8. "
    "STORAGE CELL (X8M-2): 12x7.2TB HDD=86.4TB, 4x6.4TB NVMe=25.6TB, 1.5TB PMEM "
    "write-back, 2x200Gb IB HDR, cellsrv/MS/RS. "
    "IB FABRIC: 200 Gb/s HDR fat-tree, RDMA sub-microsecond latency."
)

# =============================================================================
# CURRICULUM — Utility-focused modules
# Each lesson carries all 7 sections: why / how / syntax / demo / practice /
# real-world / quiz. The AI trainer uses these seeds as context.
# =============================================================================
CURRICULUM = {
    "M0": {
        "title": "Exadata X8M Architecture Foundations",
        "icon": "🏛",
        "desc": "Start here. Understand the engineered system before touching any CLI.",
        "lessons": [
            {
                "id": "M0L1",
                "title": "What is Exadata & Why It Exists",
                "level": "Foundation",
                "why": "Commodity DB servers treat storage as dumb block devices, shipping TBs of blocks up the wire. Exadata pushes filtering INTO storage — 10–100× less I/O for analytics. Understanding this 'why' is the single most important thing before any command.",
                "how": "Three tiers connected by InfiniBand HDR: compute nodes (DB + Grid Infrastructure), storage cells (run Exadata Storage Server Software), and the IB fabric (RDMA). Smart Scan, Storage Indexes, HCC, and Smart Flash Cache only exist because of this co-design.",
                "syntax": "No commands yet — this is a concept lesson. You will see these later:\n  $ cellcli\n  $ dcli -g cellgroup -l root\n  SQL> SELECT * FROM v$cell;",
                "demo_prompt": "Explain with a concrete story: a 1TB SALES table with WHERE region='APAC'. Show what happens on commodity DB vs Exadata. Use the environment's actual cell count.",
                "practice": "Draw the 3-tier diagram on paper from memory. Label: compute, cells, IB switches, and the direction of Smart Scan data flow.",
                "quiz_topic": "Exadata core concepts: Smart Scan, offload, IB, engineered system",
                "real_world": "Customer migrating 80TB DWH from generic SAN + Linux. Why would Exadata cut their batch window from 8h to 45 min?",
            },
            {
                "id": "M0L2",
                "title": "Compute Node Anatomy (X8M-2 Server)",
                "level": "Foundation",
                "why": "You SSH here for 90% of DBA work. Know what's inside: CPU, RAM, PMEM, IB HCAs, Oracle Linux 8, Grid Infrastructure, ASM, RAC instances.",
                "how": "2×Xeon 8260 (48 cores), up to 1.5TB RAM, 3.2TB Optane PMEM, 2×200Gb IB HDR + 10GbE client + ILOM. Runs +ASMn and RAC DB instances. Hostnames typically exadb01..exadb0N.",
                "syntax": "$ ssh oracle@exadb01\n$ uname -a\n$ ipmitool -I lan -H exadb01-ilom -U root sensor\n$ olsnodes -n\n$ crsctl stat res -t",
                "demo_prompt": "SSH to exadb01, show hardware summary (cores, mem, IB), then verify cluster health across all compute nodes.",
                "practice": "Run crsctl stat res -t and identify every resource type (ora.asm, ora.ORCL.db, ora.LISTENER.lsnr).",
                "quiz_topic": "Compute node hardware, cluster resources, GI stack",
                "real_world": "exadb02 shows high load average. How do you triangulate: RAC gc waits? Kernel? DB session? Start by checking which layer.",
            },
            {
                "id": "M0L3",
                "title": "Storage Cell Anatomy (Exadata Storage Server)",
                "level": "Foundation",
                "why": "The cell is WHERE Exadata magic happens. Smart Scan, Storage Indexes, Flash Cache, PMEM accelerator — all live here. You never run DB instances on a cell.",
                "how": "12×7.2TB HDD (86.4TB raw) + 4×6.4TB NVMe (25.6TB flash) + 1.5TB Optane PMEM write-back log. Runs cellsrv (I/O engine), MS (management server), RS (restart server). Hostnames dm01cel01..dm01cel14.",
                "syntax": "# On the cell:\n$ cellcli\nCellCLI> list cell detail\nCellCLI> list physicaldisk\nCellCLI> list celldisk\nCellCLI> list flashcache detail",
                "demo_prompt": "Login to cel01 with cellcli, walk through physical disk → cell disk → grid disk hierarchy with real output.",
                "practice": "Explain the difference between physicaldisk, celldisk, griddisk, and ASM disk in one sentence each.",
                "quiz_topic": "Cell anatomy, cellsrv/MS/RS processes, storage hierarchy",
                "real_world": "cel03 shows one predictive failure disk. Will the DB see any impact? Why / why not?",
            },
            {
                "id": "M0L4",
                "title": "InfiniBand HDR & RDMA — The Secret Sauce",
                "level": "Foundation",
                "why": "RDMA is why Exadata OLTP is faster than anything on SAN. 19μs for a cached 8K read vs 200–500μs on fibre channel. Without IB, Exadata would be 'just a cluster with fast flash'.",
                "how": "200 Gb/s HDR per port, fat-tree topology. RDMA writes directly from remote RAM to local RAM, bypassing CPU/kernel. Every compute node has redundant paths to every cell.",
                "syntax": "$ ibstat\n$ ibhosts\n$ iblinkinfo\nCellCLI> list cell attributes rsStatus,msStatus,cellsrvStatus",
                "demo_prompt": "Show ibstat on a compute node. Identify link state, rate (200Gb HDR), and LID. Then show ibhosts listing all nodes.",
                "practice": "What's the output of ibstat if one HCA port is down? How would you spot it quickly?",
                "quiz_topic": "InfiniBand, RDMA, bandwidth, latency, topology",
                "real_world": "Latency suddenly jumped from 2ms to 50ms. First thing to check on the IB layer?",
            },
        ],
    },
    "M1": {
        "title": "CellCLI — The Cell Administrator's Shell",
        "icon": "🖥",
        "desc": "Primary tool for managing a single storage cell. Every DBA on Exadata must master this.",
        "lessons": [
            {
                "id": "M1L1",
                "title": "CellCLI Basics: Login, List, Describe",
                "level": "Basic",
                "why": "CellCLI is your 'SQL*Plus for the cell'. Everything — disks, flash, alerts, metrics — is queryable with a simple LIST verb. If you can't use CellCLI, you can't administer Exadata.",
                "how": "CellCLI is installed on every cell at /opt/oracle/cell/cellsrv/bin/cellcli. It talks to cellsrv via a local socket. Commands are verb-noun: LIST, CREATE, ALTER, DROP, DESCRIBE.",
                "syntax": "$ cellcli\nCellCLI> help\nCellCLI> list cell\nCellCLI> list cell detail\nCellCLI> describe cell\nCellCLI> list physicaldisk where status != normal",
                "demo_prompt": "Demo CellCLI from scratch: enter the shell, run list cell detail, then describe cell to show all attributes. Explain each attribute.",
                "practice": "List only physicaldisks where status is not 'normal'. What query would you write?",
                "quiz_topic": "CellCLI verbs, LIST/DESCRIBE syntax, WHERE clause filters",
                "real_world": "Morning check: which one CellCLI command tells you if the cell is healthy in 2 seconds?",
            },
            {
                "id": "M1L2",
                "title": "CellCLI Disk Hierarchy (Physical → Cell → Grid)",
                "level": "Basic",
                "why": "You cannot add capacity to ASM without understanding this chain. The three layers each serve a purpose: physical = hardware, cell = LUN abstraction, grid = ASM-facing slice.",
                "how": "physicaldisk → celldisk (one per physicaldisk, includes flash) → griddisk (slice of celldisk, presented to ASM). Grid disks always belong to a disk group (DATAC1, RECOC1).",
                "syntax": "CellCLI> list physicaldisk\nCellCLI> list celldisk attributes name,size,status\nCellCLI> list griddisk attributes name,asmDiskgroupName,size\nCellCLI> create celldisk all\nCellCLI> create griddisk all harddisk prefix=DATAC1 size=5T",
                "demo_prompt": "Walk through the hierarchy with live output. Show how one 7.2TB physical disk becomes a 7TB cell disk, then becomes 5TB DATAC1 + 2TB RECOC1 grid disks.",
                "practice": "Write the create griddisk command to allocate 4TB to DATAC1 from every hard disk on the cell.",
                "quiz_topic": "Hierarchy levels, size math, prefix naming, ASM linkage",
                "real_world": "You have 4TB free on each cell disk and need to add it to DATAC1. What's the full sequence?",
            },
            {
                "id": "M1L3",
                "title": "CellCLI Flash Cache & Flash Log",
                "level": "Medium",
                "why": "Flash Cache is why Exadata OLTP flies. If hit ratio drops below 90%, your latency suffers. Knowing how to inspect and re-create it is a bread-and-butter skill.",
                "how": "4×6.4TB NVMe flash on each cell becomes Smart Flash Cache (read+write-back) and Smart Flash Log (redo accelerator). Write-back mode means writes acknowledge when they hit flash, not HDD.",
                "syntax": "CellCLI> list flashcache detail\nCellCLI> list flashcachecontent where dbUniqueName='ORCL'\nCellCLI> list metriccurrent where name like 'FC_.*'\nCellCLI> drop flashcache\nCellCLI> create flashcache all size=20T",
                "demo_prompt": "Show flashcache detail with realistic output. Identify hit ratio, flashCacheMode, and size. Explain what write-back means.",
                "practice": "Current hit ratio is 72%. List three things you'd check in CellCLI before concluding the cache is too small.",
                "quiz_topic": "Flash cache modes, hit ratio, flash log, metrics",
                "real_world": "After a patch, flash cache shows size=0. What happened and how do you recover without downtime?",
            },
            {
                "id": "M1L4",
                "title": "CellCLI Metrics & Alert History",
                "level": "Medium",
                "why": "Exadata exposes hundreds of metrics via CellCLI. Learning to filter them is the difference between 'I don't know why it's slow' and 'cel04 has a failing disk, here's the alert'.",
                "how": "METRICCURRENT = real-time snapshot. METRICHISTORY = time-series. ALERTHISTORY = operational events. ACTIVEREQUEST = running I/O.",
                "syntax": "CellCLI> list metriccurrent where objectType='CELL_DISK' and name like 'CD_IO.*'\nCellCLI> list metrichistory where ageInMinutes < 60\nCellCLI> list alerthistory where severity='critical'\nCellCLI> list activerequest",
                "demo_prompt": "Show metriccurrent for cell disk I/O with realistic numbers. Then show three critical alerthistory entries.",
                "practice": "Write a metriccurrent query to find the 5 busiest cell disks right now.",
                "quiz_topic": "Metric types, filtering, alerthistory severity",
                "real_world": "Latency alert fired at 02:14. How do you pull the metric history for that exact minute and correlate?",
            },
        ],
    },
    "M2": {
        "title": "DCLI — Parallel Command Execution Across Cells",
        "icon": "⚡",
        "desc": "Run the same command on all 14 cells at once. Essential once you scale beyond one cell.",
        "lessons": [
            {
                "id": "M2L1",
                "title": "DCLI Fundamentals & Cell Groups",
                "level": "Basic",
                "why": "You have 14 cells. Running 'list cell detail' by SSHing to each is insane. DCLI fans out one command to all of them in parallel and consolidates output.",
                "how": "DCLI is a Python wrapper around SSH. It reads a cell group file (list of hostnames), opens parallel connections, and prefixes each line of output with the hostname.",
                "syntax": "$ cat /etc/oracle/cell/network-config/cellgroup\n$ dcli -g cellgroup -l root 'cellcli -e list cell'\n$ dcli -g cellgroup -l root 'imageinfo | grep -i version'\n$ dcli -g cellgroup -l root -x mycommand.sh",
                "demo_prompt": "Demo DCLI on the environment's cell count. Show the cellgroup file, run list cell across all cells, point out the hostname prefix on each line.",
                "practice": "Write a DCLI one-liner that lists all physicaldisks with non-normal status across every cell.",
                "quiz_topic": "DCLI syntax, cellgroup files, -x vs inline, -l user",
                "real_world": "You need to check imageinfo on all cells before a rolling patch. What's the one DCLI command?",
            },
            {
                "id": "M2L2",
                "title": "DCLI Passwordless SSH Setup",
                "level": "Medium",
                "why": "DCLI without passwordless SSH means typing the password 14 times per command. Setting up keys once saves hours per week.",
                "how": "dcli -k pushes your public SSH key to every host in the cellgroup. After that, DCLI runs silently.",
                "syntax": "$ ssh-keygen -t rsa -b 2048\n$ dcli -g cellgroup -l root -k\n$ dcli -g cellgroup -l root 'hostname'",
                "demo_prompt": "Demo the key-push workflow end to end. Show how dcli -k prompts for password once per cell, then passwordless thereafter.",
                "practice": "DCLI still asks for a password after running -k. What 3 things could be wrong?",
                "quiz_topic": "SSH keys, authorized_keys, permissions, dcli -k flag",
                "real_world": "New cell added to the rack. Shortest path to bring it into your DCLI group?",
            },
        ],
    },
    "M3": {
        "title": "ASM on Exadata — Diskgroups & Rebalance",
        "icon": "💾",
        "desc": "ASM is the DB's view of Exadata storage. Grid disks feed ASM disk groups with HIGH redundancy.",
        "lessons": [
            {
                "id": "M3L1",
                "title": "ASM Disk Groups: DATAC1, RECOC1, DBFS_DG",
                "level": "Basic",
                "why": "Everything the DB reads and writes flows through ASM. If ASM is misconfigured (wrong redundancy, wrong AU size), you lose Exadata's fault tolerance.",
                "how": "Oracle recommends DATAC1 (database files, HIGH), RECOC1 (FRA, NORMAL), DBFS_DG (OCR/voting). Grid disks from all cells are striped across the disk group.",
                "syntax": "$ sqlplus / as sysasm\nSQL> SELECT name, state, type, total_mb/1024/1024 tb FROM v$asm_diskgroup;\nSQL> SELECT path, state FROM v$asm_disk WHERE group_number=1;\n$ asmcmd lsdg\n$ asmcmd lsdsk -k",
                "demo_prompt": "Log in as sysasm, show v$asm_diskgroup, then show how many disks belong to DATAC1 and from how many distinct cells.",
                "practice": "Query v$asm_disk to confirm DATAC1 has failgroups from every cell (important for HIGH redundancy).",
                "quiz_topic": "Disk groups, redundancy levels, failgroups, AU size",
                "real_world": "DATAC1 shows REQUIRED_MIRROR_FREE_MB > USABLE_FILE_MB. What does that mean, and is it safe?",
            },
            {
                "id": "M3L2",
                "title": "Adding Grid Disks to Expand DATAC1",
                "level": "Medium",
                "why": "Capacity exhaustion is the #1 operational issue. You must know the end-to-end sequence: CellCLI create griddisk → ASM alter diskgroup add disk → monitor rebalance.",
                "how": "Rebalance is online. Power level (1–11) controls speed vs impact. V$ASM_OPERATION shows progress.",
                "syntax": "-- On each cell:\nCellCLI> create griddisk all harddisk prefix=DATAC1 size=500G\n-- On ASM:\nSQL> ALTER DISKGROUP DATAC1 ADD DISK 'o/*/DATAC1_*' REBALANCE POWER 4;\nSQL> SELECT * FROM v$asm_operation;",
                "demo_prompt": "Full walk-through: create grid disks on 2 cells, add them to DATAC1, watch rebalance progress. Show realistic v$asm_operation output.",
                "practice": "YOUR TURN — write the ALTER DISKGROUP command for the environment's DG naming convention.",
                "quiz_topic": "Rebalance, power level, v$asm_operation, disk discovery string",
                "real_world": "Rebalance is running at power 6 and users are complaining. What's the safest way to reduce impact without stopping it?",
            },
        ],
    },
    "M4": {
        "title": "RMAN on Exadata — Backup to ZDLRA or FRA",
        "icon": "🛡",
        "desc": "Exadata backups are faster (Smart Scan + PMEM) but follow the same RMAN principles.",
        "lessons": [
            {
                "id": "M4L1",
                "title": "RMAN Incremental Strategy on Exadata",
                "level": "Medium",
                "why": "Full backups of a 50TB DB are impractical daily. Incremental level 1 + block change tracking brings nightly backup to minutes.",
                "how": "Exadata's Smart Incremental uses storage-side block filtering: cells skip unchanged blocks. BCT file tracks changed blocks since last level 0.",
                "syntax": "SQL> ALTER DATABASE ENABLE BLOCK CHANGE TRACKING\n     USING FILE '+RECOC1/ORCL/bct.dbf';\n$ rman target /\nRMAN> BACKUP INCREMENTAL LEVEL 1 DATABASE PLUS ARCHIVELOG;\nRMAN> LIST BACKUP SUMMARY;",
                "demo_prompt": "Enable BCT, run a level-1 backup, show the speedup vs a full backup. Explain the Smart Incremental benefit.",
                "practice": "Write the RMAN script for a weekly level-0 + daily level-1 schedule.",
                "quiz_topic": "BCT, level 0 vs 1, Smart Incremental, FRA",
                "real_world": "Level-1 backup suddenly takes 4x longer. BCT file corruption is suspected. How do you verify and recover?",
            },
        ],
    },
    "M5": {
        "title": "SRVCTL & CRSCTL — RAC Cluster Management",
        "icon": "🔗",
        "desc": "Manage cluster resources, DB instances, services, and listeners.",
        "lessons": [
            {
                "id": "M5L1",
                "title": "SRVCTL: Start, Stop, Status of DB Resources",
                "level": "Basic",
                "why": "Never use 'sqlplus > shutdown' on RAC. Always use srvctl so the cluster registry stays consistent and dependencies are respected.",
                "how": "srvctl talks to CRSD which manages the OCR. Every DB, instance, service, listener, and ASM has a cluster resource.",
                "syntax": "$ srvctl status database -d ORCL\n$ srvctl stop instance -d ORCL -i ORCL1\n$ srvctl start database -d ORCL\n$ srvctl config database -d ORCL\n$ srvctl status service -d ORCL",
                "demo_prompt": "Show status of all DB instances on the environment's compute nodes. Then stop one instance, show status, start it back.",
                "practice": "Stop only instance ORCL2 without affecting other instances. What's the command?",
                "quiz_topic": "srvctl verbs, -d/-i flags, services vs instances",
                "real_world": "Instance ORCL3 shows OFFLINE in srvctl but 'ps -ef' shows pmon running. What do you do?",
            },
            {
                "id": "M5L2",
                "title": "CRSCTL: Cluster Stack Control",
                "level": "Medium",
                "why": "crsctl is the cluster-level equivalent of srvctl. You use it to check/start/stop the whole Grid Infrastructure stack and inspect voting disks.",
                "how": "crsctl runs as root (or grid) and manages the CRS/CSS/EVM daemons below srvctl's layer.",
                "syntax": "$ crsctl check cluster -all\n$ crsctl stat res -t\n$ crsctl query css votedisk\n$ crsctl stop crs  # requires root, drastic",
                "demo_prompt": "Run crsctl check cluster -all across all nodes. Then show crsctl stat res -t and decode each resource type.",
                "practice": "Which crsctl command shows voting disks, and why do you care if only 2 of 3 are online?",
                "quiz_topic": "crsctl vs srvctl, voting disk, cluster stack layers",
                "real_world": "Node 2 can't join the cluster after reboot. First three crsctl commands you run?",
            },
        ],
    },
    "M6": {
        "title": "Data Guard on Exadata (DGMGRL)",
        "icon": "🔄",
        "desc": "Physical standby, switchover, failover — Exadata's HA story for disaster recovery.",
        "lessons": [
            {
                "id": "M6L1",
                "title": "DGMGRL Basics: Show Configuration & Database",
                "level": "Medium",
                "why": "Before any DG operation, you must know the current state. DGMGRL is the CLI that queries the broker config and reports health.",
                "how": "DGMGRL connects to the broker process on the primary or standby. Configuration holds both databases, protection mode, transport mode.",
                "syntax": "$ dgmgrl sys/password@ORCL_PRI\nDGMGRL> show configuration\nDGMGRL> show database ORCL_STBY\nDGMGRL> show database ORCL_STBY 'StatusReport'",
                "demo_prompt": "Connect to DGMGRL, show configuration, then show database for both members. Decode every line of output.",
                "practice": "What does 'Transport Lag' vs 'Apply Lag' tell you? Which is worse to ignore?",
                "quiz_topic": "Broker, lag types, protection modes, validate database",
                "real_world": "show configuration returns 'WARNING: ORA-16853'. First thing to check?",
            },
            {
                "id": "M6L2",
                "title": "Graceful Switchover",
                "level": "Advanced",
                "why": "Planned DR failover tests, DC maintenance, or patching sequence — all require a switchover without data loss.",
                "how": "Broker coordinates: primary flushes redo, becomes standby, standby applies final redo, becomes primary. Takes 60s–5min depending on lag.",
                "syntax": "DGMGRL> validate database ORCL_STBY\nDGMGRL> switchover to ORCL_STBY\nDGMGRL> show configuration",
                "demo_prompt": "Full switchover demo with realistic output. Show validate → switchover → post-verify. Include how long each step takes.",
                "practice": "Before running switchover, what 3 validate checks must all pass?",
                "quiz_topic": "Switchover steps, validate, failover vs switchover",
                "real_world": "Switchover hangs at 'Converting primary database'. What do you check first?",
            },
        ],
    },
    "M7": {
        "title": "Smart Scan & Performance Tuning",
        "icon": "🚀",
        "desc": "The feature that justifies Exadata's price. Verify it's working; fix it when it's not.",
        "lessons": [
            {
                "id": "M7L1",
                "title": "Verifying Smart Scan is Actually Used",
                "level": "Advanced",
                "why": "Smart Scan is not automatic. Bind variables, function indexes, PL/SQL functions in WHERE, and wrong hints can silently disable it. A query may 'look like' it's offloading but actually runs on the compute node.",
                "how": "Check V$SQL.IO_CELL_OFFLOAD_ELIGIBLE_BYTES and IO_CELL_OFFLOAD_RETURNED_BYTES. Also: cell_physical_IO_bytes_saved_by_storage_index in session stats.",
                "syntax": "SQL> SELECT sql_id, io_cell_offload_eligible_bytes elig,\n            io_cell_offload_returned_bytes ret,\n            (1 - ret/NULLIF(elig,0))*100 AS savings_pct\n       FROM v$sql WHERE sql_id = :sqlid;\nSQL> SELECT name, value FROM v$mystat m JOIN v$statname n USING(statistic#)\n     WHERE name LIKE 'cell%';",
                "demo_prompt": "Run a full table scan query, then show v$sql offload stats. Contrast a query that IS offloaded vs one that is NOT (e.g., has a PL/SQL function in WHERE).",
                "practice": "A query has elig=50GB, ret=48GB. Is Smart Scan working well? Why or why not?",
                "quiz_topic": "Offload stats, storage index, blockers of Smart Scan",
                "real_world": "Analytic query that used to run in 30s now takes 12 minutes. You suspect Smart Scan broke. What's your diagnostic sequence?",
            },
        ],
    },
    "M8": {
        "title": "Incident Response & Troubleshooting",
        "icon": "🚨",
        "desc": "Real-world scenarios: cell failure, IB link down, runaway workload, rolling patch gone wrong.",
        "lessons": [
            {
                "id": "M8L1",
                "title": "Cell Failure with HIGH Redundancy",
                "level": "Advanced",
                "why": "A storage cell can die at 3 AM. If DATAC1 is HIGH redundancy, the DB stays up — but only if you know how to respond and rebuild.",
                "how": "ASM auto-drops offline disks after DISK_REPAIR_TIME (default 3.6h). You must replace the cell, recreate celldisks/griddisks, and re-add to ASM.",
                "syntax": "-- Confirm cell is down\nCellCLI> list cell\n-- ASM side\nSQL> SELECT path, mode_status FROM v$asm_disk WHERE mode_status='OFFLINE';\nSQL> ALTER DISKGROUP DATAC1 OFFLINE DISKS IN FAILGROUP dm01cel03;\n-- After replacement\nCellCLI> create celldisk all\nCellCLI> create griddisk all harddisk prefix=DATAC1",
                "demo_prompt": "Full incident walk-through. Start with alerts firing, diagnose which cell is down, show ASM behavior, walk through replacement and rebuild.",
                "practice": "DISK_REPAIR_TIME is 3.6h. Cell has been down for 2h. What's your call: push repair time up or start the rebuild?",
                "quiz_topic": "HIGH redundancy, DISK_REPAIR_TIME, rebuild sequence, rebalance",
                "real_world": "Two cells offline simultaneously. DATAC1 is HIGH (can tolerate 2 failures). Are you safe?",
            },
        ],
    },
}

# =============================================================================
# CSS — shared by all pages
# =============================================================================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono&display=swap');

.stApp {
    background: radial-gradient(ellipse at top, #081424 0%, #04080f 100%);
    color: #c8dff8;
    font-family: 'Rajdhani', sans-serif;
}
h1, h2, h3, h4 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 1.2px; }

.brand-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 26px; font-weight: 700; letter-spacing: 3px;
    background: linear-gradient(90deg, #e74c3c, #f39c12);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.brand-sub { color: #6a8faa; font-size: 12px; letter-spacing: 2px; margin-top: 2px; }

.panel {
    background: #0a1220; border: 1px solid #1a2c47; border-radius: 10px;
    padding: 18px; margin-bottom: 14px;
}
.panel-title {
    font-family: 'Orbitron', sans-serif; color: #f39c12;
    font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
    border-bottom: 1px solid #1a2c47; padding-bottom: 8px; margin-bottom: 12px;
}

.module-card {
    background: linear-gradient(135deg, #0f1a2e 0%, #0a1220 100%);
    border: 1px solid #1a2c47; border-left: 4px solid #c0392b;
    border-radius: 8px; padding: 16px; margin-bottom: 12px;
    transition: all 0.2s;
}
.module-card:hover { border-left-color: #f39c12; }
.module-card h3 {
    color: #e74c3c !important; font-size: 15px !important;
    margin: 0 0 4px 0 !important; letter-spacing: 1px !important;
}
.module-card .mdesc { color: #8ab4d8; font-size: 13px; }
.module-card .mcount { color: #f39c12; font-size: 11px; font-family: 'Share Tech Mono', monospace; margin-top: 6px; }

.lesson-row {
    background: #0f1a2e; border-left: 3px solid #0088ff;
    padding: 10px 14px; border-radius: 4px; margin: 6px 0;
    display: flex; justify-content: space-between; align-items: center;
}
.lesson-row .lid { color: #f39c12; font-family: 'Share Tech Mono', monospace;
                    font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.lesson-row .ltitle { color: #c8dff8; font-weight: 600; font-size: 14px; }
.level-Foundation { background:#8844ff22; color:#c8a0ff; padding:2px 10px; border-radius:10px; font-size:10px; letter-spacing:1px; }
.level-Basic      { background:#00ff8822; color:#00ff88; padding:2px 10px; border-radius:10px; font-size:10px; letter-spacing:1px; }
.level-Medium     { background:#0088ff22; color:#66c2ff; padding:2px 10px; border-radius:10px; font-size:10px; letter-spacing:1px; }
.level-Advanced   { background:#f39c1222; color:#f39c12; padding:2px 10px; border-radius:10px; font-size:10px; letter-spacing:1px; }

.metric-pill {
    display: inline-block; background: #0f1a2e; border: 1px solid #1a2c47;
    padding: 5px 11px; border-radius: 12px; font-family: 'Share Tech Mono', monospace;
    font-size: 11px; color: #c8dff8; margin: 3px 4px 3px 0;
}
.metric-pill .v { color: #00ff88; font-weight: 700; }

.section-header {
    font-family: 'Orbitron', sans-serif; color: #f39c12;
    font-size: 13px; letter-spacing: 2px; text-transform: uppercase;
    margin: 18px 0 8px 0; padding-bottom: 6px;
    border-bottom: 1px solid #1a2c47;
}
.section-header::before { content: '▸ '; color: #c0392b; }

.why-box {
    background: #2a1a0a; border-left: 3px solid #f39c12;
    padding: 12px 16px; border-radius: 4px; color: #ffd580;
    font-size: 14px; line-height: 1.6;
}
.how-box {
    background: #0a1a2a; border-left: 3px solid #0088ff;
    padding: 12px 16px; border-radius: 4px; color: #a8d0f0;
    font-size: 14px; line-height: 1.6;
}
.syntax-box {
    background: #030a14; border: 1px solid #1a4a2a;
    padding: 12px 16px; border-radius: 4px;
    font-family: 'Share Tech Mono', monospace; color: #00ff88;
    font-size: 13px; white-space: pre-wrap; line-height: 1.55;
}
.real-box {
    background: #1a0a12; border-left: 3px solid #c0392b;
    padding: 12px 16px; border-radius: 4px; color: #f0b0a0;
    font-size: 14px; line-height: 1.6;
}

.stButton > button {
    background: linear-gradient(90deg, #c0392b, #e74c3c);
    color: white !important; border: none; font-family: 'Rajdhani', sans-serif;
    font-weight: 700; letter-spacing: 1px; border-radius: 6px;
    padding: 6px 18px;
}
.stButton > button:hover { background: linear-gradient(90deg, #e74c3c, #f39c12); }

div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stRadio"] label {
    color: #6a8faa !important; font-size: 11px !important;
    text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600;
}

/* Hide default Streamlit chrome that clutters the look */
#MainMenu, footer { visibility: hidden; }
</style>
"""

# =============================================================================
# SESSION STATE DEFAULTS
# =============================================================================
DEFAULTS = {
    "openai_key": "",
    "openai_model": "gpt-4o",
    "rack": "Half Rack",
    "dg": "DATAC1+RECOC1",
    "role": "DBA",
    "level": "Intermediate",
    "active_lesson_id": None,
    "chat": {},           # {lesson_id: [msgs]}
    "quiz_state": {},     # {lesson_id: {score, answered}}
    # Playground state
    "pg_scores": {},      # {category: {correct:0, partial:0, wrong:0, pts:0}}
    "pg_total_pts": 0,
    "pg_history": [],     # [{id, cmd, verdict, pts, ts}]
    "pg_ex_id": None,     # currently selected exercise id
    "pg_result": {},      # {ex_id: {verdict, feedback, simulated_output, pts, correct_cmd}}
    "pg_hints_shown": {}, # {ex_id: 0|1|2}
    "pg_free_hist": [],   # free-practice terminal history
}

def init_state():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v
    # Try to pre-fill key from secrets
    try:
        if not st.session_state.openai_key:
            st.session_state.openai_key = st.secrets.get("openai_key", "")
    except Exception:
        pass

def find_lesson(lesson_id):
    for mkey, mod in CURRICULUM.items():
        for lesson in mod["lessons"]:
            if lesson["id"] == lesson_id:
                return mkey, mod, lesson
    return None, None, None

# =============================================================================
# DYNAMIC ARCHITECTURE DIAGRAM
# =============================================================================
def build_diagram(compute, cells, ib, rack_name):
    W, H = 900, 520
    cw = min(110, (W - 80) // max(compute, 1) - 14)
    cw_total = compute * (cw + 14) - 14
    cx0 = (W - cw_total) // 2
    cy, ch = 70, 55

    iw = 150
    iw_total = ib * (iw + 24) - 24
    ix0 = (W - iw_total) // 2
    iy, ih = 200, 44

    sw = min(90, (W - 80) // max(cells, 1) - 10)
    sw_total = cells * (sw + 10) - 10
    sx0 = (W - sw_total) // 2
    sy, sh = 310, 72

    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">']
    s.append('''<defs>
      <linearGradient id="gc" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0a4a8a"/><stop offset="100%" stop-color="#062547"/></linearGradient>
      <linearGradient id="gs" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#005a35"/><stop offset="100%" stop-color="#002818"/></linearGradient>
      <linearGradient id="gi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#4a2288"/><stop offset="100%" stop-color="#1e0a42"/></linearGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="2.5"/></filter>
    </defs>''')

    s.append(f'<rect x="0" y="0" width="{W}" height="32" fill="#0a1220"/>')
    s.append(f'<text x="{W//2}" y="21" text-anchor="middle" font-family="Orbitron" '
             f'font-size="13" fill="#f39c12" letter-spacing="3">'
             f'[ {rack_name.upper()} — {compute} COMPUTE • {cells} CELLS • {ib} IB HDR ]</text>')

    s.append('<text x="20" y="60" font-family="Rajdhani" font-size="11" fill="#6a8faa" letter-spacing="2">DATABASE TIER (X8M-2)</text>')
    s.append('<text x="20" y="190" font-family="Rajdhani" font-size="11" fill="#6a8faa" letter-spacing="2">INFINIBAND HDR FABRIC — 200 Gb/s</text>')
    s.append('<text x="20" y="300" font-family="Rajdhani" font-size="11" fill="#6a8faa" letter-spacing="2">STORAGE TIER (X8M-2 CELLS)</text>')

    comp_centers = []
    for i in range(compute):
        x = cx0 + i * (cw + 14)
        cxc = x + cw // 2
        comp_centers.append((cxc, cy + ch))
        s.append(f'<rect x="{x}" y="{cy}" width="{cw}" height="{ch}" rx="5" fill="url(#gc)" stroke="#0088ff" stroke-width="1.5"/>')
        s.append(f'<text x="{cxc}" y="{cy+20}" text-anchor="middle" font-family="Orbitron" font-size="11" fill="#66c2ff" font-weight="700">exadb0{i+1}</text>')
        s.append(f'<text x="{cxc}" y="{cy+35}" text-anchor="middle" font-family="Share Tech Mono" font-size="9" fill="#c8dff8">48c • 1.5TB</text>')
        s.append(f'<text x="{cxc}" y="{cy+47}" text-anchor="middle" font-family="Share Tech Mono" font-size="8" fill="#8ab4d8">+ASM{i+1} ORCL{i+1}</text>')
        s.append(f'<circle cx="{x+8}" cy="{cy+8}" r="3" fill="#00ff88"><animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>')

    ib_centers = []
    for i in range(ib):
        x = ix0 + i * (iw + 24)
        ixc = x + iw // 2
        ib_centers.append((ixc, iy, iy + ih))
        s.append(f'<rect x="{x}" y="{iy}" width="{iw}" height="{ih}" rx="4" fill="url(#gi)" stroke="#8844ff" stroke-width="1.5"/>')
        s.append(f'<text x="{ixc}" y="{iy+18}" text-anchor="middle" font-family="Orbitron" font-size="11" fill="#c8a0ff" font-weight="700">IB HDR SW{i+1}</text>')
        s.append(f'<text x="{ixc}" y="{iy+33}" text-anchor="middle" font-family="Share Tech Mono" font-size="9" fill="#c8dff8">200 Gb/s • RDMA</text>')

    cell_centers = []
    for i in range(cells):
        x = sx0 + i * (sw + 10)
        sxc = x + sw // 2
        cell_centers.append((sxc, sy))
        s.append(f'<rect x="{x}" y="{sy}" width="{sw}" height="{sh}" rx="4" fill="url(#gs)" stroke="#00ff88" stroke-width="1.2"/>')
        s.append(f'<text x="{sxc}" y="{sy+16}" text-anchor="middle" font-family="Orbitron" font-size="10" fill="#66ffb0" font-weight="700">cel{str(i+1).zfill(2)}</text>')
        s.append(f'<text x="{sxc}" y="{sy+32}" text-anchor="middle" font-family="Share Tech Mono" font-size="8" fill="#c8dff8">86.4TB HDD</text>')
        s.append(f'<text x="{sxc}" y="{sy+45}" text-anchor="middle" font-family="Share Tech Mono" font-size="8" fill="#c8dff8">25.6TB NVMe</text>')
        s.append(f'<text x="{sxc}" y="{sy+58}" text-anchor="middle" font-family="Share Tech Mono" font-size="7" fill="#8ab4d8">1.5TB PMEM</text>')
        s.append(f'<circle cx="{x+8}" cy="{sy+8}" r="2.5" fill="#00ff88"><animate attributeName="opacity" values="1;0.2;1" dur="{1.5+i*0.1}s" repeatCount="indefinite"/></circle>')

    for cxc, cyc in comp_centers:
        for ixc, iyt, _ in ib_centers:
            s.append(f'<line x1="{cxc}" y1="{cyc}" x2="{ixc}" y2="{iyt}" stroke="#8844ff" stroke-width="1" stroke-opacity="0.5"/>')
    for ixc, _, iyb in ib_centers:
        for sxc, syt in cell_centers:
            s.append(f'<line x1="{ixc}" y1="{iyb}" x2="{sxc}" y2="{syt}" stroke="#8844ff" stroke-width="0.8" stroke-opacity="0.35"/>')

    for k in range(min(4, compute)):
        c = comp_centers[k % len(comp_centers)]
        ibx, iyt, iyb = ib_centers[k % len(ib_centers)]
        cc = cell_centers[(k * 2) % len(cell_centers)]
        path = f"M{c[0]},{c[1]} L{ibx},{iyt} L{ibx},{iyb} L{cc[0]},{cc[1]}"
        s.append(f'<circle r="3.5" fill="#f39c12" filter="url(#glow)"><animateMotion dur="{2+k*0.4}s" repeatCount="indefinite" path="{path}"/></circle>')

    total_hdd = cells * 86.4
    total_flash = cells * 25.6
    hdd_str = f"{total_hdd/1000:.2f}PB" if total_hdd >= 1000 else f"{total_hdd:.0f}TB"
    s.append(f'<rect x="0" y="{H-30}" width="{W}" height="30" fill="#0a1220"/>')
    s.append(f'<text x="20" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#00ff88">● CLUSTER: ONLINE</text>')
    s.append(f'<text x="180" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#c8dff8">ASM RAW: {hdd_str}</text>')
    s.append(f'<text x="360" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#f39c12">FLASH: {total_flash:.1f}TB</text>')
    s.append(f'<text x="530" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#8844ff">IB: {ib}× 200Gb HDR</text>')
    s.append(f'<text x="700" y="{H-11}" font-family="Share Tech Mono" font-size="10" fill="#c8dff8">CORES: {compute*48}</text>')
    s.append('</svg>')
    return "".join(s)

# =============================================================================
# AI SYSTEM PROMPT
# =============================================================================
def system_prompt(lesson=None, mode="chat"):
    specs = RACK_SPECS[st.session_state.rack]
    env = (f"Rack={st.session_state.rack}, Cells={specs['cells']}, "
           f"Compute={specs['compute']}, IB={specs['ib']}, "
           f"DGs={st.session_state.dg}, Role={st.session_state.role}, "
           f"Level={st.session_state.level}")

    lesson_block = ""
    if lesson:
        lesson_block = (
            f"\nCURRENT LESSON: {lesson['id']} — {lesson['title']} [{lesson['level']}]\n"
            f"Module context. Tailor every answer to THIS lesson's topic only.\n"
            f"Why this matters: {lesson['why']}\n"
            f"How it works: {lesson['how']}\n"
            f"Quiz topic (if mode=quiz): {lesson['quiz_topic']}\n"
        )

    mode_rules = {
        "chat": "Answer questions about the current lesson. Be concrete and practical.",
        "demo": "Produce a DEMO: walk through the commands step-by-step with realistic simulated Exadata output after each. Explain what each line means. End with a summary.",
        "practice": "EVALUATE the user's typed command. In ≤150 words: is it correct for this lesson? Show realistic simulated output. End with CORRECT ✓ (+10 pts) or WRONG ✗ and the right command.",
        "quiz": "Generate a MCQ quiz: 3 questions, A/B/C/D options, one correct answer per question. Present ONE question at a time. After the user answers, say CORRECT ✓ or WRONG ✗ with a one-sentence explanation, then move to the next. After Q3, show final score.",
        "scenario": "Play out a realistic real-world incident scenario based on this lesson. Present symptoms first, ask the user to diagnose. Guide them step-by-step.",
    }

    return f"""You are ExaSimBot — Oracle Exadata X8M Senior DBA Trainer (15+ years experience).
Direct, practical, technical. No fluff. No marketing speak.

ENVIRONMENT: {env}
{lesson_block}
MODE: {mode} — {mode_rules.get(mode, mode_rules['chat'])}

GLOBAL RULES:
1. Commands ALWAYS in triple-backtick code blocks with correct prompt prefix:
   CellCLI>, SQL>, DGMGRL>, asmcmd> , $, #
2. Show realistic simulated Exadata output after every command.
3. Depth by Level: Basic=concepts+syntax, Intermediate=full procedure, Advanced=internals+edge cases.
4. Role focus: DBA=SQL/ASM/RMAN/srvctl/DGMGRL; DMA=hardware/ILOM/patchmgr/firmware.
5. Never invent features. If unsure, say so.
6. Max 600 words per response.

X8M SPECS (use in examples): {X8M_SPECS_TEXT}
"""

# =============================================================================
# OPENAI CALL HELPERS
# =============================================================================
def get_client():
    if not st.session_state.openai_key:
        return None
    return OpenAI(api_key=st.session_state.openai_key)

def stream_response(client, messages, placeholder):
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
    return full
