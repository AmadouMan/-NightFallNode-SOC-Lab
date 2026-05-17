\# Mitigation Playbook — INC-002

\# Web Application Scan Response



\## Incident Reference

\- \*\*Case:\*\* INC-002

\- \*\*Attack:\*\* Web Application Scan (Nikto v2.5.0)

\- \*\*Analyst:\*\* Amadou Mane (NightFallNode)

\- \*\*Date:\*\* 2026-05-17

\- \*\*Target:\*\* NexusShield-corp (192.168.112.133)

\- \*\*Attacker:\*\* Day Gone VM (192.168.112.135)



\---



\## 🔴 Before Mitigation — 9 Findings

\- Apache/2.4.58 version exposed

\- Missing X-Frame-Options header

\- Missing X-Content-Type-Options header

\- ETags leaking inodes (CVE-2003-1418)

\- /admin/ directory accessible

\- /backup/ directory exposed

\- /dev/ directory with indexing

\- /admin/index.html admin login exposed

\- No rate limiting / scan protection



\---



\## 📋 Step-by-Step Response



\### STEP 1 — Disable Directory Listing

\*\*Problem:\*\* /dev/ had directory indexing enabled

\*\*Risk:\*\* Attacker can browse all files

\*\*Fix:\*\*

```bash

sudo nano /etc/apache2/apache2.conf

\# Changed:

\# Options Indexes FollowSymLinks

\# To:

\# Options -Indexes +FollowSymLinks

```

\*\*Verify:\*\*

```bash

grep -n "Indexes" /etc/apache2/apache2.conf

\# Result: Options -Indexes +FollowSymLinks ✅

```



\---



\### STEP 2 — Add Security Headers

\*\*Problem:\*\* Missing X-Frame-Options and X-Content-Type

\*\*Risk:\*\* Clickjacking and MIME sniffing attacks

\*\*Fix:\*\*

```bash

sudo a2enmod headers

sudo nano /etc/apache2/conf-available/security.conf

\# Added:

Header always set X-Frame-Options "SAMEORIGIN"

Header always set X-Content-Type-Options "nosniff"

Header always set X-XSS-Protection "1; mode=block"

Header always set Referrer-Policy "strict-origin"

```

\*\*Verify:\*\*

```bash

curl -I http://192.168.112.133

\# X-Frame-Options: SAMEORIGIN ✅

\# X-Content-Type-Options: nosniff ✅

\# X-XSS-Protection: 1; mode=block ✅

\# Referrer-Policy: strict-origin ✅

```



\---



\### STEP 3 — Hide Apache Version

\*\*Problem:\*\* Apache/2.4.58 fully exposed

\*\*Risk:\*\* Attacker targets known CVEs

\*\*Fix:\*\*

```bash

sudo nano /etc/apache2/conf-available/security.conf

\# ServerTokens OS → ServerTokens Prod

\# ServerSignature On → ServerSignature Off

```

\*\*Verify:\*\*

```bash

curl -I http://192.168.112.133

\# Server: Apache (no version) ✅

```



\---



\### STEP 4 — Fix ETag Inode Leak

\*\*Problem:\*\* ETags leaking server inode numbers

\*\*CVE:\*\* CVE-2003-1418

\*\*Risk:\*\* Information disclosure

\*\*Fix:\*\*

```bash

sudo nano /etc/apache2/conf-available/security.conf

\# Added: FileETag None

```

\*\*Verify:\*\*

```bash

curl -I http://192.168.112.133

\# No ETag header present ✅

```



\---



\### STEP 5 — Remove Sensitive Directories

\*\*Problem:\*\* /backup/ and /dev/ on web server

\*\*Risk:\*\* Sensitive files accessible

\*\*Fix:\*\*

```bash

ls /var/www/html/

\# Found: admin backup dev dvwa index.html xss\_vuln.php

sudo rm -rf /var/www/html/backup

sudo rm -rf /var/www/html/dev

```

\*\*Verify:\*\*

```bash

ls /var/www/html/

\# Result: admin dvwa index.html xss\_vuln.php ✅

```



\---



\### STEP 6 — Install Fail2Ban

\*\*Problem:\*\* No protection against web scanning

\*\*Risk:\*\* Unlimited automated scanning

\*\*Fix:\*\*

```bash

sudo apt install fail2ban -y

sudo nano /etc/fail2ban/jail.local

\# Added apache-scan jail:

\# maxretry=50, findtime=60, bantime=7200



sudo nano /etc/fail2ban/filter.d/apache-scan.conf

\# failregex = ^<HOST>.\*"(GET|POST|HEAD).\*" (400|404|403)



sudo systemctl enable fail2ban

sudo systemctl start fail2ban

```

\*\*Verify:\*\*

```bash

sudo systemctl status fail2ban

\# active (running) ✅

```



\---



\### STEP 7 — Restart Apache

```bash

sudo systemctl restart apache2

sudo systemctl status apache2

\# active (running) ✅

```



\---



\### STEP 8 — Add Wazuh Custom Rules

```bash

sudo nano /var/ossec/etc/rules/local\_rules.xml

\# Added rule 100001 — Nikto detection Level 12

\# Added rule 100002 — Sensitive dir access Level 12

sudo systemctl restart wazuh-manager

```



\---



\### STEP 9 — Re-scan Verification

```bash

\# From Day Gone VM:

nikto -h http://192.168.112.133

\# Before: 9 findings

\# After:  3 findings ✅

```



\---



\## 🟢 After Mitigation — Only 3 Findings



| Finding | Before | After | Status |

|---|---|---|---|

| Server version | Apache/2.4.58 | Apache | ✅ Fixed |

| X-Frame-Options | Missing | SAMEORIGIN | ✅ Fixed |

| X-Content-Type | Missing | nosniff | ✅ Fixed |

| ETag inode leak | Present | None | ✅ Fixed |

| /backup/ exposed | Yes | Deleted | ✅ Fixed |

| /dev/ indexing | Yes | Deleted | ✅ Fixed |

| Rate limiting | None | Fail2Ban | ✅ Fixed |

| Total findings | 9 | 3 | ✅ 67% reduced |



\## ⚠️ Remaining Risk

\- /admin/ needs password authentication

\- HTTP OPTIONS method allowed (low risk)



\## 📚 Lessons Learned

1\. Apache default config is insecure out of the box

2\. Security headers must be explicitly configured

3\. Sensitive directories must never be in web root

4\. Rate limiting prevents automated scanning

5\. Wazuh detected scan in under 1 minute ✅

6\. DFIR-IRIS received 2750 alerts automatically ✅

7\. Mitigation reduced attack surface by 67% ✅

8\. Re-scanning confirms effectiveness of fixes ✅



\## 🔧 Future Improvements

\- Install ModSecurity WAF

\- Implement HTTPS/TLS

\- Password protect /admin/ directory

\- Disable HTTP OPTIONS method

\- Regular vulnerability assessments

