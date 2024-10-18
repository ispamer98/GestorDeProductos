#UserFrame.py
import time

import winsound
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import Frame, Label, Button, Scrollbar
from PIL import Image, ImageTk
import db
from models import User, Product, Cart
import json
from sqlalchemy.orm.attributes import flag_modified
import ctypes


# Creamos el Frame del panel de usuario
class UserFrame(Frame):
    def __init__(self, parent, controller, user): # Pasamos como argumento el usuario, para poder actuar sobre el
        Frame.__init__(self, parent) # Iniciamos el constructor de la clase que hereda
        self.controller = controller # Guardamos el controlador
        self.user = user # Y guardamos el usuario

        # Cargamos y configuramos la imagen de fondo
        self.image = Image.open("resources/backgroundUser.jpeg")
        self.image = self.image.resize((600, 800), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(self, image=self.image_tk)
        self.image_label.grid(row=0, column=0, sticky='nsew')

        # Configuramos la fila y columna para que se ajusten al tamaño de la ventana
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Establecemos dos estilos para los botones por defecto
        self.button_style = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat"}
        self.button_style2 = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat", "background": "#d3d3d3"}

        # Creamos un botón para volver al frame principal.
        self.back_button = Button(self, text="Cerrar Sesión", bg="#333333", fg="white", **self.button_style, command=self.close_session)
        self.back_button.place(relx=1, rely=1, anchor="se")

        # Creamos el Frame que contendrá el Treeview
        self.table = Frame(self, bg="white")
        self.table.place(relx=0.5, rely=0.4, anchor="center", width=500, height=400)

        # Crear un estilo personalizado
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configuramos el Treeview
        self.style.configure("Custom.Treeview",  # Estilo personalizado para el Treeview
                             background="#d3d3d3",  # Color de fondo de las filas del Treeview
                             foreground="black",  # Color del texto en las filas del Treeview
                             rowheight=25,  # Altura de las filas en el Treeview
                             fieldbackground="white",  # Color de fondo de las celdas en el Treeview
                             font=('Comic Sans MS', 12))  # Fuente y tamaño del texto en el Treeview

        # Configuramos el estilo para los encabezados del Treeview
        self.style.configure("Custom.Treeview.Heading",
                             background="#2e2e2e",  # Color de fondo de los encabezados del Treeview
                             foreground="white",  # Color del texto en los encabezados del Treeview
                             font=('Comic Sans MS', 14, 'bold'))  # Fuente, tamaño y estilo del texto en los encabezados

        # Configuramos el comportamiento de los encabezados del Treeview cuando están activos
        self.style.map("Custom.Treeview.Heading",
                       background=[("active", "#2e2e2e")],  # Color de fondo cuando el encabezado está activo
                       foreground=[("active", "white")])  # Color del texto cuando el encabezado está activo

        # Configuramos el comportamiento general del Treeview para filas seleccionadas
        self.style.map("Custom.Treeview",
                       background=[("selected", "#4f4f4f")],  # Color de fondo de las filas seleccionadas
                       foreground=[("selected", "black")])  # Color del texto en las filas seleccionadas


        # Creamo el Treeview para mostrar los productos
        self.products_tree = ttk.Treeview(self.table, columns=("name", "price"),
                                          show="headings", height=15, style="Custom.Treeview")
        self.products_tree.heading("name", text="Producto") # Creamos la columna de producto
        self.products_tree.heading("price", text="Precio (€)") # Y la columna de precio
        self.products_tree.column("name", anchor="center", width=300) # Le damos su espacio
        self.products_tree.column("price", anchor="center", width=150)

        # Agregar barra de desplazamiento vertical
        vertical_scrollbar = ttk.Scrollbar(self.table, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=vertical_scrollbar.set)

        # Añadimos el treeview y la scrollbar
        self.products_tree.pack(side='left', fill=BOTH, expand=True, padx=10, pady=10)
        vertical_scrollbar.pack(side='right', fill='y')

        # Creamos el botón para añadir al carrito
        self.cart_button = Button(self, text="Añadir al Carrito", compound="bottom", **self.button_style,
                                  command=self.add_to_cart)
        self.cart_button.place(relx=0.5, rely=0.7, anchor="center")

        # Ruta al archivo .ico
        self.cart_image = "resources/cart2.ico"

        # Cargamos la imagen y la preparamos para su uso
        original_image = Image.open(self.cart_image)
        resized_image = original_image.resize((20, 20), Image.LANCZOS)
        self.cart_symbol = ImageTk.PhotoImage(resized_image)

        # Botón para mostrar el carrito
        self.show_cart_button = Button(self, image=self.cart_symbol, compound="bottom", command=self.show_cart,
                                       **self.button_style)
        self.show_cart_button.place(relx=0.9, rely=0.7, anchor="center")

        # Si la etiqueta que muestra la cantidad de objetos añadidos al carrito no existe, la crea a 0
        if not hasattr(self, 'cart_quantity_label'):
            self.cart_quantity_label = Label(self, text="0", font=('Comic Sans MS', 9, 'bold'), bg="white")
            self.cart_quantity_label.place(relx=0.92, rely=0.67, anchor="center")

        # Actualiza la cantidad de objetos en el carrito
        self.update_cart_quantity()

        # Muestra los productos en el treeview
        self.show_products()

    #Creamos una función que se encargue de actualizar la etiqueta del total de productos en el carrito
    def update_cart_quantity(self):
        # Verificar si encuentra el usuario
        if self.user is None:
            return  # No hacer nada si no hay usuario

        # Consultamos el carrito del usuario
        self.cart = db.session.query(Cart).filter_by(username=self.user.username).first()

        # Si encontramos el carrito en la base de datos
        if self.cart:
            # Capturamos todos los productos de la base de datos
            products_in_db = db.session.query(Product.name).all()

            # Creamos una lista vacía para almacenar los nombres de los productos
            products_in_db_names = []

            # Recorremos la lista de productos
            for product_name in products_in_db:
                # Extraemos el nombre del producto y lo añadimos a la lista
                products_in_db_names.append(product_name[0])

            # Filtramos los productos del carrito para eliminar los que no están en la base de datos
            filtered_products = [] # Iniciamos la lista de productos que coinciden tanto en carrito como en db
            for product in self.cart.products:
                # Si el producto se encuentra en la lista que hemos sacado de la base de datos y su cantidad es mayor que 0
                if product["name"] in products_in_db_names and product["quantity"] > 0:
                    # Añadimos el producto a la lista
                    filtered_products.append(product)

            # Si hubo cambios en los productos del carrito, actualizarlos en la base de datos
            if len(filtered_products) != len(self.cart.products):
                self.cart.products = filtered_products
                db.session.commit()

            # Creamos una variable para almacenar la cantidad total de productos
            total_quantity = 0

            # Recorremos cada producto en el carrito
            for item in self.cart.products:
                # Obtenemos la cantidad del producto, si no existe la clave "quantity", usamos 0
                quantity = item.get("quantity", 0)

                # Sumamos la cantidad al total
                total_quantity += quantity
        else:
            total_quantity = 0

        # Verificar si la etiqueta existe antes de configurarlo
        if self.cart_quantity_label is None or not self.cart_quantity_label.winfo_exists():
            # Crear la etiqueta si no existe
            self.cart_quantity_label = Label(self, text="0", font=('Comic Sans MS', 9, 'bold'), fg='green')
            self.cart_quantity_label.place(relx=0.92, rely=0.67, anchor="center")

        # Actualizamos la etiqueta con la cantidad total de productos
        self.cart_quantity_label.config(text=str(total_quantity), font=('Comic Sans MS', 9, 'bold'), fg='green')

    # Función que se encargará de añadir productos al carrito del usuario
    def add_to_cart(self):
        # Obtenemos el carrito del usuario desde la base de datos
        self.cart = db.session.query(Cart).filter_by(username=self.user.username).first()

        # Si el carrito no existe, lo creamos
        if not self.cart:
            self.cart = Cart(username=self.user.username)
            db.session.add(self.cart)
            db.session.commit()

        # Obtenemos la selección del Treeview
        selection = self.products_tree.selection()

        # Si no se ha seleccionado un producto
        if not selection:
            ctypes.windll.user32.MessageBeep(0x00000010)  # Sonido de exclamación
            # Creamos una etiqueta de error
            self.not_product_select_label = Label(self, text="", font=('Comic Sans MS', 12), fg='red')
            self.not_product_select_label.place(relx=0.5, rely=0.85, anchor="center")  # Ajusta la posición
            self.not_product_select_label.config(text="Debes seleccionar un producto")
            return

        # Eliminamos el mensaje de error si ya existía
        if hasattr(self, 'not_product_select_label') and self.not_product_select_label.winfo_exists():
            self.not_product_select_label.destroy()

        # Obtenemos los datos del producto seleccionado
        product = selection[0]
        product_data = self.products_tree.item(product, "values") # Guardamos los valores
        product_name = product_data[0] # Guardamos el nombre
        product_price = float(product_data[1].rstrip("€")) #Y el precio sin el simbolo

        # Creamos una variable para saber si es una actualización del producto en el carrito
        product_updated = False

        # Actualiza la cantidad si el producto ya está en el carrito
        for item in self.cart.products: # Itera sobre los productos en el carrito
            if item["name"] == product_name: # Si el objeto encontrado es igual al seleccionado
                item["quantity"] += 1 # Actualizará la cantidad
                product_updated = True #Actualizará la variable para saber que ya se encuentra
                ctypes.windll.user32.MessageBeep(0x00000010) # Manda un sonido
                self.show_add_message(f"{product_name} añadido al carrito") #Y crea una etiqueta para avisar
                break

        # Si el producto no estaba en el carrito lo agregamos
        if not product_updated:
            new_product = {"name": product_name, "price": product_price, "quantity": 1} # Creamos el producto en forma de diccionario
            ctypes.windll.user32.MessageBeep(0x00000010) #Añadimos un sonido al agregarlo
            self.cart.products.append(new_product) #Añadimos el producto al carrito
            self.show_add_message(f"{product_name} añadido al carrito") # Mostramos el mensaje de aañadido

        # Marca la columna products como modificada
        flag_modified(self.cart, "products")

        # Inicializamos la variable para almacenar el precio total
        total_price = 0

        # Recorremos cada producto en el carrito
        for product in self.cart.products:
            # Calculamos el precio de cada producto
            price = product["price"] * product["quantity"]

            # Sumamos el precio al total
            total_price += price
        self.cart.total_price = round(total_price, 2) #Redondemos a dos decimales el precio

        # Actualiza la cantidad en el carrito
        self.update_cart_quantity()

        # Guarda el carrito actualizado en la base de datos
        db.session.commit()



    def show_add_message(self, message):
        # Elimina la etiqueta anterior si existe
        if hasattr(self, 'add_to_cart_label') and self.add_to_cart_label.winfo_exists():
            self.add_to_cart_label.destroy()

        # Crea una nueva etiqueta y muestra el mensaje
        self.add_to_cart_label = Label(self, text="", font=('Comic Sans MS', 12), fg='green')
        self.add_to_cart_label.place(relx=0.5, rely=0.85, anchor="center")  # Ajusta la posición
        self.add_to_cart_label.config(text=message)

        # Si hay una tarea programada previa, cancélala
        if hasattr(self, 'remove_message_id'):
            self.after_cancel(self.remove_message_id)

        # Programa la eliminación de la etiqueta después de 3 segundos (3000 milisegundos)
        self.remove_message_id = self.after(3000, self.remove_message)

    #Función que se encargará de eliminar el mensaje de añadido
    def remove_message(self):
        # Verifica si la etiqueta existe antes de intentar destruirla
        if hasattr(self, 'add_to_cart_label') and self.add_to_cart_label.winfo_exists():
            self.add_to_cart_label.destroy()

    # Función que se encargará de mostrar el carrito
    def show_cart(self):
        # Crear la ventana del carrito
        self.cart_window = Toplevel(self)
        self.cart_window.resizable(0,0)
        self.cart_window.title(f"Carrito de {self.user.username}")
        self.cart_table = Frame(self.cart_window, bg="white")
        self.cart_window.geometry("350x400")
        self.cart_window.grab_set()
        self.cart_table.place(relx=0.5, rely=0.35, anchor="center", width=320, height=250)

        # Obtener el carrito de la base de datos
        self.cart = db.session.query(Cart).filter_by(username=self.user.username).first()
        # Calcular la posición centrada
        screen_width = self.cart_window.winfo_screenwidth()
        screen_height = self.cart_window.winfo_screenheight()
        x = (screen_width - 320) // 2
        y = (screen_height - 400) // 2
        self.cart_window.geometry(f"{320}x{400}+{x}+{y}")

        # Crear el Treeview
        self.cart_tree = ttk.Treeview(self.cart_table, columns=("name", "quantity"), show="headings", height=15,
                                      style="Custom.Treeview")
        self.cart_tree.heading("name", text="Producto")
        self.cart_tree.heading("quantity", text="Cantidad")
        self.cart_tree.column("name", anchor="center", width=200)
        self.cart_tree.column("quantity", anchor="center", width=100)
        self.cart_tree.pack(side=tk.LEFT, fill=BOTH, expand=True)

        # Crear y configurar la Scrollbar
        vertical_scrollbar = ttk.Scrollbar(self.cart_table, orient="vertical", command=self.cart_tree.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_tree.configure(yscrollcommand=vertical_scrollbar.set)

        # Limpiar el Treeview antes de llenarlo de nuevo
        self.cart_tree.delete(*self.cart_tree.get_children())

        # Filtrar productos con cantidad > 0 y eliminarlos de la lista si es necesario
        filtered_products = []
        total_price = 0

        products_in_db=db.session.query(Product.name).all()
        products_in_db_names=[]
        for product_name in products_in_db:
            products_in_db_names.append(product_name[0])

        for product in self.cart.products:
            if product["quantity"] > 0 and product["name"] in products_in_db_names:
                filtered_products.append(product)
                self.cart_tree.insert("", "end", values=(product["name"], product["quantity"]))
                total_price += product["price"] * product["quantity"]

        # Actualizar el total_price en la base de datos y eliminar productos con cantidad <= 0
        if len(filtered_products) != len(self.cart.products):
            self.cart.products = filtered_products
            self.cart.total_price = total_price
            flag_modified(self.cart, "products")
            db.session.commit()

        # Eliminar la etiqueta total_price si existe
        if hasattr(self, 'total_price_label'):
            self.total_price_label.destroy()

        # Mostrar el total_price en la interfaz de usuario
        self.total_price_label = Label(self.cart_window, text=f"Total: {total_price:.2f}€", font=("Comic Sans MS", 12),
                                       bg="white")
        self.total_price_label.place(relx=0.5, rely=0.70, anchor="center")

        # Crear el botón de eliminar producto
        self.delete_product_button = Button(self.cart_window, text="Eliminar", compound="bottom",
                                            command=self.delete_product,
                                            **self.button_style2, bg="red", fg="white")
        self.delete_product_button.place(relx=0.30, rely=0.85, anchor="center")

        # Crear el botón de modificar producto
        self.modify_product_button = Button(self.cart_window, text="Modificar", compound="bottom",
                                            command=self.modify_product,
                                            **self.button_style2)
        self.modify_product_button.place(relx=0.70, rely=0.85, anchor="center")

        # Configurar el ícono de la ventana y mostrar la ventana
        self.cart_window.wm_iconbitmap("resources/cart2.ico")
        self.cart_window.transient(self.controller.window)
        self.cart_window.wait_window(self.cart_window)

    def delete_product(self):
        # Seleccionar el producto actual
        product_select = self.cart_tree.selection()
        if not product_select:
            error_label = Label(self.cart_window, text="Debes seleccionar un producto.", fg="red",
                                font=("Comic Sans MS", 12))
            error_label.place(relx=0.5, rely=0.95, anchor="center")
            return

        item = self.cart_tree.item(product_select)
        product_name = item["values"][0]

        # Confirmar eliminación del producto
        winsound.MessageBeep()
        confirm = messagebox.askyesno("Eliminar Producto",
                                      f"¿Estás seguro de que deseas eliminar el producto \"{product_name}\" del carrito?")

        if confirm:
            # Consultar nuevamente el carrito desde la base de datos
            self.cart = db.session.query(Cart).filter_by(username=self.user.username).first()

            # Encontrar y eliminar el producto seleccionado
            self.cart.products = [product for product in self.cart.products if product["name"] != product_name]

            # Recalcular el total_price
            self.cart.total_price = sum(p["price"] * p["quantity"] for p in self.cart.products)

            # Marcar la columna como modificada para que SQLAlchemy registre los cambios
            flag_modified(self.cart, "products")

            # Guardar los cambios en la base de datos
            db.session.add(self.cart)
            db.session.commit()

            # Actualizar la vista del carrito
            self.update_cart_view()
    def modify_product(self):
        # Seleccionar el producto actual
        product_select = self.cart_tree.selection()
        if not product_select:
            error_label = Label(self.cart_window, text="Debes seleccionar un producto.", fg="red",
                                font=("Comic Sans MS", 12))
            error_label.place(relx=0.5, rely=0.95, anchor="center")
            return
        else:
            item = self.cart_tree.item(product_select)
            product_select_name = item["values"][0]
            product_select_quantity = int(item["values"][1])  # Convertir a entero para manipular

        # Crear la ventana de modificación
        self.modify_window = Toplevel(self.cart_window)
        self.modify_window.title("Modificar Producto")

        # Configuración de la ventana para que sea modal
        self.modify_window.grab_set()  # Hace que la ventana sea modal
        self.modify_window.focus_set()  # Asegura que la ventana tenga el foco

        # Configurar el tamaño de la ventana de modificación
        self.modify_window.geometry("300x200")

        # Calcular la posición centrada de la ventana de modificación
        screen_width = self.modify_window.winfo_screenwidth()
        screen_height = self.modify_window.winfo_screenheight()
        window_width = 300
        window_height = 200
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.modify_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Etiqueta para mostrar el producto seleccionado
        product_label = Label(self.modify_window, text=f"Producto: {product_select_name}", font=("Comic Sans MS", 12))
        product_label.pack(pady=10)

        # Frame para la cantidad y botones de incremento/decremento
        quantity_frame = Frame(self.modify_window)
        quantity_frame.pack(pady=10)

        # Botón de decremento
        decrement_button = Button(quantity_frame, text="-", font=("Arial", 16), bg="red", fg="white", width=2, height=1,
                                  command=lambda: self.change_quantity(-1))
        decrement_button.pack(side=tk.LEFT, padx=10)

        # Etiqueta de cantidad
        self.quantity_var = tk.IntVar(value=product_select_quantity)
        quantity_label = Label(quantity_frame, textvariable=self.quantity_var, font=("Comic Sans MS", 14))
        quantity_label.pack(side=tk.LEFT, padx=10)

        # Botón de incremento
        increment_button = Button(quantity_frame, text="+", font=("Arial", 16), bg="green", fg="white", width=2,
                                  height=1,
                                  command=lambda: self.change_quantity(1))
        increment_button.pack(side=tk.LEFT, padx=10)

        # Botón de confirmación
        confirm_button = Button(self.modify_window, text="Confirmar", **self.button_style2,
                                command=lambda: self.confirm_modification(product_select, product_select_name))
        confirm_button.pack(pady=10)

        self.update_cart_quantity()

        # Al cerrar la ventana de modificación, restaurar el grab_set en self.cart_window
        self.modify_window.protocol("WM_DELETE_WINDOW", lambda: (
            self.modify_window.grab_release(),  # Libera el grab actual
            self.cart_window.grab_set(),  # Restablece el grab en cart_window
            self.modify_window.destroy()  # Destruye la ventana de modificación
        ))


    def change_quantity(self, quantity):
        # Cambiar la cantidad de acuerdo a lo que se añade
        new_quantity = self.quantity_var.get() + quantity
        if new_quantity < 0:
            new_quantity = 0  # Evitamos la cantidad negativa
        self.quantity_var.set(new_quantity)

        self.update_cart_quantity()

    def confirm_modification(self, product_select, product_name):
        # Obtener la nueva cantidad
        new_quantity = self.quantity_var.get()

        # Consultar nuevamente el carrito desde la base de datos
        self.cart = db.session.query(Cart).filter_by(username=self.user.username).first()

        # Encontrar y actualizar el producto seleccionado
        for product in self.cart.products:
            if product["name"] == product_name:
                if new_quantity <= 0:
                    self.cart.products.remove(product)  # Eliminar producto si la cantidad es 0 o menor
                else:
                    product["quantity"] = new_quantity
                break

        # Recalculamos el precio total
        self.cart.total_price = sum(p["price"] * p["quantity"] for p in self.cart.products)

        # Marcar la columna como modificada
        flag_modified(self.cart, "products")

        # Guardar los cambios en la base de datos
        db.session.add(self.cart)
        db.session.commit()

        # Actualizar la vista del carrito
        self.update_cart_view()


        self.modify_window.destroy()  # Destruye la ventana de modificación
        self.modify_window.grab_release(),  # Libera el grab actual
        self.cart_window.grab_set(),  # Restablece el grab en cart_window
        self.update_cart_quantity() # Actualiza la cantidad de items en el carrito

    def update_cart_view(self):
        # Volver a consultar el carrito actualizado
        self.cart = db.session.query(Cart).filter_by(username=self.user.username).first()

        # Limpiar el Treeview
        self.cart_tree.delete(*self.cart_tree.get_children())


        # Insertar los productos actualizados en el Treeview
        total_price = 0 # Establecemos el precio total del carrito en 0
        for product in self.cart.products: # Recorremos los productos en el carrito
            if product["quantity"] > 0: # Si la cantidad del producto es mayor que 0
                # Introducimos en el Treeview  los calores nombre y cantidad
                self.cart_tree.insert("", "end", values=(product["name"], product["quantity"]))
                total_price += product["price"] * product["quantity"] # Y Actualizamos el precio total segun la cantidad de items de cada producto

        # Si la etiqueta del precio total ya existe, la eliminamos
        if hasattr(self, 'total_price_label'):
            self.total_price_label.destroy()  # Eliminar la etiqueta existente si existe

        # Y la modificamos por el precio total actualizado
        self.total_price_label = Label(self.cart_window, text=f"Total: {total_price:.2f}€", font=("Comic Sans MS", 12),
                                       bg="white")
        self.total_price_label.place(relx=0.5, rely=0.70, anchor="center")
        self.update_cart_quantity() # Y actualizamos la cantidad de items en el carrito


    # Mostramos los productos disponibles en el Treeview
    def show_products(self):
        # Buscamos en la base de datos
        all_products = db.session.query(Product).all()

        # Eliminamos el Treeview anterior
        for row in self.products_tree.get_children():
            self.products_tree.delete(row)

        # Establecemos un maximo de 18 lineas para el Treeview
        self.products_tree.config(height=min(len(all_products),18))

        # E insertamos uno a uno los nombres y precios de cada producto
        for product in all_products:
            self.products_tree.insert("", "end", values=(product.name,f"{product.price}€"))


    # Creamos la funcion que cierra la sesion
    def close_session(self):
        winsound.MessageBeep(2500) # Enviamos un sonido de alerta

        # Mostramos una ventana de confirmación
        confimation =  messagebox.askyesno("Cerrar Sesión",
                                     f"¿Estás seguro de querer cerrar el usuario "
                                             f"\n                         \"{self.user.username}\"   ?")

        if confimation:  # Si el usuario elige "Sí"
            self.controller.show_frame("FirstFrame",title="App Gestor de Productos")
