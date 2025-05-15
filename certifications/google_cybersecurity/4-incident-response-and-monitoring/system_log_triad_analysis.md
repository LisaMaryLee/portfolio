# system_log_triad_analysis.md

## Suspicious Log Entries

```
Mar 13 08:42:01 ubuntu sshd[1021]: Failed password for invalid user admin from 10.0.0.5 port 54321
Mar 13 08:42:10 ubuntu sudo: pam_unix(sudo:session): session opened for user root by lisa(uid=1001)
Mar 13 08:42:12 ubuntu useradd[1098]: new user: name=malware, UID=1042
```

## Detection Actions

- Flag brute-force attempts from 10.0.0.5
- Review who accessed `sudo` (Lisa)
- Investigate the newly created `malware` user
