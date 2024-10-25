# FirstFrame.py

from tkinter import *
from tkinter import ttk
from tkinter import Frame, Label, Button
from PIL import Image, ImageTk



# Creamos el primer frame
class FirstFrame(Frame):
    def __init__(self, parent, controller):
        # Inicializa el constructor de la ventana principal
        Frame.__init__(self, parent)
        self.controller = controller # Guarda el controller,
        self.image = Image.open("resources/background.jpeg") # Abrimos la imagen que será el fondo de la app
        self.image = self.image.resize((600, 800), Image.LANCZOS) # Ajustamos el tamaño
        self.image_tk = ImageTk.PhotoImage(self.image) # Modificamos el formato de esta imagen

        self.image_label = Label(self, image=self.image_tk) # Creamos una etiqueta para alojar la imagen
        self.image_label.grid(row=0, column=0, sticky='nsew') # Y la ubicamos en la pantalla

        # Configuramos la fila y columna para que se ajusten al tamaño de la ventana
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Configuramos el estilo de los botones por defecto
        button_style = {"font": ("Comic Sans MS", 16, 'bold'), "bg": "white", "fg": "#333333", "padx": 10, "pady": 5, "relief": "flat"}

        # Botón Acceder
        self.acces_button = Button(self, text="Acceder", **button_style,
                                  command=lambda: controller.show_frame("AccesFrame", title="Ventana de Acceso")) # Pasamos el titulo para que se cambie al mostrar el frame de acceso
                                    # Con este comando, llamaria a la funcion para que la ventana principal muestre el frame de acceso
        self.acces_button.place(relx=0.5, rely=0.4, anchor="center", width=200, height=50) # Y ubicamos el boton

        # Botón Registrarse
        self.register_button = Button(self, text="Registrarse", **button_style,
                                     command=lambda: controller.show_frame("RegisterFrame", title="Ventana de Registro"))
                                    # Misma operacion que con el boton de acceso
        self.register_button.place(relx=0.5, rely=0.58, anchor="center", width=200, height=50)

        # Botón Salir
        self.exit_button = Button(self, text="Salir", bg="#333333", fg="white", font=("Comic Sans MS", 14),
                                 padx=10, pady=5, relief="flat", command=self.controller.close_app)
                                #En este caso, el comando llama a la funcion que cierra el programa
        self.exit_button.place(relx=0.003, rely=0.003, anchor="nw")