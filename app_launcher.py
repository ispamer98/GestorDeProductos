import os
import subprocess
import sys


def create_virtualenv():
    if not os.path.exists(".venv"):
        print("Creando entorno virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
        print("Entorno virtual creado.")

        # Actualizar pip
        upgrade_pip()
    else:
        print("El entorno virtual ya existe.")


def upgrade_pip():
    print("Actualizando pip...")
    subprocess.check_call([os.path.join('.venv', 'Scripts', 'python.exe'), '-m', 'pip', 'install', '--upgrade', 'pip'],
                          stderr=subprocess.STDOUT)


def install_dependencies():
    print("Instalando dependencias...")
    try:
        subprocess.check_call(
            [os.path.join('.venv', 'Scripts', 'python.exe'), '-m', 'pip', 'install', '-r', 'requirements.txt'],
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias: {e.output.decode() if e.output else 'sin salida para decodificar.'}")
        sys.exit(1)


def run_app():
    print("Ejecutando la aplicación...")
    try:
        subprocess.check_call([os.path.join('.venv', 'Scripts', 'python.exe'), 'app.py'])
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar la aplicación: {e.output.decode() if e.output else 'sin salida para decodificar.'}")
        sys.exit(1)


def main():
    create_virtualenv()

    # Verificar si 'venv' existe antes de instalar dependencias
    if os.path.exists(".venv"):
        install_dependencies()
        run_app()


if __name__ == "__main__":
    main()
