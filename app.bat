@echo off
REM Obtener la ruta del directorio donde se encuentra el archivo .bat
set SCRIPT_DIR=%~dp0

REM Cambiar al directorio del script
cd /d "%SCRIPT_DIR%"

REM Verificar si el entorno virtual existe
if not exist ".venv\Scripts\activate" (
    echo El entorno virtual no se encuentra. Creando uno nuevo...
    python -m venv .venv

    REM Activar el entorno virtual
    echo Activando el entorno virtual...
    call .venv\Scripts\activate

    REM Actualizar pip
    echo Actualizando pip...
    python -m pip install --upgrade pip

    REM Instalar dependencias desde requirements.txt
    echo Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
) else (
    REM Activar el entorno virtual
    echo Activando el entorno virtual...
    call .venv\Scripts\activate
)

REM Verificar si `app.py` existe
if exist "app.py" (
    echo Ejecutando el script Python sin ventana de terminal...
    start "" /min pythonw app.py
    echo El script se ha ejecutado.
) else (
    echo El archivo app.py no se encuentra.
    pause
)
