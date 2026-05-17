\# Attack Timeline — INC-002



\## 2026-05-17 — Web Application Scan



| Time | Event | Source | Detail |

|---|---|---|---|

| 09:28:07 | Scan started | Day Gone (192.168.112.135) | nikto -h http://192.168.112.133 |

| 09:28:07 | Recon begins | Day Gone | 8,102 requests sent |

| 09:28:15 | Detection | Wazuh rule 31101 fired | Web 400 errors detected Level 5 |

| 09:28:15 | Correlation | Wazuh rule 31153 fired | Multiple 400s same IP Level 10 |

| 09:28:15 | Alert forwarded | DFIR-IRIS | 2750 alerts auto-received |

| 09:28:20 | Scan complete | Day Gone | 9 vulnerabilities found |

| 15:20:00 | Mitigation started | Amadou Mane | Apache hardening begun |

| 15:25:00 | Mitigation complete | Amadou Mane | Apache restarted — headers verified |

| 15:28:07 | Re-scan | Day Gone | Nikto re-run to verify fixes |

| 15:28:20 | Verification | Amadou Mane | 9 findings reduced to 3 — 67% fixed |



\## Result

\- ✅ Attack detected in under 1 minute

\- ✅ 2750 alerts forwarded automatically

\- ✅ 67% attack surface reduced

\- ✅ Apache hardened successfully

