import customtkinter as ctk
from tkinter import ttk, messagebox


class InventarioMixin:
    def build_inventory_tab(self):
        self.inventory_tab = self.tabview.tab("Inventario")
        self.inventory_tab.grid_columnconfigure(0, weight=1)

        tool_frame = ctk.CTkFrame(self.inventory_tab, fg_color="transparent")
        tool_frame.pack(fill="x", padx=10, pady=10)

        self.search_inventory_var = ctk.StringVar()
        self.search_inventory_var.trace("w", self.filter_inventory)
        self.search_entry_inv = ctk.CTkEntry(
            tool_frame,
            placeholder_text="Buscar medicamento...",
            width=350,
            textvariable=self.search_inventory_var
        )
        self.search_entry_inv.pack(side="left", padx=(0, 10))

        self.btn_new = ctk.CTkButton(tool_frame, text="+ Nuevo Producto", fg_color="#6366f1", hover_color="#4f46e5", command=self.open_add_window)
        self.btn_new.pack(side="right", padx=5)

        self.btn_delete = ctk.CTkButton(tool_frame, text="Eliminar Seleccionado", fg_color="#ef4444", hover_color="#dc2626", command=self.delete_product)
        self.btn_delete.pack(side="right", padx=5)

        self.btn_edit = ctk.CTkButton(tool_frame, text="Editar Seleccionado", fg_color="#0ea5e9", hover_color="#0284c7", command=self.edit_selected_product)
        self.btn_edit.pack(side="right", padx=5)

        self.tree_inv = ttk.Treeview(self.inventory_tab, columns=("ID", "Producto", "Marca", "Categoria", "Stock", "Precio"), show="headings")
        for col in self.tree_inv["columns"]:
            self.tree_inv.heading(col, text=col)
            self.tree_inv.column(col, width=100, anchor="center")

        self.tree_inv.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree_inv.bind("<Double-1>", lambda event: self.edit_selected_product())
        self.update_inventory_table()

    def update_inventory_table(self):
        for item in self.tree_inv.get_children():
            self.tree_inv.delete(item)

        for p in self.inventory:
            self.tree_inv.insert("", "end", values=(p["id"], p["prod"], p["marca"], p["cat"], p["stock"], f"${p['precio']:.2f}"))

        self.update_stock_alert()

    def get_selected_inventory_product(self):
        selected = self.tree_inv.selection()
        if not selected:
            messagebox.showwarning("Sin seleccion", "Selecciona un producto del inventario.")
            return None

        product_id = int(self.tree_inv.item(selected[0], "values")[0])
        return next((p for p in self.inventory if p["id"] == product_id), None)

    def edit_selected_product(self):
        product = self.get_selected_inventory_product()
        if product:
            self.open_product_editor(product)

    def open_product_editor(self, product):
        edit_win = ctk.CTkToplevel(self)
        edit_win.title("Editar Producto")
        edit_win.geometry("420x500")
        edit_win.attributes("-topmost", True)
        edit_win.grab_set()

        ctk.CTkLabel(edit_win, text="Editar Producto", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))

        fields = {}
        field_config = [
            ("prod", "Producto"),
            ("marca", "Marca"),
            ("cat", "Categoria"),
            ("prov", "Proveedor"),
            ("stock", "Stock"),
            ("precio", "Precio"),
            ("costo", "Costo"),
        ]

        form_frame = ctk.CTkFrame(edit_win, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20)

        for key, label in field_config:
            ctk.CTkLabel(form_frame, text=label).pack(anchor="w", pady=(8, 2))
            entry = ctk.CTkEntry(form_frame)
            entry.insert(0, str(product[key]))
            entry.pack(fill="x")
            fields[key] = entry

        def save_changes():
            try:
                stock = int(fields["stock"].get())
                precio = float(fields["precio"].get())
                costo = float(fields["costo"].get())
            except ValueError:
                messagebox.showerror("Datos invalidos", "Stock debe ser entero. Precio y costo deben ser numeros.")
                return

            if stock < 0 or precio < 0 or costo < 0:
                messagebox.showerror("Datos invalidos", "Stock, precio y costo no pueden ser negativos.")
                return

            for key in ("prod", "marca", "cat", "prov"):
                value = fields[key].get().strip()
                if not value:
                    messagebox.showerror("Datos incompletos", "Completa todos los campos de texto.")
                    return
                product[key] = value

            product["stock"] = stock
            product["precio"] = precio
            product["costo"] = costo

            self.update_inventory_table()
            if hasattr(self, "products_frame") and self.products_frame.winfo_exists():
                self.filter_sale_products()
            edit_win.destroy()

        buttons_frame = ctk.CTkFrame(edit_win, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkButton(buttons_frame, text="Guardar cambios", fg_color="#6366f1", hover_color="#4f46e5", command=save_changes).pack(side="right", padx=(5, 0))
        ctk.CTkButton(buttons_frame, text="Cancelar", fg_color="gray", hover_color="darkgray", command=edit_win.destroy).pack(side="right")

    def filter_inventory(self, *args):
        term = self.search_inventory_var.get().strip().lower()

        for item in self.tree_inv.get_children():
            self.tree_inv.delete(item)

        for p in self.inventory:
            searchable_text = " ".join([
                str(p["id"]),
                p["prod"],
                p["marca"],
                p["cat"],
                p["prov"],
                str(p["stock"]),
                f"{p['precio']:.2f}"
            ]).lower()

            if term in searchable_text:
                self.tree_inv.insert("", "end", values=(p["id"], p["prod"], p["marca"], p["cat"], p["stock"], f"${p['precio']:.2f}"))

    def open_add_window(self):
        # Crear la ventana secundaria
        add_win = ctk.CTkToplevel(self)
        add_win.title("Agregar Nuevo Producto")
        add_win.geometry("420x500")
        add_win.attributes("-topmost", True)
        add_win.grab_set()

        ctk.CTkLabel(add_win, text="Nuevo Producto", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))

        fields = {}
        field_config = [
            ("prod", "Producto"),
            ("marca", "Marca"),
            ("cat", "Categoria"),
            ("prov", "Proveedor"),
            ("stock", "Stock"),
            ("precio", "Precio"),
            ("costo", "Costo"),
        ]

        form_frame = ctk.CTkFrame(add_win, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20)

        # Crear los campos de entrada vacíos
        for key, label in field_config:
             ctk.CTkLabel(form_frame, text=label).pack(anchor="w", pady=(8, 2))
             entry = ctk.CTkEntry(form_frame)
             entry.pack(fill="x")
             fields[key] = entry


        def save_new_product():
            # Validar números
            try:
                stock = int(fields["stock"].get())
                precio = float(fields["precio"].get())
                costo = float(fields["costo"].get())
            except ValueError:
                messagebox.showerror("Datos inválidos", "El stock debe ser un número entero. El precio y costo deben ser números.")
                return

            if stock < 0 or precio < 0 or costo < 0:
                messagebox.showerror("Datos inválidos", "El stock, precio y costo no pueden ser negativos.")
                return

            # Crear el diccionario del nuevo producto
            new_product = {}
            for key in ("prod", "marca", "cat", "prov"):
                value = fields[key].get().strip()
                if not value:
                    messagebox.showerror("Datos incompletos", "Completa todos los campos de texto.")
                    return
                new_product[key] = value

            new_product["stock"] = stock
            new_product["precio"] = precio
            new_product["costo"] = costo

            # Generar ID dinámico (busca el máximo ID actual y le suma 1)
            if self.inventory:
                new_id = max(p["id"] for p in self.inventory) + 1
            else:
                new_id = 1  # Si el inventario está vacío, empieza en 1
            
            new_product["id"] = new_id

            # Agregar el producto a la lista de inventario principal
            self.inventory.append(new_product)

            # Actualizar la vista de la tabla
            self.update_inventory_table()
            
            # Actualizar otras vistas si es necesario (igual que en editar)
            if hasattr(self, "products_frame") and self.products_frame.winfo_exists():
                self.filter_sale_products()

            add_win.destroy()

        buttons_frame = ctk.CTkFrame(add_win, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)

        # Botones de guardar y cancelar
        ctk.CTkButton(buttons_frame, text="Guardar producto", fg_color="#10b981", hover_color="#059669", command=save_new_product).pack(side="right", padx=(5, 0))
        ctk.CTkButton(buttons_frame, text="Cancelar", fg_color="gray", hover_color="darkgray", command=add_win.destroy).pack(side="right")

    def delete_product(self):
        product = self.get_selected_inventory_product()
        if not product:
            return

        if not messagebox.askyesno("Confirmar", f"Eliminar {product['prod']} del inventario?"):
            return

        self.inventory.remove(product)
        self.update_inventory_table()
