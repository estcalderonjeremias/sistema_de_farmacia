import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

# --- CONFIGURACIÓN GLOBAL ---
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class PharmacyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión de Farmacia - Panel Administrativo")
        self.geometry("1100x750") # Un poco más ancho para acomodar la tabla de ventas

        # --- BASE DE DATOS SIMULADA ---
        self.inventory = [
            {"id": 1, "prod": "Paracetamol 500mg", "marca": "Bayer", "cat": "Analgésico", "prov": "Droguería Sur", "stock": 150, "costo": 0.50, "precio": 5.50},
            {"id": 2, "prod": "Loratadina 10mg", "marca": "Ultra-Health", "cat": "Antihistamínico", "prov": "Farmacity Dist", "stock": 5, "costo": 1.20, "precio": 3.00},
            {"id": 3, "prod": "Ibuprofeno 400mg", "marca": "Pfizer", "cat": "Antiinflamatorio", "prov": "Farmacity Dist", "stock": 85, "costo": 2.00, "precio": 7.00},
            {"id": 4, "prod": "Amoxicilina 500mg", "marca": "GlaxoSmithKline", "cat": "Antibiótico", "prov": "Droguería Sur", "stock": 80, "costo": 5.00, "precio": 12.50},
            {"id": 5, "prod": "Omeprazol 20mg", "marca": "Genérico", "cat": "Gástrico", "prov": "Medistore", "stock": 40, "costo": 8.00, "precio": 16.00},
        ]

        # Se eliminó la clave "vend" del historial de ventas
        self.sales_history = [
            {"id": "#1", "prod": "Paracetamol 500mg", "cant": 2, "total": 11.00, "fecha": "2026-03-15 10:30"},
            {"id": "#2", "prod": "Ibuprofeno 400mg", "cant": 1, "total": 7.00, "fecha": "2026-03-16 11:15"},
            {"id": "#3", "prod": "Amoxicilina 500mg", "cant": 3, "total": 37.50, "fecha": "2026-03-20 14:20"},
            {"id": "#4", "prod": "Omeprazol 20mg", "cant": 2, "total": 32.00, "fecha": "2026-02-25 09:45"},
        ]

        self.cart = [] # Almacena los productos temporales de la nueva venta

        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # --- 1. TARJETAS DE MÉTRICAS ---
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.metrics_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.create_metric_card(0, "Productos", str(len(self.inventory)), "📦")
        self.create_metric_card(1, "Ventas Totales", f"${sum(s['total'] for s in self.sales_history):.2f}", "💰")
        self.create_metric_card(2, "Ganancia Potencial", "$2442.50", "📈")
        self.create_metric_card(3, "Stock Bajo", "1", "⚠️", icon_color="#e67e22")

        # --- 2. BANNER DE ALERTA ---
        self.alert_frame = ctk.CTkFrame(self, fg_color="#fff4e6", border_color="#d97706", border_width=1)
        self.alert_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        alert_label = ctk.CTkLabel(self.alert_frame, text="⚠️ Alertas de Stock Bajo: Loratadina 10mg necesitan reabastecimiento.", 
                                  text_color="#d97706", font=ctk.CTkFont(size=13, weight="bold"))
        alert_label.pack(side="left", padx=15, pady=10)

        # --- 3. PANEL DE PESTAÑAS ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#6366f1")
        self.tabview.grid(row=2, column=0, padx=20, pady=0, sticky="nsew", rowspan=3)
        self.tabview.add("Inventario")
        self.tabview.add("Ventas")
        self.tabview.add("Recetas")
        
        # --- ESTILOS TABLAS (Treeview) ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=35, fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#3f3f3f", foreground="white", font=('Arial', 10, 'bold'))
        style.map("Treeview", background=[('selected', '#6366f1')]) 

        # --- CONSTRUIR PESTAÑAS ---
        self.build_inventory_tab()
        self.build_sales_tab()
        
        self.tabview.set("Ventas") 

    # ==========================================
    #             PESTAÑA INVENTARIO
    # ==========================================
    def build_inventory_tab(self):
        self.inventory_tab = self.tabview.tab("Inventario")
        self.inventory_tab.grid_columnconfigure(0, weight=1)

        tool_frame = ctk.CTkFrame(self.inventory_tab, fg_color="transparent")
        tool_frame.pack(fill="x", padx=10, pady=10)

        self.search_entry_inv = ctk.CTkEntry(tool_frame, placeholder_text="Buscar medicamento...", width=350)
        self.search_entry_inv.pack(side="left", padx=(0, 10))

        self.btn_new = ctk.CTkButton(tool_frame, text="+ Nuevo Producto", fg_color="#6366f1", hover_color="#4f46e5", command=self.open_add_window)
        self.btn_new.pack(side="right", padx=5)

        self.btn_delete = ctk.CTkButton(tool_frame, text="Eliminar Seleccionado", fg_color="#ef4444", hover_color="#dc2626", command=self.delete_product)
        self.btn_delete.pack(side="right", padx=5)

        self.tree_inv = ttk.Treeview(self.inventory_tab, columns=("ID", "Producto", "Marca", "Categoría", "Stock", "Precio"), show="headings")
        for col in self.tree_inv["columns"]:
            self.tree_inv.heading(col, text=col)
            self.tree_inv.column(col, width=100, anchor="center")

        self.tree_inv.pack(expand=True, fill="both", padx=10, pady=10)
        self.update_inventory_table()

    # ==========================================
    #               PESTAÑA VENTAS
    # ==========================================
    def build_sales_tab(self):
        self.sales_tab = self.tabview.tab("Ventas")
        self.sales_tab.grid_columnconfigure(0, weight=1)

        # Header: Título y Botón Nueva Venta
        header_frame = ctk.CTkFrame(self.sales_tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        ctk.CTkLabel(header_frame, text="Todas las Ventas", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(header_frame, text="+ Nueva Venta", fg_color="#6366f1", hover_color="#4f46e5", font=ctk.CTkFont(weight="bold"), 
                      command=self.open_new_sale_window).pack(side="right")

        # Filtros
        filters_frame = ctk.CTkFrame(self.sales_tab, fg_color="transparent")
        filters_frame.pack(fill="x", padx=10, pady=15)

        self.search_sale_var = ctk.StringVar()
        self.search_sale_var.trace("w", self.filter_sales)
        self.search_sale = ctk.CTkEntry(filters_frame, placeholder_text="Buscar por producto...", width=300, textvariable=self.search_sale_var)
        self.search_sale.pack(side="left", padx=(0, 15))

        # Filtro de Mes
        ctk.CTkLabel(filters_frame, text="Filtrar por Mes:").pack(side="left", padx=(0, 5))
        self.month_filter_var = ctk.StringVar(value="Todos los meses")
        self.combo_month = ctk.CTkComboBox(filters_frame, values=["Todos los meses", "marzo de 2026", "febrero de 2026"], 
                                           variable=self.month_filter_var, command=self.filter_sales)
        self.combo_month.pack(side="left", padx=(0, 15))

        # Botón Limpiar Filtros
        ctk.CTkButton(filters_frame, text="Limpiar Filtros", fg_color="gray", hover_color="darkgray", text_color="black", 
                      command=self.clear_sales_filters).pack(side="right")

        # Etiqueta de resultados
        self.lbl_sales_count = ctk.CTkLabel(self.sales_tab, text="Mostrando ventas...", text_color="gray")
        self.lbl_sales_count.pack(anchor="w", padx=10)

        # Tabla de Ventas (Se eliminó la columna vendedor)
        self.tree_sales = ttk.Treeview(self.sales_tab, columns=("ID", "Producto", "Cantidad", "Total", "Fecha"), show="headings")
        for col in self.tree_sales["columns"]:
            self.tree_sales.heading(col, text=col)
            width = 150 if col in ("Producto", "Fecha") else 80
            self.tree_sales.column(col, width=width, anchor="center")

        self.tree_sales.pack(expand=True, fill="both", padx=10, pady=(5, 10))
        self.update_sales_table()

    # ==========================================
    #       VENTANA: NUEVA VENTA (MÓDULO)
    # ==========================================
    def open_new_sale_window(self):
        self.cart = [] # Vaciar carrito al iniciar
        self.ns_win = ctk.CTkToplevel(self)
        self.ns_win.title("Nueva Venta")
        self.ns_win.geometry("950x650")
        self.ns_win.attributes("-topmost", True)
        
        self.ns_win.grid_columnconfigure(0, weight=2) # Área Izquierda (Productos)
        self.ns_win.grid_columnconfigure(1, weight=1) # Área Derecha (Carrito)
        self.ns_win.grid_rowconfigure(1, weight=1)

        # --- CABECERA IZQUIERDA ---
        header_left = ctk.CTkFrame(self.ns_win, fg_color="transparent")
        header_left.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkButton(header_left, text="← Volver al Dashboard", fg_color="transparent", text_color="#6366f1", hover_color="#2b2b2b",
                      command=self.ns_win.destroy, anchor="w").pack(side="top", anchor="w", pady=(0, 10))
        
        title_box = ctk.CTkFrame(header_left, fg_color="#f0f4ff" if ctk.get_appearance_mode()=="Light" else "#2b2b36", corner_radius=10)
        title_box.pack(fill="x")
        ctk.CTkLabel(title_box, text="🛒 Nueva Venta", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=15, pady=(15, 0))
        ctk.CTkLabel(title_box, text="Busca y selecciona productos para vender", text_color="gray").pack(anchor="w", padx=15, pady=(0, 15))

        # Buscador y filtros de Nueva Venta
        search_bar = ctk.CTkEntry(header_left, placeholder_text="Buscar medicamento por nombre...", height=35)
        search_bar.pack(fill="x", pady=10)

        filters_row = ctk.CTkFrame(header_left, fg_color="transparent")
        filters_row.pack(fill="x")
        
        ctk.CTkComboBox(filters_row, values=["Todas las drogas"]).pack(side="left", expand=True, padx=2)
        ctk.CTkComboBox(filters_row, values=["Todos los laboratorios"]).pack(side="left", expand=True, padx=2)
        ctk.CTkComboBox(filters_row, values=["Todos los proveedores"]).pack(side="left", expand=True, padx=2)

        # --- LISTA DE PRODUCTOS (Scrollable) ---
        self.products_frame = ctk.CTkScrollableFrame(self.ns_win, fg_color="transparent")
        self.products_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.render_sale_products()

        # --- PANEL DERECHO (CARRITO) ---
        cart_panel = ctk.CTkFrame(self.ns_win, fg_color="#1e1e1e", corner_radius=15)
        cart_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=40)
        
        ctk.CTkLabel(cart_panel, text="🛒 Carrito", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=20)
        
        self.cart_items_frame = ctk.CTkScrollableFrame(cart_panel, fg_color="transparent", height=200)
        self.cart_items_frame.pack(fill="both", expand=True, padx=10)
        
        self.cart_empty_lbl = ctk.CTkLabel(self.cart_items_frame, text="El carrito está vacío", text_color="gray")
        self.cart_empty_lbl.pack(pady=50)

        # Resumen del carrito
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

    def render_sale_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        for p in self.inventory:
            card = ctk.CTkFrame(self.products_frame, fg_color="#2b2b2b", corner_radius=10)
            card.pack(fill="x", pady=5)
            
            # Info Izquierda
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", padx=15, pady=10)
            
            ctk.CTkLabel(info_frame, text=p["prod"], font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w")
            
            badges_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            badges_frame.pack(anchor="w", pady=(2,0))
            ctk.CTkLabel(badges_frame, text=f"Lab: {p['marca']}", text_color="#6366f1", font=ctk.CTkFont(size=10)).pack(side="left", padx=(0,5))
            ctk.CTkLabel(badges_frame, text=f"Droga: {p['cat']}", text_color="#a855f7", font=ctk.CTkFont(size=10)).pack(side="left", padx=(0,5))
            ctk.CTkLabel(badges_frame, text=f"Prov: {p['prov']}", text_color="#10b981", font=ctk.CTkFont(size=10)).pack(side="left")

            # Info Derecha
            action_frame = ctk.CTkFrame(card, fg_color="transparent")
            action_frame.pack(side="right", padx=15, pady=10)
            
            price_stock = ctk.CTkFrame(action_frame, fg_color="transparent")
            price_stock.pack(side="left", padx=(0, 15))
            ctk.CTkLabel(price_stock, text=f"${p['precio']:.2f}", font=ctk.CTkFont(weight="bold")).pack()
            ctk.CTkLabel(price_stock, text=f"Stock: {p['stock']}", text_color="gray", font=ctk.CTkFont(size=11)).pack()

            ctk.CTkButton(action_frame, text="+ Agregar", width=80, fg_color="#6366f1", hover_color="#4f46e5", 
                          command=lambda item=p: self.add_to_cart(item)).pack(side="right")

    def add_to_cart(self, product):
        found = False
        for c_item in self.cart:
            if c_item["id"] == product["id"]:
                if c_item["cant"] < product["stock"]:
                    c_item["cant"] += 1
                else:
                    messagebox.showwarning("Stock Insuficiente", "No hay más unidades disponibles de este producto.")
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
            self.cart_empty_lbl = ctk.CTkLabel(self.cart_items_frame, text="El carrito está vacío", text_color="gray")
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
            ctk.CTkLabel(item_row, text=f"${(item['precio']*item['cant']):.2f}").pack(side="right", padx=10)

        self.lbl_distintos.configure(text=f"Productos distintos: {len(self.cart)}")
        self.lbl_unidades.configure(text=f"Unidades totales: {total_units}")
        self.lbl_total_price.configure(text=f"${total_price:.2f}")

    def complete_sale(self):
        if not self.cart: return
        
        total = sum(i["precio"]*i["cant"] for i in self.cart)
        
        # 1. Registrar venta por cada producto (Se eliminó "vend")
        nuevo_id = f"#{len(self.sales_history) + 1}"
        for item in self.cart:
            self.sales_history.insert(0, { 
                "id": nuevo_id,
                "prod": item["prod"],
                "cant": item["cant"],
                "total": item["precio"] * item["cant"],
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            # 2. Descontar stock del inventario
            for p in self.inventory:
                if p["id"] == item["id"]:
                    p["stock"] -= item["cant"]

        # 3. Actualizar tablas e interfaz
        self.update_inventory_table()
        self.filter_sales() 
        
        messagebox.showinfo("Éxito", f"Venta completada con éxito. Total: ${total:.2f}")
        self.ns_win.destroy()

    # ==========================================
    #       UTILIDADES Y FILTROS LÓGICA
    # ==========================================
    def create_metric_card(self, col, title, value, icon, icon_color="#6366f1"):
        card = ctk.CTkFrame(self.metrics_frame, fg_color="#2b2b2b", corner_radius=10)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        ctk.CTkLabel(card, text=title, text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15, pady=(10, 0))
        ctk.CTkLabel(card, text=value, text_color="white", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=15, pady=(0, 10))

    def update_inventory_table(self):
        for item in self.tree_inv.get_children(): self.tree_inv.delete(item)
        for p in self.inventory:
            self.tree_inv.insert("", "end", values=(p["id"], p["prod"], p["marca"], p["cat"], p["stock"], f"${p['precio']:.2f}"))

    def filter_sales(self, *args):
        # Se solucionó el error de sintaxis que tenías aquí
        term = self.search_sale_var.get().lower() 
        mes = self.month_filter_var.get()

        for item in self.tree_sales.get_children(): self.tree_sales.delete(item)
        
        count = 0
        for s in self.sales_history:
            # Lógica de filtros
            match_term = term in s["prod"].lower()
            
            # Lógica de fecha simple
            match_mes = True
            if mes == "marzo de 2026": match_mes = "-03-" in s["fecha"]
            elif mes == "febrero de 2026": match_mes = "-02-" in s["fecha"]

            # Eliminado match_vendedor
            if match_term and match_mes:
                # La inserción ya no pasa el argumento 'vendedor'
                self.tree_sales.insert("", "end", values=(s["id"], s["prod"], s["cant"], f"${s['total']:.2f}", s["fecha"]))
                count += 1
                
        self.lbl_sales_count.configure(text=f"Mostrando {count} de {len(self.sales_history)} ventas")

    def update_sales_table(self):
        self.filter_sales()

    def clear_sales_filters(self):
        self.search_sale_var.set("")
        self.month_filter_var.set("Todos los meses")
        self.filter_sales()

    # Métodos heredados del original...
    def open_add_window(self):
        pass 
        
    def delete_product(self):
        pass 

if __name__ == "__main__":
    app = PharmacyApp()
    app.mainloop()