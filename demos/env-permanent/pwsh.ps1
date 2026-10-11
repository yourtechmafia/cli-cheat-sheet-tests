[Environment]::SetEnvironmentVariable("GREETING", "hello", "User")
[Environment]::GetEnvironmentVariable("GREETING", "User")
"this session: [$env:GREETING]"
