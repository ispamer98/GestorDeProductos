# AccesFrame.py
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import Frame, Label, Button
from PIL import Image, ImageTk
import db
from models import User



# Creamos el frame de Acceso al usuario
class AccesFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent) # Inicia el constructor de la clase principal
        self.controller = controller # Pasamos el controlador que es la primera ventana

        # Cargamos y configuramos la imagen de fondo
        self.image = Image.open("resources/background.jpeg")
        self.image = self.image.resize((600, 800), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(self, image=self.image_tk)
        self.image_label.grid(row=0, column=0, sticky='nsew')

        # Configuramos la fila y columna para que se ajusten al tamaño de la ventana
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


        # Definimos el estilo de los botones por defecto
        button_style = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat"}

        # Creamos un campo de entrada para el nombre de usuario.
        self.userEntry = Entry(self, font=("Comic Sans MS", 12))
        self.userEntry.place(relx=0.5, rely=0.4, anchor="center", width=150)
        self.userEntry.bind("<Return>", lambda event: self.logIn())


        # Creamos una etiqueta que indica el campo de nombre de usuario.
        self.userLabel = Label(self, text="Usuario:", font=("Comic Sans MS", 12), fg="black")
        self.userLabel.place(relx=0.27, rely=0.4, anchor="center")

        # Crea un campo de entrada para la contraseña, que oculta el texto ingresado.
        self.paswEntry = Entry(self, font=("Comic Sans MS", 12), show="*")
        self.paswEntry.place(relx=0.5, rely=0.6, anchor="center", width=150)
        # Al pulsar enter, hará la misma función que el boton de logIn
        self.paswEntry.bind("<Return>", lambda event: self.logIn())

        # Creamos una etiqueta que indica el campo de contraseña.
        self.paswLabel = Label(self, text="Contraseña:", font=("Comic Sans MS", 12), fg="black")
        self.paswLabel.place(relx=0.25, rely=0.6, anchor="center")

        # Crea un botón que, al ser presionado, intenta iniciar sesión.
        self.logInButton = Button(self, text="Iniciar Sesión", **button_style, command=self.logIn)
        self.logInButton.place(relx=0.5, rely=0.75, anchor="center")

        # Crea un botón para volver al frame principal.
        self.back_button = Button(self, text="Atrás", bg="#333333", fg="white",**button_style, command=self.goBack)
        self.back_button.place(relx=0.003, rely=0.003, anchor="nw")

        self.pasw_attempts = 0 # Establecemos el numero de intentos de contraseña a 0
        self.pasw_blocked = False # Y el bloqueo del campo de contraseña a False


    # Función que se encargará de avisar del bloqueo de contraseña
    def block_password(self):
        self.pasw_blocked = True # Modificamos el estado a True
        self.paswEntry.config(state='disabled',bg="#333") # Bloqueamos la entrada de la contraseña
        # Creamos una etiqueta que nos avisará del bloqueo
        self.block_label = Label(self, text="30", font=("Comic Sans MS", 12), fg="red")
        self.block_label.place(relx=0.5, rely=0.65, anchor="center")
        # Establecemos un contador de 10 segundos
        self.countdown(10)

    # Limpiamos el campo de contraseña
    def clear_entries(self):
        self.paswEntry.delete(0, END)

    # Creamos un contador para el bloqueo de contraseña
    def countdown(self, count):
        if count > 0: # Mientras que el conteo sea mayor que 0
            # Muestra una etiqueta con los segundos restantes
            self.block_label.config(text=f"Intentalo de nuevo en {count} segundos")
            # Cada 1000 milisegundos, el conteo actualiza su contenido a -1
            self.after(1000, self.countdown, count - 1)

        else:
            # Cuando el conteo llega a 0
            self.pasw_blocked = False # El estado vuelve a su origen
            self.paswEntry.config(state='normal',bg="white") # Deja de bloquear el campo de contraseña
            self.block_label.destroy() # Elimina la etiqueta de contador

    # Vuelta al frame principal
    def goBack(self):
        # Cambia a la pantalla del frame principal.
        self.controller.show_frame("FirstFrame",title="App Gestor de Productos")

    # Elimina las etiquetas de error (Rojas)
    def clear_error_labels(self):
        for widget in self.winfo_children():
            if isinstance(widget, Label) and widget.cget('fg') == 'red':
                widget.destroy()

    # Función que se encarga de hacer el log in en el usuario

    def logIn(self):
        self.clear_error_labels() # Limpia las label de error en caso de que existan

        # Captura el usuario y la contraseña proporcionados en las entradas
        username=self.userEntry.get()
        pasw=self.paswEntry.get()

        # Si el usuario NO está vacio
        if username != "":
            # Lo primero es buscar coincidencias en la base de datos
            user = db.session.query(User).filter_by(username=username).first()

            # Si encuentra coincidencias
            if user :
                #  Codifica la contraseña obtenida, y la compara con la de la base de datos
                if user.pasw == pasw.encode('utf-8').hex():
                    # Si tiene exito, limpia el campo de contraseña
                    self.paswEntry.delete(0, END)
                    self.pasw_attempts = 0 # Establece los intentos a 0

                    # Si el usuario encontrado NO es administrador, entonces accede al panel de usuario
                    if user.admin == False:
                        self.controller.show_frame("UserFrame",user=user,title=f"Panel de {user.username}")

                    # Si el usuario SI es administrador, accede al panel de administrador
                    elif user.admin == True:
                        self.controller.show_frame("AdminFrame",user=user,title=f"Panel de {user.username} (ADMIN)")

                # En caso de no coincidir la contraseña proporcionada con la de la base de datos
                elif pasw != "" and user.pasw != pasw.encode('utf-8').hex():
                    self.pasw_attempts += 1 # Suma un intento de acceso

                    # Muestra una etiqueta de error con el numero de intentos actual
                    self.pasw_incorrect_label = Label(self, text=f"Contraseña incorrecta ({self.pasw_attempts} / 5)", font=("Comic Sans MS", 12),fg="red")
                    self.pasw_incorrect_label.place(relx=0.5, rely=0.65, anchor="center")

                    self.paswEntry.delete(0, END) # Y borra el campo de contraseña

                    # Cuando el total de intentos, llega a 5
                    if self.pasw_attempts >= 5:
                        # Limpia las etiquetas de error
                        self.clear_error_labels()
                        # Llama al bloqueo de contraseña
                        self.block_password()
                        # Una vez acaba este bloqueo, los intentos vuelven a 0
                        self.pasw_attempts=0

            # En caso de no encontrar el usuario
            else:
                # Se crea una etiqueta de error
                self.user_not_found_label = Label(self, text="Usuario no encontrado", font=("Comic Sans MS", 12), fg="red")
                self.user_not_found_label.place(relx=0.5, rely=0.45, anchor="center")

        # Si el campo de usuario se encuentra vacio
        else:
            # Muestra una etiqueta de error
            self.user_empty_label = Label(self, text="Usuario no puede estar vacio", font=("Comic Sans MS", 12), fg="red")
            self.user_empty_label.place(relx=0.5, rely=0.45, anchor="center")

        # Si el campo de contraseña se encuentra vacio
        if pasw == "":
            # Muestra una etiqueta de error
            self.pasw_empty_label = Label(self, text="Contraseña no puede estar vacio", font=("Comic Sans MS", 12), fg="red")
            self.pasw_empty_label.place(relx=0.5, rely=0.65, anchor="center")



