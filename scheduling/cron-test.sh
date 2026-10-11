#!/usr/bin/env bash
# Prove a cron entry fires: schedule hello.sh every minute, wait, read the log, remove it.
set -u
work=$(mktemp -d)
printf '#!/usr/bin/env bash\necho "Hello from cron at $(date +%%H:%%M:%%S)"\n' > "$work/hello.sh"
chmod +x "$work/hello.sh"
cd "$work"

echo '$ crontab -l'
crontab -l
echo "\$ (crontab -l 2>/dev/null; echo \"* * * * * \$PWD/hello.sh >> \$PWD/hello.log 2>&1\") | crontab -"
(crontab -l 2>/dev/null; echo "* * * * * $PWD/hello.sh >> $PWD/hello.log 2>&1") | crontab -
echo '$ crontab -l'
crontab -l | sed "s#$work#~/practice#g"

for _ in $(seq 1 30); do [ -s hello.log ] && break; sleep 5; done
echo '$ cat hello.log'
cat hello.log
crontab -r
echo '$ crontab -l   (after crontab -r)'
crontab -l
[ -s hello.log ]
