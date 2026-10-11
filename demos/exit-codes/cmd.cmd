findstr zzz log.txt
echo findstr exit code: %ERRORLEVEL%
nosuchcommand
echo command not found: %ERRORLEVEL%
