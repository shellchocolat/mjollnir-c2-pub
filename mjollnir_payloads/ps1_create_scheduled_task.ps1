$Action = New-ScheduledTaskAction -Execute '{{PROGRAM}}' {{PROGRAM_ARG}}
$Trigger = New-ScheduledTaskTrigger {{FREQUENCY}} {{AT_TIME}}
$Settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable -WakeToRun
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings
Register-ScheduledTask -TaskName '{{TASK_NAME}}' -InputObject $Task