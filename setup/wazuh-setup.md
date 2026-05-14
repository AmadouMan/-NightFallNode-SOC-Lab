\# Wazuh SIEM Setup Guide



\## Environment

\- \*\*VM:\*\* Wazuh SIEM SecMon

\- \*\*IP:\*\* 192.168.112.131

\- \*\*OS:\*\* Ubuntu 24.04 LTS

\- \*\*Version:\*\* Wazuh v4.11.1



\## Components Installed

\- Wazuh Manager

\- Elasticsearch / Indexer

\- Wazuh Dashboard

\- Custom IRIS Integration Script



\## Agent Deployed

\- \*\*NexusShield-corp\*\* (192.168.112.133)

\- OS: Ubuntu 24.04 LTS

\- Version: Wazuh Agent v4.11.1

\- Status: Active



\## Key Detection Rules Triggered



| Rule ID | Level | Description |

|---|---|---|

| 5760 | 5 | sshd: authentication failed |

| 5503 | 5 | PAM: User login failed |

| 40111 | 10 | Multiple authentication failures |

| 5758 | 8 | Maximum authentication attempts exceeded |

| 2502 | 10 | User missed password more than one time |



\## MITRE ATT\&CK Coverage



| Tactic | Count |

|---|---|

| Reconnaissance | 28 |

| Defense Evasion | 9 |

| Credential Access | 8 |

| Initial Access | 6 |

| Lateral Movement | 6 |



\## Integration Configuration

See integration/integration-guide.md



\## Useful Commands

```bash

\# Check Wazuh status

sudo systemctl status wazuh-manager



\# Watch alerts live

sudo tail -f /var/ossec/logs/alerts/alerts.json



\# Watch integration log

sudo tail -f /var/ossec/logs/integrations.log



\# Restart Wazuh

sudo systemctl restart wazuh-manager

```

