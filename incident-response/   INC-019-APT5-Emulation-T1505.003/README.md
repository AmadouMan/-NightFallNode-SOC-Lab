# INC-019 — APT5 (Keyhole Panda) Emulation, Detection & Investigation

> **Threat actor:** APT5 / Keyhole Panda (MITRE ATT&CK **G1023**)
> **Asset:** NexusShield-corp (Wazuh agent 001) · `192.168.112.133`
> **Attacker:** DayGone (Kali) · `192.168.112.135`
> **SIEM:** SecMon · Wazuh 4.14.5 · `192.168.112.131`
> **Status:** ✅ Contained / Eradicated — persistence established, never used

---

## 1. Scenario

APT5 is a China-nexus espionage actor known for mass-exploiting internet-facing edge devices, deploying web shells (the **ATRIUM** family), creating local backdoor accounts, and running anti-forensic log-clearing tools (**CLEANPULSE / BLOODMINE / THINBLOOD**) before pivoting through an **ORB** botnet for command-and-control.

This incident emulates that tradecraft against a monitored corporate endpoint, closes three detection gaps with new Wazuh rules, proves each rule by firing it live, and investigates the intrusion end to end.

---

## 2. Detection gaps closed

| Rule | Lvl | Technique | Fires on |
|------|-----|-----------|----------|
| `100023` | 13 | **T1505.003** · Web Shell | A script (`.php/.jsp/.asp…`) written under `/var/www` (realtime FIM) |
| `100024` | 12 | **T1136** · Create Account | A new local account created on the endpoint |
| `100025` | 14 | **T1070.002** · Clear Logs | `journalctl --vacuum` / log-clearing via auditd command logging |
| `100022` | 12 | **T1071** · C2 *(existing)* | Auth attempt from an IP on the threat-intel IOC list |

### Rules (`local_rules.xml`, group `nightfallnode_soc`)

```xml
<!-- Web shell written to the web root (T1505.003) -->
<rule id="100023" level="13">
  <if_group>syscheck</if_group>
  <field name="file" type="pcre2">/var/www/.+\.(php|phtml|jsp|jspx|asp|aspx)$</field>
  <description>NightFallNode: Script written to web root - possible web shell (APT5 ATRIUM-style)</description>
  <mitre><id>T1505.003</id></mitre>
  <group>web_shell,apt5,attack,</group>
</rule>

<!-- Backdoor local account creation (T1136) -->
<rule id="100024" level="12">
  <if_group>syslog</if_group>
  <match>useradd|new user:|new group:</match>
  <description>NightFallNode: New local account created - possible attacker persistence (APT5)</description>
  <mitre><id>T1136</id></mitre>
  <group>account_creation,apt5,attack,</group>
</rule>

<!-- Anti-forensic log clearing via journalctl --vacuum (T1070.002) -->
<rule id="100025" level="14">
  <if_sid>80792</if_sid>
  <field name="audit.exe" type="pcre2">journalctl$</field>
  <field name="audit.execve.a1" type="pcre2">vacuum|rotate</field>
  <description>NightFallNode: Anti-forensic log clearing - journalctl vacuum (APT5 CLEANPULSE/THINBLOOD-style, extends INC-011)</description>
  <mitre><id>T1070.002</id></mitre>
  <group>log_tampering,apt5,attack,</group>
</rule>
```

> **Prereq on the endpoint:** auditd command logging via Wazuh's reserved key, feeding rule `80792` → `100025`:
> ```bash
> sudo auditctl -a always,exit -F arch=b64 -S execve -k audit-wazuh-c
> sudo auditctl -a always,exit -F arch=b32 -S execve -k audit-wazuh-c
> ```
> FIM for the web root (agent `ossec.conf`):
> ```xml
> <syscheck>
>   <directories check_all="yes" realtime="yes" report_changes="yes">/var/www</directories>
> </syscheck>
> ```

---

## 3. Kill chain (executed live)

