grep zzz log.txt
echo "grep found nothing: $?"
nosuchcommand
echo "command not found: $?"
./hello.sh
echo "not executable: $?"
sh -c 'kill -INT $$'
echo "stopped by Ctrl+C (SIGINT): $?"
