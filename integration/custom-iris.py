#!/usr/bin/env python3
# ============================================
# Wazuh -> DFIR-IRIS Integration Script
# Author: Amadou Mane (NightFallNode)
# Version: 1.0
# Description: Automatically forwards Wazuh
#              alerts to DFIR-IRIS platform
# ============================================

import json
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Replace with your values
API_KEY  = "YOUR_IRIS_API_KEY_HERE"
IRIS_URL = "https://YOUR_IRIS_IP_HERE"

alert_file = sys.argv[1]

with open(alert_file) as f:
    alert = json.load(f)

rule       = alert.get("rule", {})
agent      = alert.get("agent", {})
title      = rule.get("description", "Wazuh Alert")
level      = int(rule.get("level", 3))
agent_name = agent.get("name", "Unknown")
agent_ip   = agent.get("ip", "Unknown")

# Map Wazuh level to IRIS severity
if level >= 12:
    severity = 5   # Critical
elif level >= 10:
    severity = 4   # High
elif level >= 7:
    severity = 3   # Medium
elif level >= 4:
    severity = 2   # Low
else:
    severity = 1   # Informational

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "alert_title":       f"[Wazuh] {title}",
    "alert_description": f"Agent: {agent_name} ({agent_ip})\nRule: {rule.get('id','N/A')} Level: {level}\n\n{json.dumps(alert, indent=2)}",
    "alert_source":      "Wazuh SIEM",
    "alert_source_ref":  alert.get("id", "N/A"),
    "alert_severity_id": severity,
    "alert_status_id":   2,
    "alert_customer_id": 1
}

try:
    r = requests.post(
        f"{IRIS_URL}/alerts/add",
        headers=headers,
        json=payload,
        verify=False,
        timeout=10
    )
    print(f"[IRIS] Status: {r.status_code}")
    print(f"[IRIS] Response: {r.text}")
except Exception as e:
    print(f"[IRIS] ERROR: {e}", file=sys.stderr)
    sys.exit(1)