| Time | Stage | Action | MITRE | Alert |
|------|-------|--------|-------|-------|
| 18:55 | Recon | nmap service scan — found Apache (80), SSH (22), LDAP (389) | T1595 / T1046 | 100004 |
| 18:58 | Initial access | Web shell dropped → `/var/www/html/status.php` | T1505.003 | **100023** |
| 19:06 | Persistence | Backdoor sudo account `svc-update` created | T1136 | **100024** |
| 19:59 | Defense evasion | Journal wiped — `journalctl --vacuum-time=1s` | T1070.002 | **100025** |
| 20:04 | Command & control | Login attempts from known-bad IP as `svc-update` | T1071 | **100022** |

Every stage produced an alert on the SIEM — recon through C2, fully observed.

---

## 4. Detection engineering notes (what it took to fire)

The rules didn't all work first try — the debugging *is* the lab:

- **auditd command logging needs Wazuh's reserved key.** The `audit_command` group only populates when the execve audit rule uses key `audit-wazuh-c`. A different key logs the event but never classifies it as a command.
- **First audit rule wins.** The kernel tags a syscall with the *first* matching rule's key — a stale execve rule stole the tag until flushed (`auditctl -D`).
- **`<match>` is not `<regex>`.** In Wazuh, `<match>` treats `.+` literally; real regex needs `<regex>` (OS_Regex).
- **Match decoded fields, not the raw blob.** execve args arrive as pointers in SYSCALL; the real string lives in the EXECVE record. The reliable rule keys on `audit.exe` + `audit.execve.a1` — deterministic, zero false positives on benign journalctl reads.

---

## 5. Investigation

**Workflow:** triage → scope → decisive success-vs-fail check → endpoint assessment → contain → document.

### Decisive finding — did it succeed?

| Check | Result | Meaning |
|-------|--------|---------|
| C2 login (known-bad IP) | **0 accepted auths** | No interactive access gained |
| Backdoor account `svc-update` | Exists, **Never logged in** | Persistence established, never used |
| Web shell `status.php` | Present, **no HTTP requests** | Planted, never executed |
| Log wipe (journalctl) | Local purge, **SIEM intact** | Anti-forensics defeated by off-box logging |

### Verdict

> **CONTAINED** — persistence established but never used. No confirmed hands-on access or data exfiltration. The attacker's log wipe failed against real-time off-box logging.

### IOCs

| Type | Value |
|------|-------|
| Web shell (SHA256) | `a62699820cd7ed07d5c203e73ae47a271360468c2bf5d2c5b1e0d5fe7222f8c0` |
| Web shell path | `/var/www/html/status.php` |
| Backdoor account | `svc-update` (uid 1002, added to `sudo`) |
| Attacker / C2 IP | `192.168.112.135` (flagged `APT5-ORB-C2-node`) |

### Containment & eradication

```bash
# Preserve evidence (hash matches alert 100023)
sha256sum /var/www/html/status.php
sudo cp /var/www/html/status.php ./INC-019-status.php.quarantine
# Eradicate
sudo rm -f /var/www/html/status.php
sudo userdel -r svc-update
# Contain
sudo iptables -A INPUT -s 192.168.112.135 -j DROP
```

Compromise sweep: no additional accounts, SSH keys, cron, or systemd persistence found.

### Recommendations

1. **Harden web-root permissions** — world-writable files under `/var/www` were the shell drop vector.
2. **Alert on `sudo` group changes** and restrict membership.
3. **Persist the auditd command rule** (`audit-wazuh-c`) in `/etc/audit/rules.d/` so it survives reboot.
4. **Keep real-time off-box log shipping** — validated here: it defeated the anti-forensics.

---

## 6. MITRE ATT&CK coverage

`T1595` / `T1046` (recon) · `T1505.003` (web shell) · `T1136` (create account) · `T1070.002` (clear logs) · `T1071` (C2) · `T1078` (valid accounts — attempted)

---

## Key takeaway

> *Behavior catches the unknown; intel catches the known — and you cannot delete what already left the building. Detection is only half the job: a rule you haven't fired is a rule you don't have.*

---

**Author:** Amadou MANE — Detection and Response Engineer
📺 YouTube [@cyberops401unauthorized](https://www.youtube.com/@cyberops401unauthorized) · 🔴 Twitch [cyberops401unauthorized](https://www.twitch.tv/cyberops401unauthorized) · 💻 GitHub [AmadouMan](https://github.com/AmadouMan)
