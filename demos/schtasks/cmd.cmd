schtasks /create /tn "HelloScript" /tr "\"%CD%\hello.cmd\"" /sc daily /st 08:00 /f
schtasks /query /tn "HelloScript"
schtasks /delete /tn "HelloScript" /f
