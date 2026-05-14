\# 🛡️ NightFallNode SOC Home Lab



!\[Status](https://img.shields.io/badge/Status-Operational-brightgreen)

!\[Wazuh](https://img.shields.io/badge/SIEM-Wazuh\_v4.11.1-blue)

!\[IRIS](https://img.shields.io/badge/DFIR-IRIS\_v2.4.29-purple)

!\[License](https://img.shields.io/badge/License-MIT-yellow)



\## 🏗️ Lab Architecture



| VM | Role | IP | OS |

|---|---|---|---|

| Day Gone | Attacker | 192.168.112.135 | Kali Linux |

| NexusShield-Corp | Victim Endpoint | 192.168.112.133 | Ubuntu 24.04 |

| Wazuh SIEM SecMon | SIEM | 192.168.112.131 | Ubuntu |

| DFIR-IRIS | IR Platform | 192.168.112.128 | Ubuntu |



\## ✅ Capabilities



| Capability | Status |

|---|---|

| Offensive Simulation | ✅ Operational |

| Endpoint Monitoring | ✅ Operational |

| SIEM Detection | ✅ Operational |

| Automated Alert Transfer | ✅ Operational |

| Full Incident Lifecycle | ✅ Complete |



\## 📁 Incidents



\## 📁 Incidents



| ID | Title | Date | Severity | MITRE | Status |

|---|---|---|---|---|---|

| \[INC-001](incidents/INC-001/iocs.md) | SSH Brute Force from Day Gone | 2026-05-12 | 🔴 High | T1110.001 | ✅ Contained |



\## 📊 Attack Coverage



| Tactic | Technique | Status |

|---|---|---|

| Reconnaissance | T1595 - Active Scanning | ✅ INC-001 |

| Credential Access | T1110.001 - Password Guessing | ✅ INC-001 |

| Lateral Movement | T1021.004 - SSH | ✅ INC-001 |

\## 👤

