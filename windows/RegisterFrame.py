#RegisterFrame.py
from tkinter import *
from tkinter import ttk,messagebox
import winsound
import tkinter as tk
from tkinter import Frame, Label, Button
from PIL import Image, ImageTk
import db
from models import User
import re

#Creamos el frame que se encargará del registro
class RegisterFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent) # Iniciamos el constructor de la ventana principal
        self.controller = controller # Guardamos el controlador
        self.__admin_pasw="12345" # Establecemos una contraseña de admin, para poder crear cuentas con privilegios

        # Cargamos y configuramos la imagen de fondo
        self.image = Image.open("resources/background.jpeg")
        self.image = self.image.resize((600, 800), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(self,image = self.image_tk)
        self.image_label.grid(row=0, column=0, sticky='nsew')

        # Configuramos la fila y columna para que se ajusten al tamaño de la ventana
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Estilo por defecto de los botones
        button_style = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat"}

        # Campo de entrada para el nombre de usuario
        self.userEntry = Entry(self, font=("Comic Sans MS", 12))
        self.userEntry.place(relx=0.55, rely=0.2, anchor="center", width=200)
        # Al pulsar enter, hará la misma función que el boton de registro
        self.userEntry.bind("<Return>", lambda event: self.register())

        # Etiqueta que indica el campo de nombre de usuario
        self.userLabel = Label(self, text="Usuario:", font=("Comic Sans MS", 12), fg="black", bg="white")
        self.userLabel.place(relx=0.2, rely=0.2, anchor="center")

        # Campo de entrada para la contraseña, que oculta el texto ingresado
        self.paswEntry = Entry(self, font=("Comic Sans MS", 12), show="*")
        self.paswEntry.place(relx=0.55, rely=0.3, anchor="center", width=200)
        self.paswEntry.bind("<Return>", lambda event: self.register())

        # Etiqueta que indica el campo de contraseña
        self.paswLabel = Label(self, text="Contraseña:", font=("Comic Sans MS", 12), fg="black", bg="white")
        self.paswLabel.place(relx=0.2, rely=0.3, anchor="center")

        # Campo de entrada para confirmar la contraseña
        self.pasw2Entry = Entry(self, font=("Comic Sans MS", 12), show="*")
        self.pasw2Entry.place(relx=0.55, rely=0.4, anchor="center", width=200)
        self.pasw2Entry.bind("<Return>", lambda event: self.register())

        # Etiqueta que indica el campo de confirmación de contraseña
        self.pasw2Label = Label(self, text="Confirmar\nContraseña:", font=("Comic Sans MS", 12), fg="black", bg="white")
        self.pasw2Label.place(relx=0.2, rely=0.4, anchor="center")

        # Campos de entrada para la fecha de nacimiento
        # Campo de entrada para el día
        self.dayEntry = ttk.Combobox(self, font=("Comic Sans MS", 12), width=3,values=[str(i).zfill(2) for i in range(1, 32)])
        #Establecemos los valores permitidos dentro de la combobox
        self.dayEntry.place(relx=0.4, rely=0.5, anchor="center")
        self.dayEntry.bind("<Return>", lambda event: self.register())

        # Campo de entrada para el mes
        self.monthEntry = ttk.Combobox(self, font=("Comic Sans MS", 12), width=3,values=[f"{i:02d}" for i in range(1, 13)])
        self.monthEntry.place(relx=0.53, rely=0.5, anchor="center")
        self.monthEntry.bind("<Return>", lambda event: self.register())

        # Campo de entrada para el año
        self.yearEntry = ttk.Combobox(self, font=("Comic Sans MS", 12), width=5,values=[str(i) for i in range(2020, 1960, -1)])
        self.yearEntry.place(relx=0.68, rely=0.5, anchor="center")
        self.yearEntry.bind("<Return>", lambda event: self.register())

        # Etiqueta para la fecha de nacimiento
        self.birthdayLabel = Label(self, text="Fecha de\nNacimiento:", font=("Comic Sans MS", 12), fg="black",bg="white")
        self.birthdayLabel.place(relx=0.2, rely=0.5, anchor="center")

        # Campo de entrada para el e-mail
        self.emailEntry = Entry(self, font=("Comic Sans MS", 12))
        self.emailEntry.place(relx=0.55, rely=0.6, anchor="center", width=200)
        self.emailEntry.bind("<Return>", lambda event: self.register())

        # Etiqueta para el e-mail
        self.emailLabel = Label(self, text="E-mail:", font=("Comic Sans MS", 12), fg="black", bg="white")
        self.emailLabel.place(relx=0.2, rely=0.6, anchor="center")

        # Campo de entrada para la confirmación del e-mail
        self.email2Entry = Entry(self, font=("Comic Sans MS", 12))
        self.email2Entry.place(relx=0.55, rely=0.7, anchor="center", width=200)
        self.email2Entry.bind("<Return>", lambda event: self.register())

        # Etiqueta para la confirmación del e-mail
        self.email2Label = Label(self, text="Confirmar\nE-mail:", font=("Comic Sans MS", 12), fg="black", bg="white")
        self.email2Label.place(relx=0.2, rely=0.7, anchor="center")

        # Campo de entrada para la contraseña de admin
        self.adminPaswEntry = Entry(self, font=("Comic Sans MS", 10), show="*", width=8)
        self.adminPaswEntry.place(relx=0.025, rely=0.99, anchor="sw")
        self.adminPaswEntry.bind("<Return>", lambda event: self.register())

        # Etiqueta para la contraseña de admin
        self.adminPaswLabel = Label(self, text="Admin:", font=("Comic Sans MS", 10), fg="black", bg="white")
        self.adminPaswLabel.place(relx=0.025, rely=0.96, anchor="sw")

        # Botón de registro
        self.registerButton = Button(self, text="Registrarse", **button_style, command=self.register)
        self.registerButton.place(relx=0.55, rely=0.8, anchor="center")

        # Botón para volver al frame principal
        self.back_button = Button(self, text="Atrás", bg="#333333", fg="white",**button_style, command=self.goBack)
        self.back_button.place(relx=0.003, rely=0.003, anchor="nw")

    # Creamos un getter para el atributo que queremos ocultar, en este caso la contraseña de administrador
    @property
    def admin_pasw(self):
        return self.__admin_pasw

    # Esta función se encargará de limpiar todos los campos de entrada cada vez que se inicie el frame
    def clear_entries(self):
        self.userEntry.delete(0, END)
        self.paswEntry.delete(0, END)
        self.pasw2Entry.delete(0, END)
        self.dayEntry.delete(0, END)
        self.monthEntry.delete(0, END)
        self.yearEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.email2Entry.delete(0, END)
        self.adminPaswEntry.delete(0, END)

    # Función que confirma el regreso al frame principal, preguntando antes
    def goBack(self):
        winsound.MessageBeep(2500)
        # Obtén la posición de la ventana principal
        x = self.winfo_rootx() + self.winfo_x()
        y = self.winfo_rooty() + self.winfo_y()

        # Muestra una ventana de confirmación
        confimation = messagebox.askyesno("Volver",
                                          "¿Desea abandonar el proceso de registro?")

        if confimation:  # Si el usuario elige "Sí"
            self.controller.show_frame("FirstFrame", title="App Gestor de Productos")


    # Función que limpia todas las etiquetas de error ( rojas )
    def clear_error_labels(self):
            for widget in self.winfo_children():
                if isinstance(widget, Label) and widget.cget('fg') == 'red':
                    widget.destroy()


    # Función que se encarga de verificar todas las entradas y de ser validas, crear el usuario
    def register(self):
        self.clear_error_labels()  # Limpia etiquetas de error existentes

        # Guardamos todos los valores de las entradas
        username = self.userEntry.get()
        pasw = self.paswEntry.get()
        pasw2 = self.pasw2Entry.get()
        email = self.emailEntry.get()
        email2 = self.email2Entry.get()
        day = self.dayEntry.get()
        month = self.monthEntry.get()
        year = self.yearEntry.get()
        admin = self.adminPaswEntry.get()

        # Establecemos los campos necesarios para crear el usuario vacios por el momento
        username_validate = None
        pasw_validate = None
        birthday_validate = None
        email_validate = None
        admin_validate = None

        # Validación de nombre de usuario

        # Si el usuario se encuentra vacio
        if username == "":
            self.user_empty_label = Label(self, text="Usuario no puede estar vacío", font=("Comic Sans MS", 10),
                                          fg="red")
            self.user_empty_label.place(relx=0.55, rely=0.235, anchor="center")

        #Si el usuario proporcionado se encuentra en la base de datos
        elif db.session.query(User).filter_by(username=username).first():
            self.user_used_label = Label(self, text="Usuario ya existe", font=("Comic Sans MS", 10), fg="red")
            self.user_used_label.place(relx=0.55, rely=0.235, anchor="center")

        # Si el usuario contiene caracteres especiales
        elif not username.isalnum():
            self.user_special_char_label = Label(self, text="No puede contener caracteres especiales",
                                                 font=("Comic Sans MS", 10), fg="red")
            self.user_special_char_label.place(relx=0.55, rely=0.235, anchor="center")

        # Si el usuario solo contiene numeros
        elif username.isdigit():
            self.user_all_num_label = Label(self, text="No puede ser solo números", font=("Comic Sans MS", 10),
                                            fg="red")
            self.user_all_num_label.place(relx=0.55, rely=0.235, anchor="center")

        # Si el usuario no contiene el numero de caracteres permitido
        elif not (5 <= len(username) <= 20):
            self.user_long_label = Label(self, text="Debe contener entre 5 y 20 caracteres", font=("Comic Sans MS", 10),
                                         fg="red")
            self.user_long_label.place(relx=0.55, rely=0.235, anchor="center")

        # En caso de que lo anterior NO se cumpla, estariamos introduciendo un usuario valido
        else:
            username_validate = username # Por lo que guardamos este usuario como valido

        # Validación de contraseña

        # Si contraseña está vacio
        if pasw == "":
            self.pasw_empty_label = Label(self, text="Contraseña no puede estar vacía", font=("Comic Sans MS", 10),
                                          fg="red")
            self.pasw_empty_label.place(relx=0.55, rely=0.335, anchor="center")

        # Si no se encuentra al menos 1 caracter en mayusucula
        elif not any(c.isupper() for c in pasw):
            self.pasw_upper_label = Label(self, text="Debe contener al menos 1 mayúscula", font=("Comic Sans MS", 10),
                                          fg="red")
            self.pasw_upper_label.place(relx=0.55, rely=0.335, anchor="center")

        # Si no se encuentra al menos 1 numero
        elif not any(c.isdigit() for c in pasw):
            self.pasw_number_label = Label(self, text="Debe contener al menos 1 número", font=("Comic Sans MS", 10),
                                           fg="red")
            self.pasw_number_label.place(relx=0.55, rely=0.335, anchor="center")

        # Si no se encuentra al menos un caracter especial
        elif pasw.isalnum() or pasw.isalpha():
            self.pasw_special_char_label = Label(self, text="Debe contener al menos 1 caracter especial",
                                                 font=("Comic Sans MS", 10), fg="red")
            self.pasw_special_char_label.place(relx=0.55, rely=0.335, anchor="center")

        # Si no contiene la cantidad de caracteres validos
        elif not (6 <= len(pasw) <= 16):
            self.pasw_long_label = Label(self, text="Debe contener entre 6 y 16 caracteres", font=("Comic Sans MS", 10),
                                         fg="red")
            self.pasw_long_label.place(relx=0.55, rely=0.335, anchor="center")

        # Si el campo de contraseña con su validación no coincide
        elif pasw != pasw2:
            self.pasw2_error_label = Label(self, text="Las contraseñas no coinciden", font=("Comic Sans MS", 10),
                                           fg="red")
            self.pasw2_error_label.place(relx=0.55, rely=0.435, anchor="center")

        # Si las comprobaciones son validas
        else:
            pasw_validate = pasw # Guardamos la contraseña

        # Validación de fecha de nacimiento

        # Si alguno de los campos está vacio
        if day == "" or month == "" or year == "":
            self.birthday_empty_label = Label(self, text="No puede haber campos vacíos", font=("Comic Sans MS", 10),
                                              fg="red")
            self.birthday_empty_label.place(relx=0.55, rely=0.535, anchor="center")

        # En caso de que todos los campos estén completos
        else:
            try:
                # Intentamos convertir todos los valores a enteros
                day, month, year = int(day), int(month), int(year)

                max_days = 31  # Establecemos el maximo de dias permitido
                if month in [4, 6, 9, 11]:
                    # Guardamos el maximo de dias en caso de ser estos meses
                    max_days = 30
                elif month == 2:  # en el caso de febrero, verificamos si fue bisiesto o no
                    max_days = 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28

                # Comprobamos que no se haya introducido ningun dato negativo, ni supere el maximo permitido en ningun caso
                if day < 1 or day > max_days:
                    self.birthday_error_label = Label(self, text="Día inválido", font=("Comic Sans MS", 10), fg="red")
                    self.birthday_error_label.place(relx=0.55, rely=0.535, anchor="center")
                elif month < 1 or month > 12:
                    self.birthday_error_label = Label(self, text="Mes inválido", font=("Comic Sans MS", 10), fg="red")
                    self.birthday_error_label.place(relx=0.55, rely=0.535, anchor="center")
                elif year < 1900 or year > 2023:
                    self.birthday_error_label = Label(self, text="Año inválido", font=("Comic Sans MS", 10), fg="red")
                    self.birthday_error_label.place(relx=0.55, rely=0.535, anchor="center")

                # Si las comprobaciones pasan validas, guardamos la fecha
                else:
                    birthday_validate = f"{day:02d}/{month:02d}/{year}"  # En el formato que nos interesa
                    print("birthday valido")

            except ValueError:
                # Si la conversión de dia/mes/año no es posible, lanzará value error, la capturamos para mostrar el error
                self.birthday_error_label = Label(self, text="Formato de fecha inválido", font=("Comic Sans MS", 10),
                                                  fg="red")
                self.birthday_error_label.place(relx=0.55, rely=0.535, anchor="center")



        # Validación de e-mail

        # Si el campo de email o email2 están vacios...
        if email == "":
            self.email_empty_label = Label(self, text="E-Mail no puede estar vacío", font=("Comic Sans MS", 10),
                                           fg="red")
            self.email_empty_label.place(relx=0.55, rely=0.635, anchor="center")
        elif email2 == "":
            self.email2_empty_label = Label(self, text="Confirmar E-Mail no puede estar vacío",
                                            font=("Comic Sans MS", 10), fg="red")
            self.email2_empty_label.place(relx=0.55, rely=0.735, anchor="center")

        # Si los dos campos no coinciden
        elif email != email2:
            self.email2_error_label = Label(self, text="El e-mail no coincide", font=("Comic Sans MS", 10), fg="red")
            self.email2_error_label.place(relx=0.55, rely=0.735, anchor="center")

        # Si el email ya se encuentra en la base de datos
        elif db.session.query(User).filter_by(email=email).first():
            self.email_used_label = Label(self, text="E-Mail en uso", font=("Comic Sans MS", 10), fg="red")
            self.email_used_label.place(relx=0.55, rely=0.635, anchor="center")

        # Si pasa estas validaciones entonces comprobamos el formato del email
        else:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' # Guardamos el formato

            # Si no se cumple con este formato
            if not re.match(email_pattern, email):
                self.email_invalid_label = Label(self, text="Formato de E-Mail incorrecto", font=("Comic Sans MS", 10),
                                                 fg="red")
                self.email_invalid_label.place(relx=0.55, rely=0.635, anchor="center")

            # De ser correcto
            else:
                email_validate = email # Guardamos tambien el email
                print("email valido")

        # Validación de contraseña de administrador

        # Si la contraseña introducida coincide con la guardada
        if admin == self.admin_pasw:
            admin_validate = True # Validamos este campo

        # Si se ha introducido una contraseña, pero esta no es valida
        elif admin != self.admin_pasw and len(admin) > 0:
            self.admin_pasw_error_label = Label(self, text="Error",
                                                font=("Comic Sans MS", 10), fg="red")
            self.admin_pasw_error_label.place(relx=0.055, rely=0.91, anchor="center")


        # Con todos los campos validados, procedemos al Registro del usuario

        # Si todos los campos, incluido el de admin pasw, son validos, entonces creamos un usuario con privilegios
        if username_validate and pasw_validate and birthday_validate and email_validate and admin_validate:
            new_user = User(username=username_validate, pasw=pasw_validate, email=email_validate,
                            birthday=birthday_validate, admin=True)
            db.session.add(new_user) # Añadimos el nuevo usuario a la sesion
            db.session.commit() # Guardamos cambios
            db.session.close() # Cerramos sesion
            self.clear_entries() # Limpiamos todas las entradas
            # Y mostramos un mensaje que indique que se ha creado un ADMINISTRADOR , y el nombre del mismo
            messagebox.showinfo("Registro Exitoso", f"Registro exitoso para el administrador {username_validate}.")
            # Redirigimos al frame principal una vez acabado el registro
            self.controller.show_frame("FirstFrame", title="App Gestor de Productos")

        # En caso de no contar con la casilla de admin validada, crearemos un usuario raso
        elif username_validate and pasw_validate and birthday_validate and email_validate:
            new_user = User(username=username_validate, pasw=pasw_validate, email=email_validate,
                            birthday=birthday_validate)
            db.session.add(new_user) # Mismo proceso, añadir a la sesion el usuario
            db.session.commit() # Guardar cambios
            db.session.close() # Cerrar sesion
            self.clear_entries() # Limpiar entradas
            # En este caso mostraremos el mensaje pero con un USUARIO
            messagebox.showinfo("Registro Exitoso", f"Registro exitoso para el usuario {username_validate}.")
            # De igual forma redirigimos al frame principal
            self.controller.show_frame("FirstFrame", title="App Gestor de Productos")







