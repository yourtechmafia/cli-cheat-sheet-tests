New-Item -ItemType File -Path $PROFILE -Force | Out-Null
Add-Content -Path $PROFILE -Value 'function ll { Get-ChildItem -Force @args }'
