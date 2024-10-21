#app.py
import db
import winsound
from PIL import Image, ImageTk
from tkinter import Tk, Label, messagebox

#Importamos todos los frames para poder cambiar entre ellos

from windows.FirstFrame import FirstFrame
from windows.AccesFrame import AccesFrame
from windows.RegisterFrame import RegisterFrame
from windows.UserFrame import UserFrame
from windows.AdminFrame import AdminFrame
from models import User

#Creamos la ventana principal, la que alojará todos los frames
class FirstWindow():
    def __init__(self, root):
        self.window = root #Guardamos la ventana principal en root para poder referirnos a ella
        self.window.title("App Gestor De Productos") #Le damos un titulo a la ventana
        self.window.resizable(0, 0) #Evitamos que se pueda redimensionar
        self.window.wm_iconbitmap("resources/logo.ico") #Incrustamos el logo de la app
        self.user = None #Inicializamos el usuario, que mas adelante servirá


        # Sacamos tanto el ancho como el alto de la pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculamos X e Y para que la ventana quede centrada
        x = (screen_width - 600) // 2
        y = (screen_height - 800) // 2

        # Establecemos las dimensiones de la pantalla en la posicion calculada
        self.window.geometry(f"600x800+{x}+{y}")


        self.image = Image.open("resources/background.jpeg") #Cargamos la imagen de fondo
        self.image = self.image.resize((600, 800), Image.LANCZOS) #La redimensionamos
        self.image_tk = ImageTk.PhotoImage(self.image) #La damos un formato que tkinter entienda

        #Creamos una etiqueta para lojar la imagen de fondo y la colocamos
        self.image_label = Label(self.window, image=self.image_tk)
        self.image_label.grid(row=0, column=0, sticky='nsew')

        # Configuramos la fila y columna para que se ajusten al tamaño de la ventana
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Creamos un diccionario para alojar los frames
        self.frames = {}

        # Introducimos los frames en el diccionario
        for F in (FirstFrame, AccesFrame, RegisterFrame):
            page_name = F.__name__  #Obtenemos el nombre del frame
            frame = F(parent=self.window, controller=self) #Creamos los frames configurando su parent y controller
            self.frames[page_name] = frame #Añadimos los frames al diccionarop
            frame.grid(row=0, column=0, sticky="nsew")  # Añadimos los frames a la cuadricula


        # Añadimos los frames de usuario y administrador, pero configurando además el usuario, que lo inicializamos vacio
        user_frame = UserFrame(parent=self.window, controller=self, user=None)
        self.frames["UserFrame"] = user_frame
        user_frame.grid(row=0, column=0, sticky="nsew")

        admin_frame = AdminFrame(parent=self.window,controller=self,user=None)
        self.frames["AdminFrame"] = admin_frame
        admin_frame.grid(row=0, column=0, sticky="nsew")

        # Llamamos al metodo para mostrar el frame que necesitamos, en este caso, llamamos al frame "Principal"
        self.show_frame("FirstFrame",title="App Gestor de Productos")

    # Creamos una funcion que se encargue de enviar a la ventana principal, el frame necesario en cada caso
    def show_frame(self, page_name,user=None,title=None):
        frame = self.frames[page_name] #Según el frame que necesitemos, es el que buscará en su diccionario
        frame.tkraise() #Nos aseguramos que el frame se vea por encima del resto

        # Si le damos un titulo al llamar a la función
        if title:
            self.window.title(title)  # Cambia el título de la ventana principal

        if page_name == "AccesFrame": # En caso de que sea AccesFrame...
            frame.clear_error_labels() # Limpiará las etiquetas de error
            frame.userEntry.focus() # Establecerá el foco en la entrada de usuario
            frame.clear_entries() # Limpiará las entradas
            frame.pasw_attempts=0 # Establecerá el numero de intentos de contraseña a 0

        elif page_name == "RegisterFrame": # Si se trata de la pagina de resistro...
            frame.userEntry.focus() # Establece el foco en el nombre de usuario
            frame.clear_entries() # Limpiará de igual forma todas las entradas
            frame.clear_error_labels() # Y limpiará tambien las etiquetas de error

        # En caso de acceder a un usuario, y adeás tener un usuario como argumento...
        elif page_name == "UserFrame" and user:
            frame.user = user # El usuario del frame, es el dado como argumento
            frame.show_products() # Mostramos los productos
            frame.update_cart_quantity() # Actualizaremos la cantidad de objetos en el carrito del usuario

        #En caso de acceder como administrador, y obtener un usuario en el argumento..
        elif page_name == "AdminFrame" and user:
            frame.user = user # El usuario será este mismo


    # creamos una función que nos de una confirmación al cerrar la aplicación
    def close_app(self):
        winsound.MessageBeep(2500) # Advertmos con un sonido

        # Mostramos una ventana de confirmación
        confimation = messagebox.askyesno("Cerrar",
                                          f"¿Estás seguro de querer cerrar el programa?")
        # Si el usuario presiona en Si:
        if confimation:
            root.destroy() # La ventana principal se destruye y cierra el programa


if __name__ == "__main__":
    root = Tk() #Creamos la ventana principal
    root.geometry("0x0") # La geometria la mantenemos "invisible" para no visualizarla hasta que se inicie el primer frame

    # Obtenemos el alto y ancho de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    #Y posicionamos la ventana en las coordenadas maximas para no visualizarla (Ya que no contiene ningun frame aún)
    root.geometry(f"+{screen_width}+{screen_height}")

    #Creamos una instancia de primera ventana, pasandole la ventana principal como argumento
    app = FirstWindow(root)

    #Asociamos el evento de cerrar la ventana con la función de close_app
    root.protocol("WM_DELETE_WINDOW", app.close_app)



    # Y por último iniciamos el bucle que mantiene la app en ejecución
    root.mainloop()