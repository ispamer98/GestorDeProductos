@echo off
setlocal

:: Obtener la ruta del script actual
cd /d %~dp0

:: Verificar si 'app_launcher.py' existe y ejecutarlo sin ventana de terminal
if exist "app_launcher.py" (
    start "" /b pythonw app_launcher.py
)

endlocal
