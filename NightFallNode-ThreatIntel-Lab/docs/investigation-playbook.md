# SOC Investigation Playbook — Known-Malicious IP on an Endpoint

Alert: `rule.id 100022` — "Login attempt from known-malicious IP (threat-intel / IOC match)".
Driving question throughout: **did anything succeed?**

## 1. Triage / validate
- Why is the IP on the list? Read the CDB label (e.g. `feodo-c2`, `tor-exit`).
- Confirm it is not your own infrastructure (scanner, VPN, jump host) wrongly listed -> false positive check.

## 2. Scope the source
Pivot on the IP, not the rule, in Threat Hunting:
```
data.srcip: <IP>
```
Add columns `agent.name`, `data.srcuser`, `rule.id`. Note how many endpoints and the time window.

## 3. Success vs. fail (decisive)
```
data.srcip: <IP> and rule.groups: authentication_success
```
or on the endpoint:
```
sudo grep 'Accepted' /var/log/auth.log | grep <IP>
```
No result -> attempt only. Any result -> compromise: record user + time, go to containment.

## 4. Scope the accounts
Which usernames (`data.srcuser`)? Any real or privileged ones? Check lockouts.

## 5. Endpoint compromise check
```
sudo last -n 10
sudo lastb -n 10
tail -5 /etc/passwd
sudo ls -la ~/.ssh/ /root/.ssh/
sudo crontab -l; ls -la /etc/cron.*
ss -tnp
```

## 6. Enrich / contain / document
- Enrich (real-world): AbuseIPDB, VirusTotal, GreyNoise.
- Contain: `sudo ufw deny from <IP>`; disable any targeted real account.
- Document: open a DFIR-IRIS case with the IOC, timeline, scope, and verdict.

## Verdict template
who -> what -> scope -> success/fail -> action -> verdict
