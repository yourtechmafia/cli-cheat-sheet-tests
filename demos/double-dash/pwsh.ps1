New-Item -ItemType File -Path -oops.txt | Out-Null
Get-ChildItem -oops.txt
Get-ChildItem -LiteralPath -oops.txt | Select-Object -ExpandProperty Name
Remove-Item -LiteralPath -oops.txt
