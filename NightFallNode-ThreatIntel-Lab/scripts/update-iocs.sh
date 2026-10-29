#!/bin/bash
# Daily refresh of the malicious-IP CDB list from a public threat feed.
# cron: 0 5 * * * root /usr/local/bin/update-iocs.sh
set -e
LIST=/var/ossec/etc/lists/malicious-ioc/malicious-ip
TMP=$(mktemp)

# keep manual/lab entries (RFC1918 lab net + any you pinned)
grep -E '^(192\.168\.|10\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)' "$LIST" > "$TMP" 2>/dev/null || true

# abuse.ch Feodo Tracker C2 IP blocklist
curl -s https://feodotracker.abuse.ch/downloads/ipblocklist.txt \
  | grep -vE '^#' | grep -E '^[0-9]' \
  | awk '{print $1":feodo-c2"}' >> "$TMP"

sort -u "$TMP" > "$LIST"
rm -f "$TMP"

# recompile + reload (manager compiles CDB lists on restart)
systemctl restart wazuh-manager
logger "update-iocs: malicious-ip refreshed ($(wc -l < "$LIST") entries)"
