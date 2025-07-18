Set WshShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
Dim scriptPath
scriptPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))

' Try reliable launcher first, fallback to direct launch
' The 0 parameter means the command window will be hidden completely
WshShell.Run "cmd /c cd /d """ & scriptPath & """ && python launch_app.py", 0, False