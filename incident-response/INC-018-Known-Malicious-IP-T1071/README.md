# INC-018 — Login Attempt from Known-Malicious IP (T1071)

> Threat-intelligence (IOC) detection and investigation of a known-bad source IP attempting SSH access to a protected endpoint.

| Field | Value |
|-------|-------|
| **Incident ID** | INC-018 |
| **Detection rule** | `100022` (level 12) |
| **MITRE ATT&CK** | T1071 — Command and Control (Application Layer Protocol) |
| **Detection type** | Threat intelligence — IOC / CDB list match |
| **Source** | 192.168.112.135 (DayGone, lab attacker) — listed as `daygone-lab-attacker` |
| **Target** | NexusShield-corp (Wazuh agent 001, 192.168.112.133) |
| **Classification** | Attempted access — **no compromise** |
| **Severity** | Medium-High (level 12) |

---

## 1. Detection

Wazuh matches the source IP of each failed-login event against a CDB list of known-malicious IPs. A hit raises a level-12 alert — detection by **who the attacker is**, independent of the behavioral brute-force rule (INC-001).

```xml
<rule id="100022" level="12">
  <if_group>authentication_failed</if_group>
  <list field="srcip" lookup="address_match_key">etc/lists/malicious-ioc/malicious-ip</list>
  <description>NightFallNode: Login attempt from known-malicious IP (threat-intel / IOC match)</description>
  <mitre><id>T1071</id></mitre>
  <group>threat_intel,ioc_match,attack,</group>
</rule>
```

**Evidence (alert document):**
```
data.srcip   : 192.168.112.135
data.srcuser : baduser
agent.name   : NexusShield-corp (001)
location     : /var/log/auth.log
full_log     : sshd[9925]: Failed password for invalid user baduser from 192.168.112.135 port 52810 ssh2
rule.id 100022 | level 12 | firedtimes 8 | MITRE T1071
```

The built-in Wazuh rule `2502` ("user missed the password more than one time") fired on the same events — **behavioral + threat-intel detection on one attack**.

---

## 2. Investigation

Driving question: **did anything succeed?**

| Step | Action | Finding |
|------|--------|---------|
| 1. Triage / validate | Why is the IP listed? FP check vs own infra. | List label `daygone-lab-attacker` — confirmed hostile, not a false positive. |
| 2. Scope the source | Pivot `data.srcip: 192.168.112.135`; other endpoints? window? | Single endpoint (NexusShield-corp); short burst of 5 attempts. |
| 3. **Success vs. fail** | `grep 'Accepted' /var/log/auth.log \| grep <IP>` | **No successful authentication** — attempt only. |
| 4. Scope accounts | Usernames? Real/privileged? Lockouts? | `baduser` — invalid account, pure guessing, low risk. |
| 5. Endpoint check | last/lastb, new users, ~/.ssh keys, cron, listeners. | No new users, no rogue keys, no cron persistence, no unexpected listeners. |
| 6. Enrich / contain / document | Reputation; block; open case. | Blocked at firewall; case documented. |

**Commands used (on the endpoint):**
```bash
sudo grep 'Accepted' /var/log/auth.log | grep 192.168.112.135   # did any login SUCCEED?
sudo lastb -n 10
sudo last -n 10
tail -5 /etc/passwd
sudo ls -la ~/.ssh/ /root/.ssh/
sudo crontab -l; ls -la /etc/cron.*
ss -tnp
```

---

## 3. Containment

- Blocked the source IP at the host firewall:
  ```bash
  sudo ufw deny from 192.168.112.135
  ```
- No account disable required (targeted user was invalid).

## 4. Eradication & Mitigation

- No artifacts to remove — attempt only, no foothold established.
- Hardening recommendations:
  - Enforce key-based SSH auth; disable password auth (`PasswordAuthentication no`).
  - Restrict SSH exposure via firewall / allowlist of admin sources.
  - Add fail2ban as a complementary host-level control.

## 5. Timeline

| Time (local) | Event |
|--------------|-------|
| 23:27 | First failed SSH login from 192.168.112.135 on NexusShield-corp |
| 23:27–23:29 | 8 failed attempts (invalid user `baduser`) — rule 100022 fires each time |
| 23:30 | Alert triaged in Wazuh Threat Hunting |
| 23:3x | Source IP blocked at firewall; endpoint verified clean |

## 6. Lessons Learned

- **Threat intel complements behavior.** The IP was flagged immediately on the first failed login — faster than waiting for the brute-force threshold. Run both detections.
- **The success/fail check is the pivot.** Failed attempts are documented noise; a single success would have escalated this to a full compromise investigation.
- **IOCs age.** A daily feed refresh (`scripts/update-iocs.sh`) keeps the list current; a static list is half fiction within weeks.

## 7. Indicators of Compromise (IOCs)

| Type | Value | Note |
|------|-------|------|
| IP | 192.168.112.135 | Source of brute-force attempts (lab: DayGone) |
| Account | baduser | Invalid username targeted |

## 8. Analyst verdict

> Known-bad IP 192.168.112.135 attempted SSH brute force against NexusShield-corp (agent 001), targeting invalid user `baduser`. 8 failed attempts, **no successful authentication**, single endpoint. Blocked at firewall. No compromise — monitoring continued.
