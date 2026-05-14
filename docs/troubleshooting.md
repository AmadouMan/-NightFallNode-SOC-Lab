\# Troubleshooting Guide — NightFallNode SOC Lab



\## Wazuh → DFIR-IRIS Integration Issues



| Symptom | Cause | Fix |

|---|---|---|

| 401 Unauthorized | Wrong API key | Regenerate key in IRIS profile |

| 404 Not Found | Wrong endpoint | Check IRIS version endpoint |

| Empty integration log | Script never called | Lower level to 3 in ossec.conf |

| Connection refused | IRIS not running | Check docker ps on IRIS VM |

| Permission denied | Wrong permissions | chmod 750 + chown root:wazuh |

| No alerts in IRIS | Wrong script name | Match name in ossec.conf exactly |



\## Common Commands



\### On Wazuh SIEM SecMon VM (192.168.112.131)

```bash

\# Check integration log

sudo tail -f /var/ossec/logs/integrations.log



\# Check alerts log

sudo tail -f /var/ossec/logs/alerts/alerts.json



\# Test connectivity to IRIS

curl -k https://192.168.112.128/api/ping



\# Test script manually

sudo python3 /var/ossec/integrations/custom-iris.py \\

&#x20; /tmp/test-alert.json



\# Restart Wazuh

sudo systemctl restart wazuh-manager



\# Check script permissions

sudo ls -la /var/ossec/integrations/custom-iris.py

\# Should show: -rwxr-x--- root wazuh

```



\### On DFIR-IRIS VM (192.168.112.128)

```bash

\# Check Docker containers

docker ps



\# Check IRIS logs

docker logs iris\_app



\# Disable sleep

gsettings set org.gnome.desktop.session idle-delay 0

```



\## Network Connectivity Test

```bash

\# From Wazuh VM - ping IRIS

ping 192.168.112.128



\# From Day Gone - ping NexusShield

ping 192.168.112.133



\# Test SSH target

nmap -p 22 192.168.112.133

```



\## Wazuh Agent Issues



| Issue | Fix |

|---|---|

| Agent disconnected | sudo systemctl restart wazuh-agent |

| No events showing | Check agent status in dashboard |

| Wrong IP showing | Check agent.conf on endpoint |



\## DFIR-IRIS Issues



| Issue | Fix |

|---|---|

| Template error | Leave template field empty |

| Case merge bug | Skip template selection |

| Report empty | Set severity and owner in case |

| Sleep too fast | gsettings idle-delay 0 |

