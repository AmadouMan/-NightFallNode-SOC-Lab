\# Wazuh to DFIR-IRIS Integration Guide



\## Overview

Custom Python script that automatically forwards

Wazuh SIEM alerts to DFIR-IRIS for incident response.



\## Lab Environment

\- Wazuh SIEM: 192.168.112.131

\- DFIR-IRIS:  192.168.112.128



\## Installation Steps



\### Step 1 - Copy script to Wazuh VM

```bash

sudo cp custom-iris.py /var/ossec/integrations/

sudo chmod 750 /var/ossec/integrations/custom-iris.py

sudo chown root:wazuh /var/ossec/integrations/custom-iris.py

```



\### Step 2 - Add to ossec.conf

```xml

<integration>

&#x20; <name>custom-iris.py</name>

&#x20; <hook\_url>https://YOUR\_IRIS\_IP</hook\_url>

&#x20; <api\_key>YOUR\_IRIS\_API\_KEY</api\_key>

&#x20; <level>3</level>

&#x20; <alert\_format>json</alert\_format>

</integration>

```



\### Step 3 - Restart Wazuh

```bash

sudo systemctl restart wazuh-manager

```



\### Step 4 - Test manually

```bash

sudo python3 /var/ossec/integrations/custom-iris.py /tmp/test-alert.json

```



\## Troubleshooting



| Issue | Solution |

|---|---|

| 401 Unauthorized | Wrong API key |

| 404 Not Found | Wrong IRIS URL |

| Empty log | Lower alert level to 3 |

| Permission denied | chmod 750 + chown root:wazuh |

