import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3


class VentasMixin:
    def ensure_sales_schema(self):
        with self.get_db_connection() as conn:
            columns = [row[1] for row in conn.execute("PRAGMA table_info(ventas)").fetchall()]
            if "total" not in columns:
                conn.execute("ALTER TABLE ventas ADD COLUMN total REAL DEFAULT 0")
            if "fecha" not in columns:
                conn.execute("ALTER TABLE ventas ADD COLUMN fecha TEXT")
            if "empleado" not in columns:
                conn.execute("ALTER TABLE ventas ADD COLUMN empleado TEXT DEFAULT 'Empleado'")

    def load_sales_from_db(self):
        self.ensure_sales_schema()
        self.sales_history = []

        with self.get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            sales = conn.execute("""
                SELECT
                    v.num_venta,
                    v.cant_vendida,
                    v.total,
                    v.fecha,
                    COALESCE(v.empleado, 'Empleado') AS empleado,
                    COALESCE(p.nombre, 'Producto eliminado') AS producto
                FROM ventas v
                LEFT JOIN productos p ON p.legajo_ptoducto = v.id_producto
                ORDER BY v.num_venta DESC
            """).fetchall()

        for sale in sales:
            self.sales_history.append({
                "id": f"#{sale['num_venta']}",
                "prod": sale["producto"],
                "cant": sale["cant_vendida"],
                "total": float(sale["total"] or 0),
                "fecha": sale["fecha"] or "",
                "empleado": sale["empleado"],
            })

    def build_sales_tab(self):
        self.sales_tab = self.tabview.tab("Ventas")
        self.sales_tab.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(self.sales_tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(header_frame, text="Todas las Ventas", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(
            header_frame,
            text="+ Nueva Venta",
            fg_color="#6366f1",
            hover_color="#4f46e5",
            font=ctk.CTkFont(weight="bold"),
            command=self.open_new_sale_window
        ).pack(side="right")

        filters_frame = ctk.CTkFrame(self.sales_tab, fg_color="transparent")
        filters_frame.pack(fill="x", padx=10, pady=15)

        self.search_sale_var = ctk.StringVar()
        self.search_sale_var.trace("w", self.filter_sales)
        self.search_sale = ctk.CTkEntry(filters_frame, placeholder_text="Buscar por producto...", width=300, textvariable=self.search_sale_var)
        self.search_sale.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(filters_frame, text="Filtrar por Mes:").pack(side="left", padx=(0, 5))
        self.month_filter_var = ctk.StringVar(value="Todos los meses")
        self.combo_month = ctk.CTkComboBox(
            filters_frame,
            values=["Todos los meses", "marzo de 2026", "febrero de 2026"],
            variable=self.month_filter_var,
            command=self.filter_sales
        )
        self.combo_month.pack(side="left", padx=(0, 15))

        ctk.CTkButton(
            filters_frame,
            text="Limpiar Filtros",
            fg_color="gray",
            hover_color="darkgray",
            text_color="black",
            command=self.clear_sales_filters
        ).pack(side="right")

        self.lbl_sales_count = ctk.CTkLabel(self.sales_tab, text="Mostrando ventas...", text_color="gray")
        self.lbl_sales_count.pack(anchor="w", padx=10)

        self.tree_sales = ttk.Treeview(self.sales_tab, columns=("ID", "Producto", "Cantidad", "Total", "Fecha"), show="headings")
        for col in self.tree_sales["columns"]:
            self.tree_sales.heading(col, text=col)
            width = 150 if col in ("Producto", "Fecha") else 80
            self.tree_sales.column(col, width=width, anchor="center")

        self.tree_sales.pack(expand=True, fill="both", padx=10, pady=(5, 10))
        self.update_sales_table()

    def open_new_sale_window(self):
        self.cart = []
        self.ns_win = ctk.CTkToplevel(self)
        self.ns_win.title("Nueva Venta")
        self.ns_win.geometry("950x650")
        self.ns_win.attributes("-topmost", True)

        self.ns_win.grid_columnconfigure(0, weight=2)
        self.ns_win.grid_columnconfigure(1, weight=1)
        self.ns_win.grid_rowconfigure(1, weight=1)

        header_left = ctk.CTkFrame(self.ns_win, fg_color="transparent")
        header_left.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        ctk.CTkButton(
            header_left,
            text="<- Volver al Dashboard",
            fg_color="transparent",
            text_color="#6366f1",
            hover_color="#2b2b2b",
            command=self.ns_win.destroy,
            anchor="w"
        ).pack(side="top", anchor="w", pady=(0, 10))

        title_box = ctk.CTkFrame(header_left, fg_color="#f0f4ff" if ctk.get_appearance_mode() == "Light" else "#2b2b36", corner_radius=10)
        title_box.pack(fill="x")
        ctk.CTkLabel(title_box, text="Nueva Venta", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=15, pady=(15, 0))
        ctk.CTkLabel(title_box, text="Busca y selecciona productos para vender", text_color="gray").pack(anchor="w", padx=15, pady=(0, 15))

        self.search_sale_product_var = ctk.StringVar()
        self.search_sale_product_var.trace("w", self.filter_sale_products)
        self.search_bar_sale_products = ctk.CTkEntry(
            header_left,
            placeholder_text="Buscar medicamento por nombre...",
            height=35,
            textvariable=self.search_sale_product_var
        )
        self.search_bar_sale_products.pack(fill="x", pady=10)

        filters_row = ctk.CTkFrame(header_left, fg_color="transparent")
        filters_row.pack(fill="x")

        ctk.CTkComboBox(filters_row, values=["Todas las categorias"]).pack(side="left", expand=True, padx=2)
        ctk.CTkComboBox(filters_row, values=["Todos las marcas"]).pack(side="left", expand=True, padx=2)
        ctk.CTkComboBox(filters_row, values=["Todos los proveedores"]).pack(side="left", expand=True, padx=2)

        self.products_frame = ctk.CTkScrollableFrame(self.ns_win, fg_color="transparent")
        self.products_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.render_sale_products()

        cart_panel = ctk.CTkFrame(self.ns_win, fg_color="#1e1e1e", corner_radius=15)
        cart_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=40)

        ctk.CTkLabel(cart_panel, text="Carrito", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=20)

        self.cart_items_frame = ctk.CTkScrollableFrame(cart_panel, fg_color="transparent", height=200)
        self.cart_items_frame.pack(fill="both", expand=True, padx=10)

        self.cart_empty_lbl = ctk.CTkLabel(self.cart_items_frame, text="El carrito esta vacio", text_color="gray")
        self.cart_empty_lbl.pack(pady=50)

        summary_frame = ctk.CTkFrame(cart_panel, fg_color="transparent")
        summary_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(summary_frame, text="Resumen", font=ctk.CTkFont(weight="bold")).pack(anchor="w")

        self.lbl_distintos = ctk.CTkLabel(summary_frame, text="Productos distintos: 0")
        self.lbl_distintos.pack(anchor="w")
        self.lbl_unidades = ctk.CTkLabel(summary_frame, text="Unidades totales: 0")
        self.lbl_unidades.pack(anchor="w")

        total_frame = ctk.CTkFrame(cart_panel, fg_color="transparent")
        total_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(total_frame, text="Total:", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        self.lbl_total_price = ctk.CTkLabel(total_frame, text="$0.00", text_color="#10b981", font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_total_price.pack(side="right")

        self.btn_complete = ctk.CTkButton(cart_panel, text="Completar Venta", fg_color="gray", state="disabled", command=self.complete_sale)
        self.btn_complete.pack(fill="x", padx=20, pady=(10, 5))
        ctk.CTkButton(cart_panel, text="Cancelar", fg_color="transparent", border_width=1, hover_color="#333", command=self.ns_win.destroy).pack(fill="x", padx=20, pady=(0, 20))

    def render_sale_products(self, products=None):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        products = self.inventory if products is None else products

        if not products:
            ctk.CTkLabel(self.products_frame, text="No se encontraron productos", text_color="gray").pack(pady=30)
            return

        for p in products:
            card = ctk.CTkFrame(self.products_frame, fg_color="#2b2b2b", corner_radius=10)
            card.pack(fill="x", pady=5)

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", padx=15, pady=10)

            ctk.CTkLabel(info_frame, text=p["prod"], font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w")

            badges_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            badges_frame.pack(anchor="w", pady=(2, 0))
            ctk.CTkLabel(badges_frame, text=f"Marca: {p['marca']}", text_color="#6366f1", font=ctk.CTkFont(size=10)).pack(side="left", padx=(0, 5))
            ctk.CTkLabel(badges_frame, text=f"Categoria: {p['cat']}", text_color="#a855f7", font=ctk.CTkFont(size=10)).pack(side="left", padx=(0, 5))
            ctk.CTkLabel(badges_frame, text=f"Prov: {p['prov']}", text_color="#10b981", font=ctk.CTkFont(size=10)).pack(side="left")

            action_frame = ctk.CTkFrame(card, fg_color="transparent")
            action_frame.pack(side="right", padx=15, pady=10)

            price_stock = ctk.CTkFrame(action_frame, fg_color="transparent")
            price_stock.pack(side="left", padx=(0, 15))
            ctk.CTkLabel(price_stock, text=f"${p['precio']:.2f}", font=ctk.CTkFont(weight="bold")).pack()
            ctk.CTkLabel(price_stock, text=f"Stock: {p['stock']}", text_color="gray", font=ctk.CTkFont(size=11)).pack()

            ctk.CTkButton(action_frame, text="+ Agregar", width=80, fg_color="#6366f1", hover_color="#4f46e5", command=lambda item=p: self.add_to_cart(item)).pack(side="right")

    def add_to_cart(self, product):
        found = False
        for c_item in self.cart:
            if c_item["id"] == product["id"]:
                if c_item["cant"] < product["stock"]:
                    c_item["cant"] += 1
                else:
                    messagebox.showwarning("Stock Insuficiente", "No hay mas unidades disponibles de este producto.")
                found = True
                break

        if not found:
            if product["stock"] > 0:
                self.cart.append({"id": product["id"], "prod": product["prod"], "precio": product["precio"], "cant": 1})
            else:
                messagebox.showwarning("Sin Stock", "Producto agotado.")
                return

        self.update_cart_ui()

    def update_cart_ui(self):
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        if not self.cart:
            self.cart_empty_lbl = ctk.CTkLabel(self.cart_items_frame, text="El carrito esta vacio", text_color="gray")
            self.cart_empty_lbl.pack(pady=50)
            self.btn_complete.configure(state="disabled", fg_color="gray")
            self.lbl_distintos.configure(text="Productos distintos: 0")
            self.lbl_unidades.configure(text="Unidades totales: 0")
            self.lbl_total_price.configure(text="$0.00")
            return

        self.btn_complete.configure(state="normal", fg_color="#6366f1")

        total_price = 0
        total_units = 0

        for item in self.cart:
            total_price += item["precio"] * item["cant"]
            total_units += item["cant"]

            item_row = ctk.CTkFrame(self.cart_items_frame, fg_color="#333", corner_radius=5)
            item_row.pack(fill="x", pady=2)
            ctk.CTkLabel(item_row, text=f"{item['cant']}x {item['prod']}", font=ctk.CTkFont(size=12)).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(item_row, text=f"${(item['precio'] * item['cant']):.2f}").pack(side="right", padx=10)

        self.lbl_distintos.configure(text=f"Productos distintos: {len(self.cart)}")
        self.lbl_unidades.configure(text=f"Unidades totales: {total_units}")
        self.lbl_total_price.configure(text=f"${total_price:.2f}")

    def complete_sale(self):
        if not self.cart:
            return

        total = sum(i["precio"] * i["cant"] for i in self.cart)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

        try:
            self.ensure_sales_schema()
            with self.get_db_connection() as conn:
                for item in self.cart:
                    current_stock = conn.execute(
                        "SELECT stock FROM productos WHERE legajo_ptoducto = ?",
                        (item["id"],)
                    ).fetchone()

                    if current_stock is None:
                        messagebox.showerror("Error", f"El producto {item['prod']} ya no existe en la base.")
                        return

                    if current_stock[0] < item["cant"]:
                        messagebox.showwarning("Stock Insuficiente", f"No hay stock suficiente de {item['prod']}.")
                        return

                    conn.execute("""
                        INSERT INTO ventas (cant_vendida, id_producto, total, fecha, empleado)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        item["cant"],
                        item["id"],
                        item["precio"] * item["cant"],
                        fecha,
                        "Empleado",
                    ))
                    conn.execute(
                        "UPDATE productos SET stock = stock - ? WHERE legajo_ptoducto = ?",
                        (item["cant"], item["id"])
                    )
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"No se pudo guardar la venta: {error}")
            return

        self.load_sales_from_db()
        self.load_inventory_from_db()
        self.update_inventory_table()
        self.update_stock_alert()
        self.filter_sales()
        self.update_metric_cards()
        if hasattr(self, "update_stats_dashboard"):
            self.update_stats_dashboard()

        messagebox.showinfo("Exito", f"Venta completada con exito. Total: ${total:.2f}")
        self.ns_win.destroy()

    def filter_sale_products(self, *args):
        term = self.search_sale_product_var.get().strip().lower()
        filtered_products = [
            p for p in self.inventory
            if term in " ".join([p["prod"], p["marca"], p["cat"], p["prov"]]).lower()
        ]
        self.render_sale_products(filtered_products)

    def filter_sales(self, *args):
        term = self.search_sale_var.get().lower()
        mes = self.month_filter_var.get()

        for item in self.tree_sales.get_children():
            self.tree_sales.delete(item)

        count = 0
        for s in self.sales_history:
            match_term = term in s["prod"].lower()
            match_mes = True
            if mes == "marzo de 2026":
                match_mes = "-03-" in s["fecha"]
            elif mes == "febrero de 2026":
                match_mes = "-02-" in s["fecha"]

            if match_term and match_mes:
                self.tree_sales.insert("", "end", values=(s["id"], s["prod"], s["cant"], f"${s['total']:.2f}", s["fecha"]))
                count += 1

        self.lbl_sales_count.configure(text=f"Mostrando {count} de {len(self.sales_history)} ventas")

    def update_sales_table(self):
        self.filter_sales()

    def clear_sales_filters(self):
        self.search_sale_var.set("")
        self.month_filter_var.set("Todos los meses")
        self.filter_sales()
