import win32com.client
import os
from pathlib import Path

# Crear un objeto de shell
shell = win32com.client.Dispatch("WScript.Shell")

# Obtener la ruta del directorio actual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta donde se guardará el acceso directo en el escritorio
desktop_path = Path.home() / "Desktop"
shortcut_path = desktop_path / "GestorDeProductos.lnk"

# Crear el acceso directo
shortcut = shell.CreateShortcut(str(shortcut_path))

# Ruta al ejecutable de tu proyecto
executable_path = Path(script_dir) / "Launcher.exe"

# Ruta al icono del acceso directo
icon_path = Path(script_dir) / "resources" / "icono.ico"

# Verificar si el ejecutable y el icono existen
if not executable_path.exists():
    print(f"Error: No se encontró el ejecutable en {executable_path}")
else:
    shortcut.TargetPath = str(executable_path)  # Ruta completa al ejecutable

if not icon_path.exists():
    print(f"Error: No se encontró el icono en {icon_path}")
else:
    shortcut.IconLocation = str(icon_path)  # Ruta completa al icono

# Guardar el acceso directo
shortcut.Save()
print(f"Acceso directo creado en el escritorio: {shortcut_path}")
