# Lab: Threat Intelligence in Wazuh — Detect & Investigate a Known-Malicious IP (INC-018)

Detection by **known indicator** (IOC/CDB lists) to run alongside the behavioral rules — then a full **SOC investigation** of the resulting alert.

## Contents
- `wazuh/rules/nightfallnode_identity_and_threatintel.xml` — rules 100017-100022 (Keycloak authz/authn + threat-intel IP match), for the `nightfallnode_soc` group
- `wazuh/lists/malicious-ip.sample` — CDB list format (IP:label)
- `wazuh/ossec.conf-ruleset-snippet.xml` — list registration
- `scripts/update-iocs.sh` — daily feed refresh (abuse.ch Feodo Tracker)
- `docs/investigation-playbook.md` — the SOC investigation runbook
- `docs/Lab6_ThreatIntel_IOC_Investigation.pdf` — full write-up

## Pipeline
feed / manual entry -> CDB list -> compiled .cdb -> rule 100022 (srcip lookup) -> level-12 alert -> investigation

## Proof
Attacker (DayGone, 192.168.112.135) brute-forced the protected endpoint (NexusShield-corp, agent 001).
Rule 100022 fired at level 12, MITRE T1071 — detection by the attacker's IP, before the behavioral pattern completed.
