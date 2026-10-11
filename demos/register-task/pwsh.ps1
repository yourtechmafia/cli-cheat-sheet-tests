$action  = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-File $PWD\hello.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 8am
Register-ScheduledTask -TaskName "HelloScript" -Action $action -Trigger $trigger | Select-Object TaskName, State
Unregister-ScheduledTask -TaskName "HelloScript" -Confirm:$false
