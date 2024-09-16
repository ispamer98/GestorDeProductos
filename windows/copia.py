def add_cart(self):
    selection = self.tree.selection()
    for item in selection:
        item_data = self.tree.item(item, "values")
        product_name = item_data[0]
        product_price = item_data[1]

        # Convertir los items del carrito de JSON a una lista de Python
        cart_items = json.loads(self.cart.items)

        # Verifica si el producto ya está en el carrito
        found = False
        for cart_item in cart_items:
            if cart_item["name"] == product_name:
                # Incrementar la cantidad si el producto ya está en el carrito
                cart_item["quantity"] += 1
                found = True
                break

        # Si el producto no está en el carrito, agregarlo con cantidad 1
        if not found:
            cart_items.append({"name": product_name, "price": product_price, "quantity": 1})

        # Convertir la lista de nuevo a JSON y guardarla en el carrito
        self.cart.items = json.dumps(cart_items)
        db.session.commit()  # Guardar los cambios en la base de datos

    print(self.cart.items)


def show_cart(self):
    # Crear la ventana del carrito
    cart_window = tk.Toplevel(self)
    cart_window.title("Carrito de Compras")
    cart_window.grab_set()  # Captura todos los eventos hasta que se cierre

    # Centrar la ventana en la pantalla
    self.center_window(cart_window, 600, 400)

    # Crear el Treeview para mostrar los productos, precios, cantidades y el total en el carrito
    cart_tree = ttk.Treeview(cart_window, columns=("Producto", "Precio", "Cantidad", "Total"), show="headings",
                             height=10)
    cart_tree.heading("Producto", text="Producto")
    cart_tree.heading("Precio", text="Precio (€)")
    cart_tree.heading("Cantidad", text="Cantidad")
    cart_tree.heading("Total", text="Total (€)")

    cart_tree.column("Producto", anchor="center", width=150)
    cart_tree.column("Precio", anchor="center", width=100)
    cart_tree.column("Cantidad", anchor="center", width=100)
    cart_tree.column("Total", anchor="center", width=100)

    cart_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Convertir los items del carrito de JSON a una lista de Python
    cart_items = json.loads(self.cart.items)

    # Calcular el total del carrito
    total_cart = 0
    for item in cart_items:
        name = item["name"]
        price_str = item["price"].replace('€', '').strip()
        price = float(price_str)
        count = item["quantity"]
        total = float(count) * price
        total_cart += total

        # Insertar los valores en el Treeview
        cart_tree.insert("", tk.END, values=(name, f"{price}€", count, f"{total:.2f}€"))

    # Mostrar el total del carrito
    total_label = tk.Label(cart_window, text=f"Total del Carrito: {total_cart:.2f}€", font=("Arial", 14, "bold"))
    total_label.pack(pady=10, anchor="e")

    def open_remove_window():
        selected_item = cart_tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleccionar producto", "Por favor, selecciona un producto.")
            return

        item_data = cart_tree.item(selected_item[0], "values")
        name = item_data[0]
        max_quantity = int(item_data[2])

        # Ventana de ajuste de cantidad
        remove_window = tk.Toplevel(cart_window)
        remove_window.title("Eliminar Cantidad")
        remove_window.grab_set()  # Captura todos los eventos hasta que se cierre

        # Centrar la ventana de ajuste en la ventana del carrito
        self.center_window(remove_window, 400, 200)  # Puedes ajustar el tamaño según sea necesario

        tk.Label(remove_window, text=f"Eliminar de '{name}'", font=("Arial", 14)).pack(pady=10)

        # Variable para la cantidad a eliminar
        remove_amount = tk.IntVar(value=1)

        # Funciones para aumentar y disminuir la cantidad
        def increase_quantity():
            if remove_amount.get() < max_quantity:
                remove_amount.set(remove_amount.get() + 1)

        def decrease_quantity():
            if remove_amount.get() > 1:
                remove_amount.set(remove_amount.get() - 1)

        # Mostrar la cantidad a eliminar
        quantity_label = tk.Label(remove_window, textvariable=remove_amount, font=("Arial", 12))
        quantity_label.pack(pady=5)

        # Botones para aumentar y disminuir la cantidad
        button_frame = tk.Frame(remove_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="+", command=increase_quantity, font=("Arial", 12)).pack(side=tk.LEFT,
                                                                                              padx=5)
        tk.Button(button_frame, text="-", command=decrease_quantity, font=("Arial", 12)).pack(side=tk.LEFT,
                                                                                              padx=5)

        # Botones para confirmar o cancelar
        def remove_quantity():
            quantity_to_remove = remove_amount.get()
            confirm = messagebox.askyesno("Confirmar eliminación",
                                          f"¿Estás seguro de que quieres eliminar {quantity_to_remove} del producto '{name}'?")
            if not confirm:
                return

            # Actualizar el carrito
            if quantity_to_remove >= max_quantity:
                self.cart = [i for i in self.cart.items if i["name"] != name]
                cart_tree.delete(selected_item[0])
            else:
                for cart_item in self.cart.items:
                    if cart_item["name"] == name:
                        cart_item["quantity"] -= quantity_to_remove
                        break
                cart_tree.item(selected_item[0], values=(name, f"{item_data[1]}", max_quantity - quantity_to_remove,
                                                         f"{(max_quantity - quantity_to_remove) * float(item_data[1].replace('€', '').strip()):.2f}€"))

            # Actualizar el total del carrito
            self.update_cart_total(cart_window)
            remove_window.destroy()

        tk.Button(remove_window, text="Eliminar", command=remove_quantity, font=("Arial", 12)).pack(side=tk.LEFT,
                                                                                                    padx=5, pady=10)
        tk.Button(remove_window, text="Cancelar", command=remove_window.destroy, font=("Arial", 12)).pack(
            side=tk.RIGHT, padx=5, pady=10)

    # Botón para abrir la ventana de eliminación
    remove_button = tk.Button(cart_window, text="Eliminar Producto", command=open_remove_window, font=("Arial", 12))
    remove_button.pack(pady=10, side=tk.LEFT, padx=10)

    # Actualizar el total del carrito
    self.update_cart_total(cart_window)


def center_window(self, window, width, height):
    # Obtener el tamaño de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular la posición x, y para centrar la ventana
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Establecer el tamaño y la posición de la ventana
    window.geometry(f"{width}x{height}+{x}+{y}")


def update_cart_total(self, cart_window):
    total_cart = 0
    for item in self.cart.items:
        price_str = item["price"].replace('€', '').strip()
        price = float(price_str)
        count = item["quantity"]
        total = float(count) * price
        total_cart += total

    # Actualizar la etiqueta del total en la ventana del carrito
    for widget in cart_window.winfo_children():
        if isinstance(widget, tk.Label) and "Total del Carrito" in widget.cget("text"):
            widget.config(text=f"Total del Carrito: {total_cart:.2f}€")
            break


def show_products(self):
    # Limpiar el Treeview antes de mostrar los productos
    for row in self.tree.get_children():
        self.tree.delete(row)

    # Obtener los productos desde la base de datos
    all_products = db.session.query(Product).all()

    self.tree.config(height=min(len(all_products), 18))

    # Insertar los productos en la tabla
    for product in all_products:
        self.tree.insert("", "end", values=(product.name, f"{product.price:.2f}€"))