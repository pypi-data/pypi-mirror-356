%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",0)(window.close)&&exit
cd /d "%~dp0"
regsvr32 /s dm.dll