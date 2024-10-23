import os
import subprocess
import sys
import tkinter as Tk
from tkinter import messagebox
from threading import Thread

def show_message(message):
    """Muestra un cuadro de diálogo con el mensaje proporcionado."""
    messagebox.showinfo("Información", message)

def create_venv_and_install(progress_window):
    """Crea el entorno virtual y instala las dependencias."""
    venv_path = os.path.join(script_dir, 'venv')

    try:
        # Crear el entorno virtual
        subprocess.Popen([sys.executable, '-m', 'venv', venv_path], creationflags=subprocess.CREATE_NO_WINDOW).wait()

        # Actualizar pip
        subprocess.Popen([os.path.join(venv_path, 'Scripts', 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'], creationflags=subprocess.CREATE_NO_WINDOW).wait()

        # Instalar dependencias desde requirements.txt
        subprocess.Popen([os.path.join(venv_path, 'Scripts', 'pip'), 'install', '-r', 'requirements.txt'], creationflags=subprocess.CREATE_NO_WINDOW).wait()

        # Cierra la ventana de progreso
        progress_window.destroy()

        # Verificar si existe app.py y ejecutarlo
        app_path = os.path.join(script_dir, 'app.py')
        if os.path.exists(app_path):
            subprocess.Popen([os.path.join(venv_path, 'Scripts', 'python'), app_path], creationflags=subprocess.CREATE_NO_WINDOW)
            show_message("La aplicación se ha iniciado.")
        else:
            show_message("El archivo app.py no se encuentra.")

    except Exception as e:
        show_message(f"Error: {e}")

# Inicializa Tkinter
root = Tk.Tk()
root.withdraw()  # Oculta la ventana principal

# Obtiene la ruta del directorio actual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Cambia al directorio del script
os.chdir(script_dir)

# Ruta del entorno virtual
venv_path = os.path.join(script_dir, 'venv')

# Verifica si existe el entorno virtual
if os.path.exists(venv_path):
    # Verificar si el archivo requirements.txt existe
    if os.path.exists('requirements.txt'):
        # Instalar dependencias
        subprocess.Popen([os.path.join(venv_path, 'Scripts', 'python'), '-m', 'pip', 'install', '-r', 'requirements.txt'], creationflags=subprocess.CREATE_NO_WINDOW).wait()

    # Verificar si existe app.py y ejecutarlo
    app_path = os.path.join(script_dir, 'app.py')
    if os.path.exists(app_path):
        subprocess.Popen([os.path.join(venv_path, 'Scripts', 'python'), app_path], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        show_message("El archivo app.py no se encuentra.")
else:
    # Avisar al usuario que se está creando el entorno virtual
    show_message("No se encontró el entorno virtual. Se está creando uno nuevo y se instalarán las dependencias.")
    
    # Crear ventana de progreso
    progress_window = Tk.Toplevel()
    progress_window.title("Progreso")
    label = Tk.Label(progress_window, text="Creando entorno virtual e instalando dependencias...")
    label.pack(padx=20, pady=20)

    # Ejecutar la creación del entorno y la instalación en un hilo separado
    thread = Thread(target=create_venv_and_install, args=(progress_window,))
    thread.start()

# Ejecutar el bucle principal de Tkinter
root.mainloop()

