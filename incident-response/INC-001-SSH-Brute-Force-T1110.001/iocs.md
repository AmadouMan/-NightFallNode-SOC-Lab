\# IOCs — INC-001 SSH Brute Force



\## Incident Details

\- \*\*Date:\*\* 2026-05-12

\- \*\*Analyst:\*\* Amadou Mane (NightFallNode)

\- \*\*Severity:\*\* High

\- \*\*Status:\*\* Contained



\## Network Indicators



| IOC | Type | Role | TLP |

|---|---|---|---|

| 192.168.112.135 | IP Address | Attacker — Day Gone VM (Kali) | RED |

| 192.168.112.133 | IP Address | Victim — NexusShield-corp | AMBER |

| Port 22 SSH | Service | Attack vector | AMBER |

| Port 80 HTTP | Service | Discovered — not exploited | GREEN |



\## Tool Indicators



| Tool | Version | Purpose |

|---|---|---|

| Nmap | 7.95 | Reconnaissance / Port scanning |

| Hydra | v9.5 | SSH Brute Force |

| rockyou.txt | - | Password wordlist (14M passwords) |



\## MITRE ATT\&CK Mapping



| ID | Name | Tactic |

|---|---|---|

| T1595 | Active Scanning | Reconnaissance |

| T1110.001 | Password Guessing | Credential Access |

| T1021.004 | SSH | Lateral Movement |



\## Verdict

\- Brute force attempts: 467

\- Successful logins: 0

\- Impact: None — attack contained



\## **Containment \& Mitigation**



\### Immediate Actions Taken

\- Identified attacker IP: 192.168.112.135 (Day Gone VM)

\- Monitored SSH logs on NexusShield-Corp: `/var/log/auth.log`

\- Confirmed 0 successful logins — no breach occurred



\### **Hardening Applied**

| Action | Command / Method |

|---|---|

| Block attacker IP via firewall | `sudo ufw deny from 192.168.112.135 to any` |

| Enable UFW | `sudo ufw enable` |

| Disable SSH root login | Set `PermitRootLogin no` in `/etc/ssh/sshd\_config` |

| Restrict SSH to key-based auth | Set `PasswordAuthentication no` in `/etc/ssh/sshd\_config` |

| Restart SSH service | `sudo systemctl restart ssh` |

| Set login attempt limit (fail2ban) | `sudo apt install fail2ban -y` |



\---



\## **Lessons Learned**



\### What Worked

\- Wazuh rule 100001 successfully detected brute force via SID 5760

\- IRIS alert was generated and triaged correctly

\- Attack was detected before any successful authentication



\### **What Could Be Improved**

| Gap | Recommendation |

|---|---|

| SSH exposed with password auth | Enforce key-based authentication by default |

| No automated block on brute force | Deploy Fail2ban to auto-ban IPs after 5 failures |

| Alert took manual review | Configure IRIS auto-escalation for Level 12+ alerts |

| No GeoIP enrichment | Add GeoIP module to Wazuh for attacker location context |



\### **Detection Coverage**

| Layer | Tool | Status |

|---|---|---|

| Network | Wazuh Agent (NexusShield) | ✅ Detected |

| SIEM Correlation | Wazuh Rule 100001 | ✅ Fired |

| Case Management | DFIR-IRIS | ✅ Alert created |

| Automated Response | Fail2ban | ⚠️ Not deployed |



\---



\#**# Timeline**



| Time | Event |

|---|---|

| T+00:00 | Nmap reconnaissance initiated from Day Gone VM |

| T+00:05 | Hydra SSH brute force started (rockyou.txt, 467 attempts) |

| T+00:06 | Wazuh Rule 100001 fired — alert sent to IRIS |

| T+00:08 | Analyst (NightFallNode) triaged alert in IRIS |

| T+00:15 | Attacker IP blocked via UFW |

| T+00:20 | SSH hardened — password auth disabled |

| T+00:25 | Incident contained \& closed |



\---



**## Incident Status:** CLOSED — CONTAINED

\*\*Closed by:\*\* Amadou Mane (NightFallNode)

\*\*Closed date:\*\* 2026-05-17

\*\*Resolution:\*\* No breach. Attacker blocked. SSH hardened.

