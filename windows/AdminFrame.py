# AdminFrame.py
import winsound
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import Frame, Label, Button, Scrollbar
from PIL import Image, ImageTk
import db
from models import User, Product, Cart
from datetime import datetime
import re
class AdminFrame(Frame):
    def __init__(self, parent, controller, user):
        Frame.__init__(self, parent)
        self.controller = controller
        self.user = user

        self.image = Image.open("resources/backgroundUser.jpeg")
        self.image = self.image.resize((600, 800), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(self, image=self.image_tk)
        self.image_label.grid(row=0, column=0, sticky='nsew')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.button_style = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat"}

        self.welcome_message = Label(self, text="Bienvenido al panel de Administración\n\n¿Qué deseas administrar?",
                                     background="#0a0a0a", fg="white", font=("Comic Sans MS", 16, 'bold'))
        self.welcome_message.place(relx=0.5, rely=0.1, anchor="center")

        # Botón para volver al frame principal
        self.back_button = Button(self, text="Cerrar Sesión", bg="#333333", fg="white", **self.button_style, command=self.close_session)
        self.back_button.place(relx=1, rely=1, anchor="se")

        # Botón para administrar productos
        self.manage_products_button = Button(self, text="Administrar Productos", compound="bottom", **self.button_style, command=self.show_manage_products)
        self.manage_products_button.place(relx=0.5, rely=0.4, anchor="center")

        # Botón para administrar usuarios
        self.manage_users_button = Button(self, text="Administrar Usuarios", compound="bottom", **self.button_style, command=self.show_manage_users)
        self.manage_users_button.place(relx=0.5, rely=0.6, anchor="center")

        # Crea un botón para volver al frame principal.
        self.back_button = Button(self, text="Cerrar Sesión", bg="#333333", fg="white", **self.button_style, command=self.close_session)
        self.back_button.place(relx=1, rely=1, anchor="se")


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def show_manage_products(self):
        # Limpiar el contenido actual del frame
        admin_frame_widets = [self.welcome_message, self.manage_products_button, self.manage_users_button]
        self.admin_frame_widets_info = []
        for widget in admin_frame_widets:
            info = widget.place_info()
            self.admin_frame_widets_info.append(info)
            widget.place_forget()

        # Crear el Frame que contendrá el Treeview
        self.table = Frame(self, bg="white")
        self.table.place(relx=0.5, rely=0.4, anchor="center", width=500, height=400)

        # Crear un estilo personalizado
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Custom.Treeview",
                            background="#d3d3d3",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="white",
                            font=('Comic Sans MS', 12))

        self.style.configure("Custom.Treeview.Heading",
                            background="#2e2e2e",
                            foreground="white",
                            font=('Comic Sans MS', 14, 'bold'))

        self.style.map("Custom.Treeview.Heading",
                       background=[("active", "#2e2e2e")],  # Keep the same background on hover
                       foreground=[("active", "white")])

        self.style.map("Custom.Treeview",
                       background=[("selected", "#4f4f4f")],
                       foreground=[("selected", "black")])

        # Crear el Treeview para mostrar los productos
        self.products_tree = ttk.Treeview(self.table, columns=("name", "price"),
                                          show="headings", height=15, style="Custom.Treeview")
        self.products_tree.heading("name", text="Producto")
        self.products_tree.heading("price", text="Precio (€)")
        self.products_tree.column("name", anchor="center", width=300)
        self.products_tree.column("price", anchor="center", width=150)

        # Agregar barra de desplazamiento vertical
        vsb = ttk.Scrollbar(self.table, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=vsb.set)

        # Empaquetar el Treeview y la barra de desplazamiento
        self.products_tree.pack(side='left', fill=BOTH, expand=True, padx=10, pady=10)
        vsb.pack(side='right', fill='y')

        all_products = db.session.query(Product).all()

        for row in self.products_tree.get_children():
            self.products_tree.delete(row)

        self.products_tree.config(height=min(len(all_products),18))


        for product in all_products:
            self.products_tree.insert("", "end", values=(product.name,f"{product.price}€"))

        # Define el estilo de los botones.
        button_style = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat"}

        # Crea un botón para volver al frame principal del panel de admin.
        self.back_button = Button(self, text="Atrás", bg="#333333", fg="white",**button_style, command=self.goBack_products)
        self.back_button.place(relx=0.003, rely=0.003, anchor="nw")

        self.button_style = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat"}
        self.button_style2 = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat", "background": "#d3d3d3"}


        self.modify_product_buttom = Button (self, text="Editar Producto", compound="bottom", command=self.modify_product,
                                       **self.button_style)
        self.modify_product_buttom.place(relx=0.3, rely=0.7, anchor="center")

        self.add_product_buttom = Button (self, text= "Añadir Producto", compound="bottom", command=self.add_product,
                                          **self.button_style)
        self.add_product_buttom.place(relx=0.7, rely=0.7, anchor="center")

        # Crear botón de eliminar producto
        self.delete_product_button = Button(self, text="Eliminar producto", bg="red", fg="white",
                               **self.button_style, command=self.delete_product)
        self.delete_product_button.place(relx=0.5, rely=0.8, anchor="center")


    def modify_product(self):
        selection = self.products_tree.selection()

        if not selection:
            messagebox.showerror("Error", "No product selected")
            return


        product = selection[0]
        product_data = self.products_tree.item(product, "values")
        product_name = product_data[0]
        product_price = float(product_data[1].rstrip("€"))

        self.modify_product_window = Toplevel(self)
        self.modify_product_window.title(f"Editar {product_name}")
        self.modify_product_window.geometry("300x400")
        self.modify_product_window.configure(bg="#e0e0e0")
        # Calcular la posición centrada de la ventana de modificación
        screen_width = self.modify_product_window.winfo_screenwidth()
        screen_height = self.modify_product_window.winfo_screenheight()
        window_width = 300
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.modify_product_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.modify_product_window.grab_set()
        self.modify_product_window.focus_set()

        # Crear etiquetas y entradas para modificar el nombre y precio
        name_label = Label(self.modify_product_window, text="Nombre:", font=("Comic Sans MS", 14))
        name_label.pack(pady=10)
        self.name_entry = Entry(self.modify_product_window, font=("Comic Sans MS", 14))
        self.name_entry.pack(pady=10)
        self.name_entry.insert(0, product_name)

        price_label = Label(self.modify_product_window, text="Precio (€):", font=("Comic Sans MS", 14))
        price_label.pack(pady=10)
        self.price_entry = Entry(self.modify_product_window, font=("Comic Sans MS", 14))
        self.price_entry.pack(pady=10)
        self.price_entry.insert(0, product_price)

        # Crear botón de guardar cambios
        save_button = Button(self.modify_product_window, text="Guardar cambios", **self.button_style,
                             command=self.save_product_changes)
        save_button.pack(pady=10)

    def save_product_changes(self):
        # Obtener el nombre del producto seleccionado
        product_name = self.products_tree.item(self.products_tree.selection()[0], "values")[0]

        # Verificar si el producto existe en la base de datos
        product = db.session.query(Product).filter_by(name=product_name).first()
        if product is None:
            messagebox.showerror("Error", "El producto no existe en la base de datos")
            return

        # Obtener los nuevos valores de nombre y precio
        new_name = self.name_entry.get()
        new_price = float(self.price_entry.get())

        # Actualizar los valores en la base de datos
        product.name = new_name
        product.price = new_price

        # Marcar la columna como modificada para que SQLAlchemy registre los cambios
        db.session.commit()

        # Actualizar la tabla de productos
        self.update_product_table()

        self.modify_product_window.destroy()

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Cambios guardados", "Los cambios se han guardado correctamente")

    def update_product_table(self):
        # Limpiar la tabla actual
        for row in self.products_tree.get_children():
            self.products_tree.delete(row)

        # Obtener la lista de productos actualizada
        all_products = db.session.query(Product).all()

        # Insertar los productos en la tabla
        for product in all_products:
            self.products_tree.insert("", "end", values=(product.name, f"{product.price}€"))

    def delete_product(self):
        self.clear_error_labels()
        item=self.products_tree.selection()

        if not item:
            # Si no se ha seleccionado ningún producto, muestra una etiqueta de error
            self.error_label = Label(self, text="Debes seleccionar un producto para eliminar",
                                     font=("Comic Sans MS", 12), fg="red")
            self.error_label.place(relx=0.5, rely=0.87, anchor="center")  # Ajusta la posición
            return

        # Obtener el producto seleccionado
        selected_item = item[0]




        product_name = self.products_tree.item(selected_item, "values")[0]
        print(product_name)
        product = db.session.query(Product).filter_by(name=product_name).first()

        # Preguntar si está seguro de eliminar el producto
        response = messagebox.askyesno("Eliminar producto", f"¿Estás seguro de eliminar el producto '{product.name}'?")

        if response:
            # Eliminar el producto de la base de datos
            db.session.delete(product)
            db.session.commit()

            self.update_product_table()
            # Mostrar mensaje de confirmación

            messagebox.showinfo("Producto eliminado", "El producto se ha eliminado correctamente")

    def add_product(self):
        self.add_product_window = Toplevel(self)
        self.add_product_window.title("Añadir Producto")
        self.add_product_window.geometry("300x400")
        self.add_product_window.grab_set()

        # Calcular la posición centrada
        screen_width = self.add_product_window.winfo_screenwidth()
        screen_height = self.add_product_window.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 400) // 2
        self.add_product_window.geometry(f"{300}x{400}+{x}+{y}")

        # Etiqueta y entrada para el nombre del producto
        self.name_label = Label(self.add_product_window, text="Nombre del Producto :", font=("Comic Sans MS", 12))
        self.name_label.pack(pady=(20, 5))  # Espaciado superior e inferior
        self.product_name_entry = Entry(self.add_product_window, font=("Comic Sans MS", 14))
        self.product_name_entry.pack(pady=(0, 20))  # Espaciado inferior

        # Etiqueta y entrada para el precio del producto
        self.price_label = Label(self.add_product_window, text="Precio del Producto :", font=("Comic Sans MS", 12))
        self.price_label.pack(pady=(20, 5))  # Espaciado superior e inferior
        self.product_price_entry = Entry(self.add_product_window, font=("Comic Sans MS", 14))
        self.product_price_entry.pack(pady=(0, 20))  # Espaciado inferior

        # Botón para confirmar la adición del producto
        self.confirm_button = Button(self.add_product_window, text="Crear Producto",
                                     command=lambda :
                                     self.create_product(name=self.product_name_entry.get(),
                                     price=self.product_price_entry.get()),**self.button_style2)
        self.confirm_button.pack(pady=20)

    def clear_error_labels(self):

        for widget in self.winfo_children():
            if isinstance(widget, Label) and widget.cget('fg') == 'red':
                widget.destroy()

        if hasattr(self, 'add_product_window') and self.add_product_window.winfo_exists():
            for widget in self.add_product_window.winfo_children():
                if isinstance(widget, Label) and widget.cget('fg') == 'red':
                    widget.destroy()

        # Elimina las etiquetas de error en la ventana de añadir usuario si existe
        if hasattr(self, 'add_user_window') and self.add_user_window.winfo_exists():
            for widget in self.add_user_window.winfo_children():
                if isinstance(widget, Label) and widget.cget('fg') == 'red':
                    widget.destroy()
    def create_product(self,name,price):

        if not name:
            self.clear_error_labels()
            self.product_name_empty_label = Label(self.add_product_window,
                                                  text="El nombre no puede estar vacío",
                                                  font=("Comic Sans MS", 12),
                                                  fg="red")
            self.product_name_empty_label.pack(pady=10)
            return
            # Verificar si el nombre excede la longitud máxima
        elif len(name) > 24:
            self.clear_error_labels()
            self.product_name_length_label = Label(self.add_product_window,
                                                   text="El nombre no puede\nexceder los 24 caracteres",
                                                   font=("Comic Sans MS", 12),
                                                   fg="red")
            self.product_name_length_label.pack(pady=10)
            return

        # Verifica si el precio del producto está vacío
        if not price:
            self.clear_error_labels()
            self.product_price_empty_label = Label(self.add_product_window,
                                                   text="El precio no puede estar vacío",
                                                   font=("Comic Sans MS", 12),
                                                   fg="red")
            self.product_price_empty_label.pack(pady=10)
            return


        try:
            # Intenta convertir el precio a un número flotante
            price = float(price)
        except ValueError:
            self.clear_error_labels()
            self.product_price_invalid_label = Label(self.add_product_window,
                                                     text="El precio debe ser un número válido",
                                                     font=("Comic Sans MS", 12),
                                                     fg="red")
            self.product_price_invalid_label.pack(pady=10)
            return

        # Si es correcto, confirma la adición del producto
        confirmation = messagebox.askyesno("Confirmar Adición",
                                           f"¿Quieres añadir el producto {name} con precio {price}?")

        if confirmation:
            new_product=Product(name=name,price=price)
            db.session.add(new_product)
            db.session.commit()
            # Aquí iría el código para añadir el producto
            # Por ejemplo, añadir el producto a la base de datos o a una lista

            self.add_product_window.destroy()  # Cierra la ventana de añadir producto

            self.update_product_table()
            self.add_success_label = Label(self, text=f"Producto añadido: {new_product.name}, Precio: {new_product.price}",
                                           font=("Comic Sans MS", 12), fg='green')
            self.add_success_label.place(relx=0.5, rely=0.87, anchor="center")  # Ajusta la posición

            # Usa after() para eliminar la etiqueta después de 3 segundos (3000 milisegundos)
            self.after(3000, self.remove_add_success_message)


        else:
            print("Añadido de producto cancelado")

    def remove_add_success_message(self):
        # Verifica si la etiqueta existe antes de intentar destruirla
        if hasattr(self, 'add_success_label') and self.add_success_label.winfo_exists():
            self.add_success_label.destroy()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def show_manage_users(self):
        # Limpiar el contenido actual del frame
        admin_frame_widets = [self.welcome_message, self.manage_products_button, self.manage_users_button]
        self.admin_frame_widets_info = []
        for widget in admin_frame_widets:
            info = widget.place_info()
            self.admin_frame_widets_info.append(info)
            widget.place_forget()

        # Crear el Frame que contendrá el Treeview
        self.table = Frame(self, bg="white")
        self.table.place(relx=0.25, rely=0.4, anchor="center", width=200, height=400)

        # Crear un estilo personalizado
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Custom.Treeview",
                            background="#d3d3d3",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="white",
                            font=('Comic Sans MS', 12))

        self.style.configure("Custom.Treeview.Heading",
                            background="#2e2e2e",
                            foreground="white",
                            font=('Comic Sans MS', 14, 'bold'))

        self.style.map("Custom.Treeview.Heading",
                       background=[("active", "#2e2e2e")],  # Keep the same background on hover
                       foreground=[("active", "white")])

        self.style.map("Custom.Treeview",
                       background=[("selected", "#4f4f4f")],
                       foreground=[("selected", "black")])

        # Crear el Treeview para mostrar los usuarios
        self.users_tree = ttk.Treeview(self.table, columns=("username"),
                                          show="headings", height=15, style="Custom.Treeview")
        self.users_tree.heading("username", text="Usuario")
        self.users_tree.column("username", anchor="center", width=200)


        # Agregar barra de desplazamiento vertical
        vsb = ttk.Scrollbar(self.table, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=vsb.set)

        # Empaquetar el Treeview y la barra de desplazamiento
        self.users_tree.pack(side='left', fill=BOTH, expand=True, padx=10, pady=10)
        vsb.pack(side='right', fill='y')

        all_users = db.session.query(User).filter_by(admin=0).all()

        for row in self.users_tree.get_children():
            self.users_tree.delete(row)

        self.users_tree.config(height=min(len(all_users),18))


        for user in all_users:
            self.users_tree.insert("", "end", values=(user.username))


        # Define el estilo de los botones.
        button_style = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat"}

        # Crea un botón para volver al frame principal del panel de admin.
        self.back_button = Button(self, text="Atrás", bg="#333333", fg="white",**button_style, command=self.goBack_users)
        self.back_button.place(relx=0.003, rely=0.003, anchor="nw")

        self.button_style = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat"}
        self.button_style2 = {"font": ("Comic Sans MS", 14), "padx": 10, "pady": 5, "relief": "flat", "background": "#d3d3d3"}


        self.modify_user_buttom = Button (self, text="Editar Usuario", compound="bottom", command=self.modify_user,
                                       **self.button_style)
        self.modify_user_buttom.place(relx=0.7, rely=0.3, anchor="center")

        self.add_user_buttom = Button (self, text= "Añadir Usuario", compound="bottom", command=self.add_user,
                                          **self.button_style)
        self.add_user_buttom.place(relx=0.7, rely=0.4, anchor="center")

        # Crear botón de eliminar producto
        self.delete_user_button = Button(self, text="Eliminar Usuario", bg="red", fg="white",
                               **self.button_style, command=self.delete_user)
        self.delete_user_button.place(relx=0.7, rely=0.5, anchor="center")


    def delete_user(self):
        user_selected=self.users_tree.selection()
        if not user_selected:
            error_label=Label (self, text="Debes seleccionar un usuario.", fg="red",
                                font=("Comic Sans MS", 12))
            error_label.place(relx=0.5, rely=0.95, anchor="center")
            return

        user=self.users_tree.item(user_selected)
        username= user["values"][0]

        user_to_delete= db.session.query(User).filter_by(username=username).first()
        cart_from_user= db.session.query(Cart).filter_by(username=username).first()
        confirm = messagebox.askyesno("Eliminar Producto",
                                      f"¿Estás seguro de que deseas eliminar el usuario \"{user_to_delete.username}\" ?")

        if confirm:
            db.session.delete(user_to_delete)
            db.session.delete(cart_from_user)
            db.session.commit()

            all_users=db.session.query(User).filter_by(admin=0).all()

            for row in self.users_tree.get_children():
                self.users_tree.delete(row)

            self.users_tree.config(height=min(len(all_users), 18))

            for user in all_users:
                self.users_tree.insert("", "end", values=(user.username))



    def modify_user(self):
        user_selected = self.users_tree.selection()
        if not user_selected:
            error_label = Label(self, text="Debes seleccionar un usuario.", fg="red",
                                font=("Comic Sans MS", 12))
            error_label.place(relx=0.5, rely=0.95, anchor="center")
            return

        user=self.users_tree.item(user_selected)
        username= user["values"][0]
        self.user_db=db.session.query(User).filter_by(username=username).first()

        self.user_modify_window=Toplevel(self)
        self.user_modify_window.title(f"Edición de {username}")
        self.user_modify_window.grab_set()  # Hace que la ventana sea modal
        self.user_modify_window.focus_set()  # Asegura que la ventana tenga el foco
        # Configurar el tamaño de la ventana de modificación
        self.user_modify_window.geometry("300x400")
        # Calcular la posición centrada de la ventana de modificación
        screen_width = self.user_modify_window.winfo_screenwidth()
        screen_height = self.user_modify_window.winfo_screenheight()
        window_width = 300
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.user_modify_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Crear etiquetas y entradas para modificar el nombre de usuario, contraseña y email
        username_label = Label(self.user_modify_window, text="Nombre de usuario:", font=("Comic Sans MS", 14))
        username_label.pack(pady=10)
        self.username_entry = Entry(self.user_modify_window, font=("Comic Sans MS", 14))
        self.username_entry.pack(pady=10)
        self.username_entry.insert(0, self.user_db.username)

        pasw_label = Label(self.user_modify_window, text="Contraseña:", font=("Comic Sans MS", 14))
        pasw_label.pack(pady=10)
        self.pasw_entry = Entry(self.user_modify_window, font=("Comic Sans MS", 14), show='*')
        self.pasw_entry.pack(pady=10)


        # Etiqueta y entrada para el correo electrónico
        email_label = Label(self.user_modify_window, text="Email:", font=("Comic Sans MS", 14))
        email_label.pack(pady=10)
        self.email_entry = Entry(self.user_modify_window, font=("Comic Sans MS", 14))
        self.email_entry.pack(pady=10)
        self.email_entry.insert(0, self.user_db.email)  # Prellena con el correo electrónico actual

        self.confirm_edit_user_button = Button(self.user_modify_window,text="Confirmar",command=self.confirm_edit_user,font=("Comic Sans MS",12))
        self.confirm_edit_user_button.place(relx=0.5, rely=0.9, anchor="center")


    def confirm_edit_user(self):
        # Obtener los nuevos valores
        new_username = self.username_entry.get()
        new_email = self.email_entry.get()
        new_password = self.pasw_entry.get()  # La contraseña ingresada, puede estar vacía

        # Verificar si el nuevo nombre de usuario está vacío
        if not new_username:
            messagebox.showerror("Error", "El nombre de usuario no puede estar vacío.")
            return

        # Obtener el usuario de la base de datos
        user_db = db.session.query(User).filter_by(username=self.user_db.username).first()
        if not user_db:
            messagebox.showerror("Error", "El usuario no se encontró en la base de datos.")
            return


        confirm=messagebox.askyesno(f"Confirmar cambios en {self.user_db.username}",
                                    "¿Quieres guardar los cambios realizados?")
        if not confirm:
            return

        # Actualizar los valores en la base de datos
        user_db.username = new_username
        user_db.email = new_email

        # Si se ha ingresado una nueva contraseña, actualizarla
        if len(new_password) >= 1:
            self.user_db.pasw = new_password

        db.session.commit()

        all_users = db.session.query(User).filter_by(admin=0).all()

        for row in self.users_tree.get_children():
            self.users_tree.delete(row)

        self.users_tree.config(height=min(len(all_users), 18))

        for user in all_users:
            self.users_tree.insert("", "end", values=(user.username))

        self.user_modify_window.destroy()

    def clear_error_labels_user(self):
        # Elimina etiquetas de error si existen
        for widget in self.add_user_window.winfo_children():
            if isinstance(widget, Label) and widget.cget("fg") == "red":
                widget.destroy()

    def add_user(self):
        self.add_user_window = Toplevel(self)
        self.add_user_window.title(f"Añadir Usuario")
        self.add_user_window.grab_set()  # Hace que la ventana sea modal
        self.add_user_window.focus_set()  # Asegura que la ventana tenga el foco
        # Configurar el tamaño de la ventana de modificación
        self.add_user_window.geometry("300x470")
        # Calcular la posición centrada de la ventana de modificación
        screen_width = self.add_user_window.winfo_screenwidth()
        screen_height = self.add_user_window.winfo_screenheight()
        window_width = 300
        window_height = 470
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.add_user_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Crear etiquetas y entradas usando place para organización
        username_label = Label(self.add_user_window, text="Nombre de usuario:", font=("Comic Sans MS", 14))
        username_label.place(relx=0.5, rely=0.1, anchor="center")
        self.username_entry = Entry(self.add_user_window, font=("Comic Sans MS", 14))
        self.username_entry.place(relx=0.5, rely=0.17, anchor="center", width=250)

        pasw_label = Label(self.add_user_window, text="Contraseña:", font=("Comic Sans MS", 14))
        pasw_label.place(relx=0.5, rely=0.30, anchor="center")
        self.pasw_entry = Entry(self.add_user_window, font=("Comic Sans MS", 14), show='*')
        self.pasw_entry.place(relx=0.5, rely=0.37, anchor="center", width=250)

        email_label = Label(self.add_user_window, text="Email:", font=("Comic Sans MS", 14))
        email_label.place(relx=0.5, rely=0.50, anchor="center")
        self.email_entry = Entry(self.add_user_window, font=("Comic Sans MS", 14))
        self.email_entry.place(relx=0.5, rely=0.57, anchor="center", width=250)

        date_label = Label(self.add_user_window, text="Fecha de nacimiento:", font=("Comic Sans MS", 14))
        date_label.place(relx=0.5, rely=0.69, anchor="center")

        # Campos de entrada para la fecha
        self.dayEntry = ttk.Combobox(self.add_user_window, font=("Comic Sans MS", 12),
                                     values=[str(i).zfill(2) for i in range(1, 32)], state="readonly", width=5)
        self.dayEntry.place(relx=0.20, rely=0.75, anchor="center")
        self.monthEntry = ttk.Combobox(self.add_user_window, font=("Comic Sans MS", 12),
                                       values=[f"{i:02d}" for i in range(1, 13)], state="readonly", width=5)
        self.monthEntry.place(relx=0.452, rely=0.75, anchor="center")
        self.yearEntry = ttk.Combobox(self.add_user_window, font=("Comic Sans MS", 12),
                                      values=[str(i) for i in range(2020, 1960, -1)], state="readonly", width=8)
        self.yearEntry.place(relx=0.75, rely=0.75, anchor="center")

        # Botón de confirmación
        create_user_button = Button(self.add_user_window, text="Añadir", command=self.create_user,
                                font=("Comic Sans MS", 12))
        create_user_button.place(relx=0.5, rely=0.92, anchor="center")

    def create_user(self):
        self.clear_error_labels()  # Limpia etiquetas de error existentes

        # Obtención de valores
        username = self.username_entry.get().strip()
        pasw = self.pasw_entry.get().strip()
        email = self.email_entry.get().strip()
        day = self.dayEntry.get().strip()
        month = self.monthEntry.get().strip()
        year = self.yearEntry.get().strip()

        # Inicialización de variables de validación
        username_validate = None
        pasw_validate = None
        email_validate = None
        birthday_validate = None

        # Validación de campos
        if not username:
            self.user_empty_label = Label(self.add_user_window, text="Usuario no puede estar vacío",
                                          font=("Comic Sans MS", 10), fg="red")
            self.user_empty_label.place(relx=0.5, rely=0.24, anchor="center")
        else:
            username_validate = username

        if not pasw:
            self.pasw_empty_label = Label(self.add_user_window, text="Contraseña no puede estar vacía",
                                          font=("Comic Sans MS", 10), fg="red")
            self.pasw_empty_label.place(relx=0.5, rely=0.44, anchor="center")
        else:
            pasw_validate = pasw

        if not (day and month and year):
            self.birthday_empty_label = Label(self.add_user_window, text="Fecha de nacimiento completa requerida",
                                              font=("Comic Sans MS", 10), fg="red")
            self.birthday_empty_label.place(relx=0.5, rely=0.82, anchor="center")
        else:
            try:
                birthday_ = datetime(int(year), int(month), int(day))
                birthday = birthday_.strftime("%d/%m/%Y")
                birthday_validate = birthday
            except ValueError:
                self.birthday_error_label = Label(self.add_user_window, text="Fecha de nacimiento inválida",
                                                  font=("Comic Sans MS", 10), fg="red")
                self.birthday_error_label.place(relx=0.5, rely=0.82, anchor="center")

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not email:
            self.email_empty_label = Label(self.add_user_window, text="E-Mail no puede estar vacío",
                                           font=("Comic Sans MS", 10), fg="red")
            self.email_empty_label.place(relx=0.5, rely=0.64, anchor="center")
        else:
            if not re.match(email_pattern, email):
                self.email_invalid_label = Label(self.add_user_window, text="Formato de E-Mail incorrecto",
                                                 font=("Comic Sans MS", 10), fg="red")
                self.email_invalid_label.place(relx=0.5, rely=0.64, anchor="center")
            else:
                email_validate = email

        # Verificación de existencia en la base de datos
        user_exists = db.session.query(User).filter_by(username=username).first()
        email_exists = db.session.query(User).filter_by(email=email).first()

        if username and user_exists:
            self.user_used_label = Label(self.add_user_window, text="Usuario ya existe", font=("Comic Sans MS", 10),
                                         fg="red")
            self.user_used_label.place(relx=0.5, rely=0.24, anchor="center")
            username_validate = None  # Invalidar el valor

        if email and email_exists:
            self.email_used_label = Label(self.add_user_window, text="E-Mail en uso", font=("Comic Sans MS", 10),
                                          fg="red")
            self.email_used_label.place(relx=0.5, rely=0.64, anchor="center")
            email_validate = None  # Invalidar el valor

        # Crear el nuevo usuario si todos los datos son válidos
        if username_validate and pasw_validate and birthday_validate and email_validate:
            new_user = User(username=username_validate, pasw=pasw_validate, email=email_validate,
                            birthday=birthday_validate)
            db.session.add(new_user)
            db.session.commit()
            all_users = db.session.query(User).filter_by(admin=0).all()

            for row in self.users_tree.get_children():
                self.users_tree.delete(row)

            self.users_tree.config(height=min(len(all_users), 18))

            for user in all_users:
                self.users_tree.insert("", "end", values=(user.username))

            self.add_user_window.destroy()  # Cierra la ventana de añadir usuario
            messagebox.showinfo("Éxito", f"Usuario {username_validate} creado correctamente")



    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def close_session(self):
        confirmation = messagebox.askyesno("Cerrar Sesión",
                                           f"¿Estás seguro de querer cerrar la sesión del usuario "
                                           f"\"{self.user.username}\"?")



        if confirmation:
            for i, widget in enumerate([self.welcome_message, self.manage_products_button, self.manage_users_button]):
                info = self.admin_frame_widets_info[i]
                widget.place(relx=info['relx'], rely=info['rely'], anchor=info['anchor'])

            widgets_to_hide = [self.table, self.back_button, self.modify_product_buttom, self.add_product_buttom,
                               self.delete_product_button]
            for widget in widgets_to_hide:
                widget.place_forget()

            widgets_to_hide = [self.table, self.back_button, self.modify_user_buttom, self.add_user_buttom,
                               self.delete_user_button]
            for widget in widgets_to_hide:
                widget.place_forget()

            self.controller.show_frame("FirstFrame", title="App Gestor de Productos")

    def goBack_users(self):
        # Ocultar los widgets actuales
        widgets_to_hide = [self.table, self.back_button, self.modify_user_buttom, self.add_user_buttom, self.delete_user_button]
        for widget in widgets_to_hide:
            widget.place_forget()

        # Mostrar los widgets anteriores
        for i, widget in enumerate([self.welcome_message, self.manage_products_button, self.manage_users_button]):
            info = self.admin_frame_widets_info[i]
            widget.place(relx=info['relx'], rely=info['rely'], anchor=info['anchor'])


    def goBack_products(self):
        # Ocultar los widgets actuales
        widgets_to_hide = [self.table, self.back_button, self.modify_product_buttom, self.add_product_buttom, self.delete_product_button]
        for widget in widgets_to_hide:
            widget.place_forget()

        # Mostrar los widgets anteriores
        for i, widget in enumerate([self.welcome_message, self.manage_products_button, self.manage_users_button]):
            info = self.admin_frame_widets_info[i]
            widget.place(relx=info['relx'], rely=info['rely'], anchor=info['anchor'])