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

