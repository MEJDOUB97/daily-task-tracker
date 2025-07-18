Set WshShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
Dim scriptPath
scriptPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))

' Run with beautiful splash screen (console hidden, GUI visible)
WshShell.Run "cmd /c cd /d """ & scriptPath & """ && python splash_screen.py", 0, False