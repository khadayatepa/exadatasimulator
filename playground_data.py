"""
playground_data.py — DBA Playground Exercise Bank
50 hands-on exercises across 9 categories, Basic → Advanced.
Each exercise has a scenario, task, progressive hints, and correct command reference.
"""

PLAYGROUND_EXERCISES = [

    # =========================================================
    # CATEGORY: CellCLI — Basic
    # =========================================================
    {
        "id": "PG001", "category": "CellCLI", "level": "Basic",
        "title": "Launch CellCLI",
        "scenario": (
            "You've just SSH'd to storage cell dm01cel01 as root. "
            "You need to enter the cell administration shell to begin your morning check."
        ),
        "task": "Type the command to launch the Cell Command Line Interface.",
        "hints": [
            "It is a standalone binary, usually in your PATH.",
            "The command is simply: cellcli",
        ],
        "context": "$",
        "ref_command": "cellcli",
        "explanation": (
            "`cellcli` launches the Cell CLI. The binary is at "
            "/opt/oracle/cell/cellsrv/bin/cellcli but is on the default root PATH."
        ),
        "tags": ["cellcli", "basics", "login"],
    },
    {
        "id": "PG002", "category": "CellCLI", "level": "Basic",
        "title": "Check Cell Health (1 command)",
        "scenario": (
            "You are at the CellCLI prompt on dm01cel01. "
            "It's 07:00 AM and you want the fastest single command that shows overall cell health."
        ),
        "task": "Show all cell attributes including status and service states.",
        "hints": [
            "Use the LIST verb on the CELL object.",
            "Add DETAIL to see all attributes: `LIST CELL DETAIL`",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST CELL DETAIL",
        "explanation": (
            "`LIST CELL DETAIL` returns every attribute: cellsrvStatus, msStatus, rsStatus, "
            "releaseVersion, flashCacheMode — the full morning-check snapshot in one shot."
        ),
        "tags": ["cellcli", "health-check", "basics"],
    },
    {
        "id": "PG003", "category": "CellCLI", "level": "Basic",
        "title": "List Physical Disks with Filters",
        "scenario": (
            "cel04 triggered an alert overnight. You want to see only physical disks "
            "that are NOT in 'normal' status."
        ),
        "task": "Write a CellCLI command to list only non-normal physical disks.",
        "hints": [
            "Use LIST PHYSICALDISK with a WHERE clause.",
            "Filter: `WHERE status != 'normal'`",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST PHYSICALDISK WHERE status != 'normal'",
        "explanation": (
            "CellCLI supports SQL-like WHERE clauses. This filters out all healthy disks "
            "so you see only predictivefailure, failed, or missing disks."
        ),
        "tags": ["cellcli", "physicaldisk", "filtering", "basics"],
    },
    {
        "id": "PG004", "category": "CellCLI", "level": "Basic",
        "title": "Describe CellDisk Object",
        "scenario": (
            "A junior DBA asks what attributes are available on a celldisk object. "
            "You want to show them without running a Google search."
        ),
        "task": "Use CellCLI to show all available attributes for the CELLDISK object type.",
        "hints": [
            "There's a verb specifically for introspection.",
            "Syntax: `DESCRIBE <object_type>`",
        ],
        "context": "CellCLI>",
        "ref_command": "DESCRIBE CELLDISK",
        "explanation": (
            "`DESCRIBE CELLDISK` lists every attribute name and its type — like `DESC` in SQL*Plus. "
            "Useful when you forget an attribute name for a WHERE clause."
        ),
        "tags": ["cellcli", "celldisk", "describe", "basics"],
    },
    {
        "id": "PG005", "category": "CellCLI", "level": "Basic",
        "title": "List Cell Disks (name + size + status)",
        "scenario": (
            "You need a quick inventory of all cell disks on this cell with just "
            "the name, size, and status columns — not all attributes."
        ),
        "task": "List cell disks showing only: name, size, and status.",
        "hints": [
            "Use `LIST CELLDISK ATTRIBUTES ...`",
            "Separate attribute names with commas: `ATTRIBUTES name,size,status`",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST CELLDISK ATTRIBUTES name,size,status",
        "explanation": (
            "The ATTRIBUTES keyword projects only the columns you need. "
            "Saves screen space and speeds up parsing when scripting."
        ),
        "tags": ["cellcli", "celldisk", "attributes", "basics"],
    },
    {
        "id": "PG006", "category": "CellCLI", "level": "Basic",
        "title": "List Grid Disks for DATAC1",
        "scenario": (
            "ASM reported a disk discovery issue. You want to see all grid disks "
            "on this cell that belong to the DATAC1 disk group."
        ),
        "task": "List all grid disks where the ASM disk group name is DATAC1.",
        "hints": [
            "Use LIST GRIDDISK with a WHERE clause on asmDiskgroupName.",
            "Filter: `WHERE asmDiskgroupName = 'DATAC1'`",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST GRIDDISK WHERE asmDiskgroupName = 'DATAC1'",
        "explanation": (
            "Grid disks are the slices presented to ASM. Filtering by asmDiskgroupName "
            "quickly confirms all expected disks are present in DATAC1."
        ),
        "tags": ["cellcli", "griddisk", "asm", "basics"],
    },
    {
        "id": "PG007", "category": "CellCLI", "level": "Basic",
        "title": "Check Active Cell Requests",
        "scenario": (
            "A DBA reports 'Exadata feels slow right now'. You want to see what I/O "
            "requests are actively running on this cell at this moment."
        ),
        "task": "Show all active I/O requests currently being processed by this cell.",
        "hints": [
            "There is a special object type called ACTIVEREQUEST.",
            "Just list it: `LIST ACTIVEREQUEST`",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST ACTIVEREQUEST",
        "explanation": (
            "`LIST ACTIVEREQUEST` shows in-flight I/O requests: DB, consumer group, "
            "bytes read/written. Useful to confirm Smart Scan offload is active."
        ),
        "tags": ["cellcli", "activerequest", "performance", "basics"],
    },
    {
        "id": "PG008", "category": "CellCLI", "level": "Basic",
        "title": "Check Critical Alerts",
        "scenario": (
            "You are handed an Exadata system after a junior admin's shift. "
            "You want to check the last 24h of critical alerts on this cell."
        ),
        "task": "List alert history entries where severity is 'critical'.",
        "hints": [
            "The object is ALERTHISTORY.",
            "Filter: `WHERE severity = 'critical'`",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST ALERTHISTORY WHERE severity = 'critical'",
        "explanation": (
            "ALERTHISTORY persists operational events. Filtering by severity='critical' "
            "cuts through informational noise to show actionable alerts immediately."
        ),
        "tags": ["cellcli", "alerthistory", "basics"],
    },

    # =========================================================
    # CATEGORY: CellCLI — Intermediate / Advanced
    # =========================================================
    {
        "id": "PG009", "category": "CellCLI", "level": "Intermediate",
        "title": "Flash Cache: Show Hit Ratio",
        "scenario": (
            "OLTP performance has degraded. Your manager suspects Flash Cache hit ratio "
            "dropped. List Flash Cache detail to see all performance attributes."
        ),
        "task": "Show full Flash Cache detail on this cell.",
        "hints": [
            "Object: FLASHCACHE",
            "List with DETAIL to see hitRatio, size, and mode.",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST FLASHCACHE DETAIL",
        "explanation": (
            "`LIST FLASHCACHE DETAIL` shows flashCacheMode (WriteThrough/WriteBack), "
            "actualSize, currentOccupancy, hitRatio — the full performance picture."
        ),
        "tags": ["cellcli", "flashcache", "performance", "intermediate"],
    },
    {
        "id": "PG010", "category": "CellCLI", "level": "Intermediate",
        "title": "Metrics: Find Busiest Cell Disks",
        "scenario": (
            "I/O wait is high. You need to query real-time metrics for cell disk I/O "
            "to identify which disk has the highest read latency right now."
        ),
        "task": "List current metrics for CELL_DISK objects where metric name matches CD_IO read latency.",
        "hints": [
            "Use LIST METRICCURRENT with objectType and name filters.",
            "Filter: `WHERE objectType='CELL_DISK' AND name LIKE 'CD_IO_RQ_R%'`",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST METRICCURRENT WHERE objectType='CELL_DISK' AND name LIKE 'CD_IO_RQ_R%'",
        "explanation": (
            "METRICCURRENT gives real-time snapshots. CD_IO_RQ_R_LG = large read request count, "
            "CD_IO_BYTES_R = bytes read. Use LIKE patterns to filter relevant metric families."
        ),
        "tags": ["cellcli", "metrics", "performance", "intermediate"],
    },
    {
        "id": "PG011", "category": "CellCLI", "level": "Intermediate",
        "title": "Flash Cache: Recreate After Patch",
        "scenario": (
            "After a rolling cell patch, dm01cel03 shows flashCacheSize=0. "
            "The SSD NVMe drives are all healthy. You need to recreate the Flash Cache "
            "at 20TB total size."
        ),
        "task": "Drop the existing (zero-size) flash cache and recreate it at 20TB.",
        "hints": [
            "Two commands: DROP FLASHCACHE, then CREATE FLASHCACHE with size.",
            "Syntax: CREATE FLASHCACHE ALL SIZE=20T",
        ],
        "context": "CellCLI>",
        "ref_command": "DROP FLASHCACHE;\nCREATE FLASHCACHE ALL SIZE=20T",
        "explanation": (
            "DROP clears the stale metadata. CREATE FLASHCACHE ALL re-creates it using "
            "all available NVMe flash. Expect 5–10 minutes for warmup before hit ratio climbs."
        ),
        "tags": ["cellcli", "flashcache", "maintenance", "intermediate"],
    },
    {
        "id": "PG012", "category": "CellCLI", "level": "Intermediate",
        "title": "Metric History for a Time Window",
        "scenario": (
            "A latency spike was reported at 02:14 AM. It's now 03:00 AM. "
            "You need metric history from the last 60 minutes to correlate with the spike."
        ),
        "task": "Query metric history for entries in the last 60 minutes.",
        "hints": [
            "Use LIST METRICHISTORY with ageInMinutes filter.",
            "Filter: `WHERE ageInMinutes < 60`",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST METRICHISTORY WHERE ageInMinutes < 60",
        "explanation": (
            "METRICHISTORY stores time-series snapshots every 30 seconds. "
            "ageInMinutes is relative to now, so < 60 gives the last hour of samples."
        ),
        "tags": ["cellcli", "metrichistory", "troubleshooting", "intermediate"],
    },
    {
        "id": "PG013", "category": "CellCLI", "level": "Advanced",
        "title": "Create Grid Disks for Capacity Expansion",
        "scenario": (
            "DATAC1 is 85% full. You have 500GB free on every cell disk. "
            "Create new DATAC1 grid disks of 500GB each on all hard disks of this cell."
        ),
        "task": "Create grid disks on all hard disks with prefix DATAC1 and size 500G.",
        "hints": [
            "Use CREATE GRIDDISK with ALL HARDDISK and a prefix and size.",
            "Syntax: CREATE GRIDDISK ALL HARDDISK PREFIX=DATAC1 SIZE=500G",
        ],
        "context": "CellCLI>",
        "ref_command": "CREATE GRIDDISK ALL HARDDISK PREFIX=DATAC1 SIZE=500G",
        "explanation": (
            "ALL HARDDISK targets only HDD cell disks (not flash). PREFIX sets the disk "
            "group membership name. SIZE=500G allocates exactly 500GB from the free space "
            "of each cell disk. After this, add to ASM with ALTER DISKGROUP."
        ),
        "tags": ["cellcli", "griddisk", "capacity", "advanced"],
    },
    {
        "id": "PG014", "category": "CellCLI", "level": "Advanced",
        "title": "Offline a Failing Cell Disk",
        "scenario": (
            "HD_1_1 is showing predictive failure on cel07. "
            "You need to proactively offline this cell disk before ASM drops it automatically."
        ),
        "task": "Offline the cell disk named CD_01_dm01cel07 to prevent data corruption risk.",
        "hints": [
            "Use ALTER CELLDISK ... OFFLINE.",
            "Syntax: ALTER CELLDISK CD_01_dm01cel07 OFFLINE",
        ],
        "context": "CellCLI>",
        "ref_command": "ALTER CELLDISK CD_01_dm01cel07 OFFLINE",
        "explanation": (
            "ALTER ... OFFLINE gracefully removes the disk from I/O while ASM rebalances. "
            "Never physically pull a disk without offling it first — risk of I/O storm."
        ),
        "tags": ["cellcli", "celldisk", "maintenance", "advanced"],
    },

    # =========================================================
    # CATEGORY: DCLI
    # =========================================================
    {
        "id": "PG015", "category": "DCLI", "level": "Basic",
        "title": "Run a Command on All Cells",
        "scenario": (
            "You need to verify that cellsrv is running on ALL 7 cells of your Half Rack. "
            "The cell group file is at /etc/oracle/cell/network-config/cellgroup."
        ),
        "task": "Use DCLI to run 'cellcli -e list cell' across all cells as root.",
        "hints": [
            "Use dcli -g <groupfile> -l <user> '<command>'",
            "dcli -g /etc/oracle/cell/network-config/cellgroup -l root 'cellcli -e list cell'",
        ],
        "context": "$",
        "ref_command": "dcli -g /etc/oracle/cell/network-config/cellgroup -l root 'cellcli -e list cell'",
        "explanation": (
            "-g specifies the cell group file (one hostname per line). -l specifies the remote user. "
            "Each line of output is prefixed with the cell hostname."
        ),
        "tags": ["dcli", "parallel", "basics"],
    },
    {
        "id": "PG016", "category": "DCLI", "level": "Basic",
        "title": "Check Image Version on All Cells",
        "scenario": (
            "Before a rolling patch, you need to confirm the current Exadata image version "
            "on every cell. The group file is at /etc/oracle/cell/network-config/cellgroup."
        ),
        "task": "Use DCLI to run 'imageinfo | grep -i version' on all cells.",
        "hints": [
            "Same dcli pattern with a pipe inside single quotes.",
            "dcli -g cellgroup -l root 'imageinfo | grep -i version'",
        ],
        "context": "$",
        "ref_command": "dcli -g /etc/oracle/cell/network-config/cellgroup -l root 'imageinfo | grep -i version'",
        "explanation": (
            "The command inside quotes runs on each remote host via SSH. Quotes protect "
            "the pipe from the local shell. imageinfo is the Exadata firmware reporting tool."
        ),
        "tags": ["dcli", "imageinfo", "patching", "basics"],
    },
    {
        "id": "PG017", "category": "DCLI", "level": "Intermediate",
        "title": "Check Non-Normal Physical Disks Across All Cells",
        "scenario": (
            "It's your morning check. You want a one-liner that shows any physical disks "
            "in non-normal status across ALL cells in your rack."
        ),
        "task": "Use DCLI to run the CellCLI command that lists non-normal physical disks on all cells.",
        "hints": [
            "dcli + cellcli -e + WHERE filter",
            "Inner command: cellcli -e 'list physicaldisk where status != normal'",
        ],
        "context": "$",
        "ref_command": "dcli -g /etc/oracle/cell/network-config/cellgroup -l root \"cellcli -e 'list physicaldisk where status != normal'\"",
        "explanation": (
            "The outer double-quotes wrap the dcli command; single quotes wrap the CellCLI expression. "
            "Output lines with hostnames let you spot which cell has the problem instantly."
        ),
        "tags": ["dcli", "physicaldisk", "health-check", "intermediate"],
    },
    {
        "id": "PG018", "category": "DCLI", "level": "Intermediate",
        "title": "Push SSH Keys to All Cells",
        "scenario": (
            "You've just created a new RSA key pair. You need to push your public key "
            "to all cells for passwordless DCLI access."
        ),
        "task": "Use DCLI's built-in key-push flag to distribute your SSH public key.",
        "hints": [
            "dcli has a special flag for key distribution: -k",
            "Syntax: dcli -g <groupfile> -l root -k",
        ],
        "context": "$",
        "ref_command": "dcli -g /etc/oracle/cell/network-config/cellgroup -l root -k",
        "explanation": (
            "-k pushes the local user's ~/.ssh/id_rsa.pub to each host's authorized_keys. "
            "You'll enter the password once per cell. After this, DCLI runs silently."
        ),
        "tags": ["dcli", "ssh", "setup", "intermediate"],
    },
    {
        "id": "PG019", "category": "DCLI", "level": "Advanced",
        "title": "Run a Shell Script on All Cells",
        "scenario": (
            "You have a complex maintenance script at /tmp/cell_check.sh that you've "
            "already copied to all cells. Run it on all cells in parallel."
        ),
        "task": "Use DCLI to execute the remote script /tmp/cell_check.sh on all cells.",
        "hints": [
            "dcli has a -x flag to run a remote file rather than an inline command.",
            "Syntax: dcli -g <groupfile> -l root -x /tmp/cell_check.sh",
        ],
        "context": "$",
        "ref_command": "dcli -g /etc/oracle/cell/network-config/cellgroup -l root -x /tmp/cell_check.sh",
        "explanation": (
            "-x runs the specified remote file as a script (not a local file). "
            "Use for multi-line operations that are too long for inline -c quoting."
        ),
        "tags": ["dcli", "scripting", "advanced"],
    },

    # =========================================================
    # CATEGORY: ASM
    # =========================================================
    {
        "id": "PG020", "category": "ASM", "level": "Basic",
        "title": "List ASM Disk Groups",
        "scenario": (
            "You've logged in as sysasm. Get a quick overview of all disk groups: "
            "name, state, type, and size in TB."
        ),
        "task": "Query V$ASM_DISKGROUP to show name, state, type, and total size in TB.",
        "hints": [
            "SELECT from V$ASM_DISKGROUP.",
            "Divide total_mb by 1024/1024 to get TB.",
        ],
        "context": "SQL>",
        "ref_command": "SELECT name, state, type, ROUND(total_mb/1024/1024,2) tb FROM v$asm_diskgroup;",
        "explanation": (
            "V$ASM_DISKGROUP is the top-level ASM inventory. STATE should be MOUNTED; "
            "TYPE will be HIGH (DATAC1) or NORMAL (RECOC1). total_mb/1024/1024 = TB."
        ),
        "tags": ["asm", "diskgroup", "basics"],
    },
    {
        "id": "PG021", "category": "ASM", "level": "Basic",
        "title": "Check ASM Disk Failgroups",
        "scenario": (
            "DATAC1 is HIGH redundancy. You need to verify that it has a failgroup "
            "from EVERY cell — if any cell's disks are missing, HIGH redundancy is at risk."
        ),
        "task": "Query V$ASM_DISK to show path and failgroup for disk group number 1 (DATAC1).",
        "hints": [
            "SELECT path, failgroup FROM V$ASM_DISK.",
            "Filter: WHERE group_number=1 ORDER BY failgroup",
        ],
        "context": "SQL>",
        "ref_command": "SELECT path, failgroup, state FROM v$asm_disk WHERE group_number=1 ORDER BY failgroup;",
        "explanation": (
            "Each failgroup corresponds to one storage cell. For a 7-cell Half Rack "
            "with DATAC1 HIGH, you need 7 distinct failgroups — one per cell."
        ),
        "tags": ["asm", "failgroup", "high-redundancy", "basics"],
    },
    {
        "id": "PG022", "category": "ASM", "level": "Basic",
        "title": "Check ASMCMD Disk Groups",
        "scenario": (
            "You are logged in as the grid user in asmcmd. "
            "List all disk groups with their total and free space."
        ),
        "task": "Run the asmcmd command to list disk groups with space information.",
        "hints": [
            "asmcmd has an lsdg command.",
            "Just run: lsdg",
        ],
        "context": "asmcmd>",
        "ref_command": "lsdg",
        "explanation": (
            "`lsdg` shows State, Type, Rebal, Total_MB, Free_MB for all disk groups. "
            "The Rebal column shows Y when a rebalance is in progress."
        ),
        "tags": ["asm", "asmcmd", "basics"],
    },
    {
        "id": "PG023", "category": "ASM", "level": "Intermediate",
        "title": "Add New Disks to DATAC1",
        "scenario": (
            "You've created new grid disks on all cells with the prefix DATAC1. "
            "Now add them to the DATAC1 disk group and start rebalance at power 4."
        ),
        "task": "Write the ALTER DISKGROUP command to add the new disks and set rebalance power.",
        "hints": [
            "Use ALTER DISKGROUP ... ADD DISK '...' REBALANCE POWER N",
            "Discovery string for Exadata: 'o/*/DATAC1_*'",
        ],
        "context": "SQL>",
        "ref_command": "ALTER DISKGROUP DATAC1 ADD DISK 'o/*/DATAC1_*' REBALANCE POWER 4;",
        "explanation": (
            "The discovery string 'o/*/DATAC1_*' matches all ASM disks whose name "
            "starts with DATAC1 in any ASM library directory. POWER 4 = moderate speed "
            "(range 1-11). Monitor with V$ASM_OPERATION."
        ),
        "tags": ["asm", "rebalance", "capacity", "intermediate"],
    },
    {
        "id": "PG024", "category": "ASM", "level": "Intermediate",
        "title": "Monitor Rebalance Progress",
        "scenario": (
            "You just kicked off a rebalance. Your manager wants an ETA. "
            "Check the rebalance operation status from ASM."
        ),
        "task": "Query V$ASM_OPERATION to see rebalance progress, estimated time, and power.",
        "hints": [
            "SELECT * FROM V$ASM_OPERATION.",
            "Key columns: OPERATION, STATE, POWER, EST_MINUTES",
        ],
        "context": "SQL>",
        "ref_command": "SELECT group_number, operation, state, power, est_minutes FROM v$asm_operation;",
        "explanation": (
            "V$ASM_OPERATION shows active ASM operations. EST_MINUTES is the estimated "
            "remaining time. If empty, no rebalance is running (it completed)."
        ),
        "tags": ["asm", "rebalance", "monitoring", "intermediate"],
    },
    {
        "id": "PG025", "category": "ASM", "level": "Advanced",
        "title": "Reduce Rebalance Power Without Stopping",
        "scenario": (
            "Rebalance is running at power 7 and users are reporting I/O slowness. "
            "You need to reduce power to 2 WITHOUT stopping and restarting the rebalance."
        ),
        "task": "Change the rebalance power on DATAC1 to 2 while it is running.",
        "hints": [
            "Use ALTER DISKGROUP ... REBALANCE POWER N",
            "Syntax: ALTER DISKGROUP DATAC1 REBALANCE POWER 2;",
        ],
        "context": "SQL>",
        "ref_command": "ALTER DISKGROUP DATAC1 REBALANCE POWER 2;",
        "explanation": (
            "ASM allows in-flight power adjustment. Power 1 = minimal I/O impact. "
            "This is the correct approach — killing and restarting a rebalance is wasteful "
            "and can leave data temporarily unprotected."
        ),
        "tags": ["asm", "rebalance", "performance", "advanced"],
    },

    # =========================================================
    # CATEGORY: RMAN
    # =========================================================
    {
        "id": "PG026", "category": "RMAN", "level": "Basic",
        "title": "Connect RMAN to Target",
        "scenario": (
            "You are on exadb01 as the oracle user. "
            "Connect RMAN to the local database using OS authentication."
        ),
        "task": "Start RMAN and connect to the local target database.",
        "hints": [
            "Use rman target / for OS auth.",
            "Syntax: rman target /",
        ],
        "context": "$",
        "ref_command": "rman target /",
        "explanation": (
            "`rman target /` connects RMAN to the local DB using OS authentication "
            "(same as sqlplus / as sysdba). No password needed if you're the oracle OS user."
        ),
        "tags": ["rman", "basics", "connect"],
    },
    {
        "id": "PG027", "category": "RMAN", "level": "Basic",
        "title": "Enable Block Change Tracking",
        "scenario": (
            "You are setting up incremental backups on a new Exadata. "
            "Block Change Tracking (BCT) must be enabled first to accelerate incrementals. "
            "The BCT file should be on RECOC1."
        ),
        "task": "Enable block change tracking and store the BCT file in +RECOC1.",
        "hints": [
            "SQL command: ALTER DATABASE ENABLE BLOCK CHANGE TRACKING",
            "Add: USING FILE '+RECOC1/ORCL/bct.dbf'",
        ],
        "context": "SQL>",
        "ref_command": "ALTER DATABASE ENABLE BLOCK CHANGE TRACKING USING FILE '+RECOC1/ORCL/bct.dbf';",
        "explanation": (
            "BCT records which blocks changed since the last backup. "
            "This makes level-1 incrementals dramatically faster — Exadata's Smart Incremental "
            "uses BCT + storage-side filtering to skip unchanged blocks."
        ),
        "tags": ["rman", "bct", "incremental", "basics"],
    },
    {
        "id": "PG028", "category": "RMAN", "level": "Intermediate",
        "title": "Run Level-1 Incremental Backup",
        "scenario": (
            "BCT is enabled. Run tonight's scheduled incremental level-1 backup "
            "including archived logs."
        ),
        "task": "Run RMAN incremental level 1 backup of the database plus archivelogs.",
        "hints": [
            "BACKUP INCREMENTAL LEVEL 1 DATABASE",
            "Add PLUS ARCHIVELOG to include archivelogs.",
        ],
        "context": "RMAN>",
        "ref_command": "BACKUP INCREMENTAL LEVEL 1 DATABASE PLUS ARCHIVELOG;",
        "explanation": (
            "LEVEL 1 backs up only changed blocks since the last level 0 or 1. "
            "PLUS ARCHIVELOG ensures all log gaps are filled. "
            "Exadata's Smart Incremental with BCT can reduce backup size by 90% vs a full."
        ),
        "tags": ["rman", "backup", "incremental", "intermediate"],
    },
    {
        "id": "PG029", "category": "RMAN", "level": "Intermediate",
        "title": "List Recent Backups",
        "scenario": (
            "An auditor asks for proof that a backup ran last night. "
            "Show a summary of all backups in the RMAN catalog."
        ),
        "task": "List a summary of all RMAN backups (compact view).",
        "hints": [
            "LIST BACKUP SUMMARY;",
            "This shows BS Key, type, completion time, device.",
        ],
        "context": "RMAN>",
        "ref_command": "LIST BACKUP SUMMARY;",
        "explanation": (
            "LIST BACKUP SUMMARY gives a compact table: BS Key (backup set ID), "
            "Type (D=datafile, A=archivelog), Completion Time, Device. "
            "Use LIST BACKUP DETAIL for full information."
        ),
        "tags": ["rman", "catalog", "audit", "intermediate"],
    },
    {
        "id": "PG030", "category": "RMAN", "level": "Advanced",
        "title": "Crosscheck and Delete Expired Backups",
        "scenario": (
            "The FRA is at 92% usage. You need to crosscheck backup availability "
            "then delete expired (stale) pieces."
        ),
        "task": "Crosscheck all backups, then delete expired backup sets.",
        "hints": [
            "Two steps: CROSSCHECK BACKUP; then DELETE EXPIRED BACKUP;",
            "Sequence: crosscheck first, then delete.",
        ],
        "context": "RMAN>",
        "ref_command": "CROSSCHECK BACKUP;\nDELETE EXPIRED BACKUP;",
        "explanation": (
            "CROSSCHECK verifies each backup piece against the physical file. "
            "Pieces not found on disk are marked EXPIRED. "
            "DELETE EXPIRED then removes the catalog entries for those missing pieces."
        ),
        "tags": ["rman", "fra", "maintenance", "advanced"],
    },

    # =========================================================
    # CATEGORY: SRVCTL / CRSCTL
    # =========================================================
    {
        "id": "PG031", "category": "SRVCTL", "level": "Basic",
        "title": "Check Database Status (All Instances)",
        "scenario": (
            "You log onto exadb01. Check the status of all instances of the ORCL RAC database."
        ),
        "task": "Show the current running status of all instances of database ORCL.",
        "hints": [
            "Use srvctl status database.",
            "Syntax: srvctl status database -d ORCL",
        ],
        "context": "$",
        "ref_command": "srvctl status database -d ORCL",
        "explanation": (
            "srvctl reads from the OCR (Oracle Cluster Registry) and shows the actual "
            "cluster-managed status of each instance. Never use SQL*Plus shutdown "
            "on RAC — always go through srvctl."
        ),
        "tags": ["srvctl", "rac", "status", "basics"],
    },
    {
        "id": "PG032", "category": "SRVCTL", "level": "Basic",
        "title": "Stop a Single RAC Instance",
        "scenario": (
            "You need to patch exadb02 only. Stop ORCL2 without affecting ORCL1 "
            "still running on exadb01."
        ),
        "task": "Stop instance ORCL2 of database ORCL using srvctl.",
        "hints": [
            "srvctl stop instance -d <db> -i <instance>",
            "Syntax: srvctl stop instance -d ORCL -i ORCL2",
        ],
        "context": "$",
        "ref_command": "srvctl stop instance -d ORCL -i ORCL2",
        "explanation": (
            "-i specifies the instance name. srvctl will drain connections and "
            "perform a checkpoint before stopping. The cluster registry is updated "
            "to reflect the stopped state — other instances are unaffected."
        ),
        "tags": ["srvctl", "rac", "instance", "basics"],
    },
    {
        "id": "PG033", "category": "SRVCTL", "level": "Basic",
        "title": "Check Cluster Resource Status",
        "scenario": (
            "You want a complete view of all cluster-managed resources: ASM, DB, "
            "listeners, VIPs, and services in a table format."
        ),
        "task": "Show all cluster resources in table format using crsctl.",
        "hints": [
            "crsctl stat res -t",
            "The -t flag formats output as a table.",
        ],
        "context": "$",
        "ref_command": "crsctl stat res -t",
        "explanation": (
            "crsctl stat res -t shows NAME, TARGET (ONLINE/OFFLINE), STATE, and HOST "
            "for every resource. This is your 10-second cluster health check."
        ),
        "tags": ["crsctl", "cluster", "status", "basics"],
    },
    {
        "id": "PG034", "category": "SRVCTL", "level": "Intermediate",
        "title": "Configure Database for Auto-Start",
        "scenario": (
            "After a planned OS reboot, ORCL should start automatically. "
            "Ensure the DB cluster resource is configured to start on cluster restart."
        ),
        "task": "Use srvctl to set the management policy of ORCL database to AUTOMATIC.",
        "hints": [
            "Use srvctl modify database.",
            "Add: -policy AUTOMATIC",
        ],
        "context": "$",
        "ref_command": "srvctl modify database -d ORCL -policy AUTOMATIC",
        "explanation": (
            "Policy AUTOMATIC means GI will start the database after cluster startup. "
            "Policy MANUAL means it won't auto-start. Default for new databases is AUTOMATIC."
        ),
        "tags": ["srvctl", "policy", "auto-start", "intermediate"],
    },
    {
        "id": "PG035", "category": "SRVCTL", "level": "Intermediate",
        "title": "Query Voting Disks",
        "scenario": (
            "Before shutting down a cell for maintenance, you need to confirm that "
            "voting disks are on ASM (not on that cell's raw device). "
            "Check the current voting disk configuration."
        ),
        "task": "Query the current voting disk locations using crsctl.",
        "hints": [
            "crsctl query css votedisk",
        ],
        "context": "$",
        "ref_command": "crsctl query css votedisk",
        "explanation": (
            "In Exadata, voting disks are stored in the DBFS_DG or OCR disk group. "
            "This command shows the full path. On Exadata, the path is +DBFS_DG — "
            "meaning it is NOT on a raw device, so any single cell failure is safe."
        ),
        "tags": ["crsctl", "votedisk", "css", "intermediate"],
    },
    {
        "id": "PG036", "category": "SRVCTL", "level": "Advanced",
        "title": "Check Cluster Health Across All Nodes",
        "scenario": (
            "Node exadb03 failed to rejoin the cluster after a reboot. "
            "Run the crsctl cluster check that shows status across ALL nodes."
        ),
        "task": "Check cluster health status across all nodes with a single crsctl command.",
        "hints": [
            "crsctl check cluster with -all flag.",
            "Syntax: crsctl check cluster -all",
        ],
        "context": "$",
        "ref_command": "crsctl check cluster -all",
        "explanation": (
            "crsctl check cluster -all connects to every node in the cluster and "
            "reports CRS/CSS/EVM health. A node showing OFFLINE here means its "
            "GI stack is down, not just one resource."
        ),
        "tags": ["crsctl", "cluster", "multi-node", "advanced"],
    },

    # =========================================================
    # CATEGORY: DGMGRL (Data Guard)
    # =========================================================
    {
        "id": "PG037", "category": "DGMGRL", "level": "Basic",
        "title": "Connect to DGMGRL Broker",
        "scenario": (
            "You are on exadb01. Connect to the Data Guard broker for the ORCL_PRI database "
            "using the sys user."
        ),
        "task": "Connect to DGMGRL using sys credentials to primary ORCL_PRI.",
        "hints": [
            "dgmgrl <user>/<password>@<connect_identifier>",
            "dgmgrl sys/password@ORCL_PRI",
        ],
        "context": "$",
        "ref_command": "dgmgrl sys/password@ORCL_PRI",
        "explanation": (
            "DGMGRL connects to the broker process (DMON) running on the primary. "
            "You can also connect to the standby — DGMGRL will show the full config regardless."
        ),
        "tags": ["dgmgrl", "connect", "dataguard", "basics"],
    },
    {
        "id": "PG038", "category": "DGMGRL", "level": "Basic",
        "title": "Show DG Configuration",
        "scenario": (
            "You are connected to DGMGRL. Get a high-level overview of the Data Guard "
            "configuration to verify both members and protection mode."
        ),
        "task": "Show the Data Guard Broker configuration.",
        "hints": [
            "SHOW CONFIGURATION",
        ],
        "context": "DGMGRL>",
        "ref_command": "SHOW CONFIGURATION",
        "explanation": (
            "SHOW CONFIGURATION shows: config name, protection mode, members "
            "(primary + standby), and overall status. 'SUCCESS' = healthy. "
            "'Warning' or 'Error' need immediate investigation."
        ),
        "tags": ["dgmgrl", "configuration", "dataguard", "basics"],
    },
    {
        "id": "PG039", "category": "DGMGRL", "level": "Intermediate",
        "title": "Show Standby Database Status",
        "scenario": (
            "The monitoring team reports lag alerts on ORCL_STBY. "
            "Drill into the standby database details to see transport and apply lag."
        ),
        "task": "Show detailed database status for the standby ORCL_STBY.",
        "hints": [
            "SHOW DATABASE <name>",
            "SHOW DATABASE VERBOSE ORCL_STBY for more detail",
        ],
        "context": "DGMGRL>",
        "ref_command": "SHOW DATABASE VERBOSE ORCL_STBY",
        "explanation": (
            "SHOW DATABASE VERBOSE shows Transport Lag, Apply Lag, Apply Rate, "
            "log sequence gaps, and current role. Transport Lag > 0 means redo is "
            "not reaching the standby; Apply Lag > 0 means it arrived but isn't applied yet."
        ),
        "tags": ["dgmgrl", "standby", "lag", "intermediate"],
    },
    {
        "id": "PG040", "category": "DGMGRL", "level": "Intermediate",
        "title": "Validate Standby Before Switchover",
        "scenario": (
            "Planned DC maintenance requires a switchover. Before issuing the switchover "
            "command, validate that ORCL_STBY is ready."
        ),
        "task": "Validate the standby database ORCL_STBY readiness for switchover.",
        "hints": [
            "VALIDATE DATABASE <name>",
        ],
        "context": "DGMGRL>",
        "ref_command": "VALIDATE DATABASE ORCL_STBY",
        "explanation": (
            "VALIDATE DATABASE checks: transport, apply lag, redo log gaps, "
            "Flash Recovery Area space, and block change tracking. "
            "All checks must pass before a switchover is safe."
        ),
        "tags": ["dgmgrl", "switchover", "validate", "intermediate"],
    },
    {
        "id": "PG041", "category": "DGMGRL", "level": "Advanced",
        "title": "Perform Graceful Switchover",
        "scenario": (
            "VALIDATE DATABASE returned all SUCCESS. "
            "Perform the graceful switchover to ORCL_STBY."
        ),
        "task": "Issue the DGMGRL switchover command to make ORCL_STBY the new primary.",
        "hints": [
            "SWITCHOVER TO <standby_name>",
        ],
        "context": "DGMGRL>",
        "ref_command": "SWITCHOVER TO ORCL_STBY",
        "explanation": (
            "DGMGRL coordinates the entire switchover: flush redo from primary, "
            "convert primary to standby, activate new primary. Expected time: 60-300s. "
            "After completion, run SHOW CONFIGURATION to confirm new roles."
        ),
        "tags": ["dgmgrl", "switchover", "advanced"],
    },

    # =========================================================
    # CATEGORY: Smart Scan & Performance
    # =========================================================
    {
        "id": "PG042", "category": "Smart Scan", "level": "Intermediate",
        "title": "Check Smart Scan Offload Eligibility",
        "scenario": (
            "A critical analytics query is running slowly. You suspect Smart Scan is "
            "not being used. Check V$SQL offload statistics for sql_id 'a1b2c3d4e'."
        ),
        "task": "Query V$SQL to show offload eligible bytes vs returned bytes for a specific sql_id.",
        "hints": [
            "Columns: io_cell_offload_eligible_bytes, io_cell_offload_returned_bytes",
            "SELECT sql_id, io_cell_offload_eligible_bytes, io_cell_offload_returned_bytes FROM v$sql WHERE sql_id='...'",
        ],
        "context": "SQL>",
        "ref_command": "SELECT sql_id, io_cell_offload_eligible_bytes elig, io_cell_offload_returned_bytes ret, ROUND((1 - io_cell_offload_returned_bytes / NULLIF(io_cell_offload_eligible_bytes,0))*100,1) savings_pct FROM v$sql WHERE sql_id = 'a1b2c3d4e';",
        "explanation": (
            "savings_pct = 1-(ret/elig). If elig > 0 and ret ≈ elig, Smart Scan is "
            "not filtering much (table is small or no predicate). "
            "Good Smart Scan shows savings_pct > 80%."
        ),
        "tags": ["smart-scan", "offload", "performance", "intermediate"],
    },
    {
        "id": "PG043", "category": "Smart Scan", "level": "Intermediate",
        "title": "Check Storage Index Savings",
        "scenario": (
            "You want to verify that Storage Indexes are saving physical I/O "
            "for your session's current query."
        ),
        "task": "Query V$MYSTAT + V$STATNAME to find the 'cell physical IO bytes saved by storage index' statistic.",
        "hints": [
            "JOIN v$mystat m and v$statname n on statistic#",
            "WHERE name LIKE 'cell physical IO bytes saved by storage index'",
        ],
        "context": "SQL>",
        "ref_command": "SELECT n.name, m.value FROM v$mystat m JOIN v$statname n ON m.statistic# = n.statistic# WHERE n.name LIKE 'cell physical IO bytes saved by storage index';",
        "explanation": (
            "A value > 0 confirms the Storage Index skipped at least some extents. "
            "High savings means the column's values are well-clustered on disk."
        ),
        "tags": ["smart-scan", "storage-index", "statistics", "intermediate"],
    },
    {
        "id": "PG044", "category": "Smart Scan", "level": "Advanced",
        "title": "Force a Full Table Scan to Use Smart Scan",
        "scenario": (
            "A query on table SALES is not using Smart Scan (possibly using indexes). "
            "You want to force a full table scan with the Exadata Smart Scan hint."
        ),
        "task": "Add the correct hint(s) to force a full table scan with Smart Scan offload on SALES table.",
        "hints": [
            "Two hints needed: full() to force FTS and no_index() to block index access.",
            "Use /*+ FULL(s) NO_INDEX(s) */ in the SELECT",
        ],
        "context": "SQL>",
        "ref_command": "SELECT /*+ FULL(s) NO_INDEX(s) */ * FROM sales s WHERE region='APAC';",
        "explanation": (
            "Smart Scan requires a full segment scan. FULL(s) forces it; NO_INDEX(s) "
            "prevents the optimizer from choosing index range scans that bypass Smart Scan. "
            "Partition pruning + Smart Scan + Storage Indexes = maximum offload benefit."
        ),
        "tags": ["smart-scan", "hints", "full-table-scan", "advanced"],
    },
    {
        "id": "PG045", "category": "Smart Scan", "level": "Advanced",
        "title": "Identify Smart Scan Blockers",
        "scenario": (
            "Smart Scan is showing 0 offload eligible bytes for a large query. "
            "List all common blockers you would check (as a query or explanation)."
        ),
        "task": "Query V$SQL_PLAN to check if a specific sql_id is using a STORAGE FULL SCAN operation.",
        "hints": [
            "Look for operation='TABLE ACCESS' and options='STORAGE FULL' in V$SQL_PLAN",
            "WHERE sql_id='...' AND operation='TABLE ACCESS'",
        ],
        "context": "SQL>",
        "ref_command": "SELECT operation, options, object_name FROM v$sql_plan WHERE sql_id='a1b2c3d4e' AND operation='TABLE ACCESS';",
        "explanation": (
            "Options='STORAGE FULL' confirms Smart Scan. Options='FULL' (without STORAGE) "
            "means it's a compute-side full scan — Smart Scan is blocked. "
            "Common blockers: row-by-row PL/SQL functions in WHERE, ENCRYPT columns, "
            "objects smaller than 1MB, BUFFER CACHE access path."
        ),
        "tags": ["smart-scan", "execution-plan", "blockers", "advanced"],
    },

    # =========================================================
    # CATEGORY: Incident Response
    # =========================================================
    {
        "id": "PG046", "category": "Incident Response", "level": "Advanced",
        "title": "Confirm Cell is Down",
        "scenario": (
            "3 AM alert: 'dm01cel05 unreachable'. You've SSH'd to exadb01. "
            "Confirm whether the cell is truly offline from the ASM perspective."
        ),
        "task": "From ASM, query which disks are OFFLINE and which failgroup they belong to.",
        "hints": [
            "SELECT from V$ASM_DISK with mode_status='OFFLINE'",
        ],
        "context": "SQL>",
        "ref_command": "SELECT path, failgroup, mode_status, state FROM v$asm_disk WHERE mode_status='OFFLINE' ORDER BY failgroup;",
        "explanation": (
            "mode_status='OFFLINE' means ASM has stopped I/O to those disks. "
            "If all disks in failgroup 'dm01cel05' are OFFLINE, the cell is down. "
            "ASM will wait DISK_REPAIR_TIME (default 3.6h) before dropping them."
        ),
        "tags": ["incident", "asm", "cell-failure", "advanced"],
    },
    {
        "id": "PG047", "category": "Incident Response", "level": "Advanced",
        "title": "Check DISK_REPAIR_TIME",
        "scenario": (
            "cel05 has been down for 2 hours. The default DISK_REPAIR_TIME is 3.6 hours. "
            "You need to verify the current setting before deciding whether to extend it."
        ),
        "task": "Query V$ASM_ATTRIBUTE to find the disk_repair_time setting for DATAC1.",
        "hints": [
            "SELECT from V$ASM_ATTRIBUTE WHERE name='disk_repair_time'",
            "Join with V$ASM_DISKGROUP to filter by name",
        ],
        "context": "SQL>",
        "ref_command": "SELECT dg.name, a.name, a.value FROM v$asm_attribute a JOIN v$asm_diskgroup dg ON a.group_number=dg.group_number WHERE a.name='disk_repair_time' AND dg.name='DATAC1';",
        "explanation": (
            "disk_repair_time is the grace period ASM waits before permanently dropping "
            "offline disks and rebalancing. If cell repair is not complete within this "
            "window, increase it: ALTER DISKGROUP DATAC1 SET ATTRIBUTE 'disk_repair_time'='8.0h';"
        ),
        "tags": ["incident", "asm", "disk-repair-time", "advanced"],
    },
    {
        "id": "PG048", "category": "Incident Response", "level": "Advanced",
        "title": "Offline a Failgroup Manually",
        "scenario": (
            "cel08 needs emergency replacement. ASM hasn't dropped the disks yet. "
            "You manually offline the entire dm01cel08 failgroup in DATAC1 to "
            "prevent I/O timeouts from slowing the database."
        ),
        "task": "Offline all disks in failgroup dm01cel08 of disk group DATAC1 with a WAIT clause.",
        "hints": [
            "ALTER DISKGROUP ... OFFLINE DISKS IN FAILGROUP ...",
            "Syntax: ALTER DISKGROUP DATAC1 OFFLINE DISKS IN FAILGROUP dm01cel08 WAIT;",
        ],
        "context": "SQL>",
        "ref_command": "ALTER DISKGROUP DATAC1 OFFLINE DISKS IN FAILGROUP dm01cel08 WAIT;",
        "explanation": (
            "WAIT blocks until the operation completes. Without WAIT, the offline happens "
            "asynchronously. This command tells ASM to stop all I/O to that failgroup "
            "immediately, preventing additional I/O errors."
        ),
        "tags": ["incident", "asm", "failgroup", "advanced"],
    },
    {
        "id": "PG049", "category": "Incident Response", "level": "Advanced",
        "title": "Rebuild After Cell Replacement",
        "scenario": (
            "New hardware for cel08 is racked. CellCLI is running. Cell disks "
            "and grid disks need to be recreated before adding back to ASM."
        ),
        "task": "On the new cell, recreate all cell disks and then recreate all DATAC1 hard-disk grid disks.",
        "hints": [
            "Two CellCLI commands: CREATE CELLDISK ALL, then CREATE GRIDDISK ALL HARDDISK PREFIX=DATAC1",
        ],
        "context": "CellCLI>",
        "ref_command": "CREATE CELLDISK ALL;\nCREATE GRIDDISK ALL HARDDISK PREFIX=DATAC1",
        "explanation": (
            "CREATE CELLDISK ALL discovers all physical disks and creates cell disk "
            "metadata. CREATE GRIDDISK creates the ASM-facing slices. "
            "After this, ALTER DISKGROUP DATAC1 ADD DISK adds them back."
        ),
        "tags": ["incident", "cellcli", "rebuild", "advanced"],
    },
    {
        "id": "PG050", "category": "Incident Response", "level": "Advanced",
        "title": "Identify Runaway Query Consuming Flash Cache",
        "scenario": (
            "Exadata performance has degraded. CellCLI shows flash cache hit ratio "
            "dropped from 95% to 40% in the last 10 minutes. "
            "Find which database and consumer group is dominating the cell's I/O."
        ),
        "task": "Use CellCLI to list current active requests to identify the top I/O consumer.",
        "hints": [
            "LIST ACTIVEREQUEST shows db_name, consumer_group, bytes",
        ],
        "context": "CellCLI>",
        "ref_command": "LIST ACTIVEREQUEST ATTRIBUTES dbName,consumerGroupName,ioType,bytesRead,bytesWritten",
        "explanation": (
            "ACTIVEREQUEST exposes real-time I/O attribution. If one DB/consumer group "
            "is doing massive sequential reads (e.g., a full export), it will evict "
            "OLTP data from flash cache. Solution: IORM plan or session kill."
        ),
        "tags": ["incident", "cellcli", "iorm", "flash-cache", "advanced"],
    },
]

# Category metadata for UI display
CATEGORIES = {
    "CellCLI":          {"icon": "🖥",  "color": "#00ff88", "desc": "Cell administration shell"},
    "DCLI":             {"icon": "⚡",  "color": "#66c2ff", "desc": "Parallel command execution"},
    "ASM":              {"icon": "💾",  "color": "#c8a0ff", "desc": "Automatic Storage Management"},
    "RMAN":             {"icon": "🛡",  "color": "#f39c12", "desc": "Recovery Manager"},
    "SRVCTL":           {"icon": "🔗",  "color": "#ff7f50", "desc": "SRVCTL & CRSCTL cluster tools"},
    "DGMGRL":           {"icon": "🔄",  "color": "#87ceeb", "desc": "Data Guard Broker CLI"},
    "Smart Scan":       {"icon": "🚀",  "color": "#ff6b9d", "desc": "Offload engine verification"},
    "Incident Response":{"icon": "🚨",  "color": "#e74c3c", "desc": "Real-world emergency scenarios"},
}

LEVELS = ["Basic", "Intermediate", "Advanced"]
