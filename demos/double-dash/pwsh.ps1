New-Item -ItemType File "-oops.txt" | Out-Null
Get-ChildItem -oops.txt
Get-ChildItem "-oops.txt" -Name
Remove-Item "-oops.txt"
