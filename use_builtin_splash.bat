@echo off
REM Update shortcut to use the app's built-in splash screen

title Update to Built-in Splash

echo.
echo Daily Task Tracker Pro - Use Built-in Splash Screen
echo =================================================
echo.
echo You're right! The app's built-in splash screen is much better:
echo   • Professional and integrated
echo   • Shows "Preparing workspace..."
echo   • Part of the application itself
echo   • No annoying external popups
echo.

echo Updating your desktop shortcut to use direct launch...
echo This will show the app's own splash screen instead of VBScript popups.
echo.

REM Update desktop shortcut to point directly to batch file
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT_PATH=%DESKTOP%\Daily Task Tracker Pro.lnk"
set "TARGET_BAT=%~dp0run_task_tracker.bat"

echo Target: %TARGET_BAT%
echo Shortcut: %SHORTCUT_PATH%
echo.

REM Create VBScript to update the shortcut
set "VBS_TEMP=%TEMP%\update_to_builtin_splash.vbs"

(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Set oShellLink = WshShell.CreateShortcut^("%SHORTCUT_PATH%"^)
echo oShellLink.TargetPath = "%TARGET_BAT%"
echo oShellLink.WorkingDirectory = "%~dp0"
echo oShellLink.Description = "Daily Task Tracker Pro - Modern Task Management"
echo oShellLink.WindowStyle = 1
echo oShellLink.Save
) > "%VBS_TEMP%"

echo Updating shortcut...
cscript //nologo "%VBS_TEMP%" 2>nul

if exist "%SHORTCUT_PATH%" (
    echo   ✓ Desktop shortcut updated successfully!
    echo.
    echo Now your shortcut will:
    echo   • Launch directly through run_task_tracker.bat
    echo   • Show the app's beautiful built-in splash screen
    echo   • Display "Preparing workspace..." message
    echo   • No external VBScript popups
) else (
    echo   ✗ Could not find desktop shortcut
    echo   Create a new shortcut pointing to: %TARGET_BAT%
)

REM Clean up the annoying VBScript launcher
if exist "launch_silent_with_splash.vbs" (
    echo.
    echo Removing the annoying VBScript launcher...
    del "launch_silent_with_splash.vbs" 2>nul
    echo   ✓ Deleted: launch_silent_with_splash.vbs
)

REM Clean up temp file
if exist "%VBS_TEMP%" del "%VBS_TEMP%"

echo.
echo =======================================
echo PERFECT! Now you have:
echo =======================================
echo   • Direct launch to your app
echo   • Beautiful built-in splash screen
echo   • Professional "Preparing workspace..." message
echo   • No annoying external popups
echo   • Clean, integrated experience
echo.
echo Test it: Double-click your desktop shortcut now!

echo.
pause