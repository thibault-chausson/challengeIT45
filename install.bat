:: Ce script installe Python 3.7.8 si il n'y a pas Python d'installé ou si la version est inférieure à 3.0.0
@echo off
setlocal

set "var=blah 0.0.0"
py --version > temp
set /p var=<temp
del temp

for /f "tokens=2" %%G IN ("%var%") DO call :testVersions %%G 3.0.0
if "%petit%" == "oui" (
	call :install
)


echo Vous pouvez fermer cette fenetre.
pause
exit /b


:testVersions  version1  version2
set "version=%1"
set "grand=non"
set "petit=non"
set "egal=non"
call :compareVersions %1 %2
if %errorlevel% == 1 set "grand=oui"
if %errorlevel% == 0 set "egal=oui"
if %errorlevel% == -1 set "petit=oui"
exit /b

:compareVersions  version1  version2
:: Compares two version numbers and returns the result in the ERRORLEVEL
::
:: Returns 1 if version1 > version2
::         0 if version1 = version2
::        -1 if version1 < version2
::
:: The nodes must be delimited by . or , or -
setlocal enableDelayedExpansion
set "v1=%~1"
set "v2=%~2"
call :divideLetters v1
call :divideLetters v2
:loop
call :parseNode "%v1%" n1 v1
call :parseNode "%v2%" n2 v2
if %n1% gtr %n2% exit /b 1
if %n1% lss %n2% exit /b -1
if not defined v1 if not defined v2 exit /b 0
if not defined v1 exit /b -1
if not defined v2 exit /b 1
goto :loop

:parseNode  version  nodeVar  remainderVar
for /f "tokens=1* delims=.,-" %%A in ("%~1") do (
  set "%~2=%%A"
  set "%~3=%%B"
)
exit /b

:divideLetters  versionVar
for %%C in (a b c d e f g h i j k l m n o p q r s t u v w x y z) do set "%~1=!%~1:%%C=.%%C!"
exit /b



:install
echo Vous n'avez pas Python 3 d'installe sur votre ordinateur (l'installation necessite des droits administrateur).
SET /P AREYOUSURE= Voulez-vous proceder a l'installation (y / n) ? 
IF /I "%AREYOUSURE%" NEQ "y" exit /b
echo Telechargement de Python 3.7.8...
curl "https://www.python.org/ftp/python/3.7.8/python-3.7.8-amd64.exe" > %HOMEPATH%\Downloads\python3.7.8-installation.exe
echo Installation, veuillez patienter...
%HOMEPATH%\Downloads\python3.7.8-installation.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
del %HOMEPATH%\Downloads\python3.7.8-installation.exe
echo Python installe

exit /b