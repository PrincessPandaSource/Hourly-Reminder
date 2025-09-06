REM This batch file automatically compiles the code into an executable with its dependecies and then copies the customization files to its directory

@echo off
echo Building executable...
pyinstaller main.spec --clean --noconfirm

echo Copying customization files
copy reminders_data.json dist\HourlyReminder\
xcopy /E /I /Y assets dist\HourlyReminder\assets

echo Build complete. Files are in the HourlyReminder folder in the dist folder.