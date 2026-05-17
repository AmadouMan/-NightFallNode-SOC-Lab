\# IOCs — INC-002 Web Application Scan



\## Incident Details

\- \*\*Date:\*\* 2026-05-17

\- \*\*Analyst:\*\* Amadou Mane (NightFallNode)

\- \*\*Severity:\*\* Medium

\- \*\*Status:\*\* Contained ✅

\- \*\*Tool Used:\*\* Nikto v2.5.0



\## Network Indicators



| IOC | Type | Role | TLP |

|---|---|---|---|

| 192.168.112.135 | IP Address | Attacker — Day Gone VM (Kali) | RED |

| 192.168.112.133 | IP Address | Victim — NexusShield-corp | AMBER |

| Port 80 HTTP | Service | Attack vector | AMBER |



\## Vulnerabilities Found



| Finding | Severity | Fixed |

|---|---|---|

| Apache version exposed | Medium | ✅ Yes |

| Missing X-Frame-Options | Medium | ✅ Yes |

| Missing X-Content-Type | Medium | ✅ Yes |

| ETag inode leak CVE-2003-1418 | Low | ✅ Yes |

| /backup/ exposed | High | ✅ Yes |

| /dev/ indexing | Medium | ✅ Yes |

| /admin/ exposed | High | 🔄 Partial |

| No rate limiting | High | ✅ Yes |



\## MITRE ATT\&CK



| ID | Name | Tactic |

|---|---|---|

| T1190 | Exploit Public Facing App | Initial Access |

| T1083 | File and Directory Discovery | Discovery |

| T1595 | Active Scanning | Reconnaissance |



