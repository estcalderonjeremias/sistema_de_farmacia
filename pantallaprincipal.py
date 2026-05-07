import customtkinter as ctk
from tkinter import ttk, messagebox

# Configuración de apariencia
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class PharmacyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión de Farmacia - Panel Administrativo")
        self.geometry("1000x700")

        # Datos iniciales (Base de datos simulada)
        self.inventory = [
            {"id": 1, "prod": "Paracetamol", "marca": "Genérico", "cat": "Analgésico", "stock": 150, "costo": 0.50, "precio": 1.50},
            {"id": 2, "prod": "Loratadina 10mg", "marca": "Ultra-Health", "cat": "Antihistamínico", "stock": 5, "costo": 1.20, "precio": 3.00},
            {"id": 3, "prod": "Ibuprofeno", "marca": "Bayer", "cat": "Antiinflamatorio", "stock": 85, "costo": 2.00, "precio": 4.50},
        ]

        self.setup_ui()

    def setup_ui(self):
        # --- CONTENEDOR PRINCIPAL ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # --- 1. TARJETAS DE MÉTRICAS (SUPERIOR) ---
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.metrics_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.create_metric_card(0, "Productos", "5", "📦")
        self.create_metric_card(1, "Ventas Hoy", "$215.00", "💰")
        self.create_metric_card(2, "Ganancia Potencial", "$2442.50", "📈")
        self.create_metric_card(3, "Stock Bajo", "1", "⚠️", icon_color="#e67e22")

        # --- 2. ALERTA DE STOCK BAJO ---
        self.alert_frame = ctk.CTkFrame(self, fg_color="#fff4e6", border_color="#d97706", border_width=1)
        self.alert_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        alert_label = ctk.CTkLabel(self.alert_frame, text="⚠️ Alertas de Stock Bajo: Loratadina 10mg necesitan reabastecimiento.", 
                                  text_color="#d97706", font=ctk.CTkFont(size=13, weight="bold"))
        alert_label.pack(side="left", padx=15, pady=10)

        # --- 3. PESTAÑAS (TABS) ---
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#6366f1")
        self.tabview.grid(row=2, column=0, padx=20, pady=0, sticky="nsew")
        self.tabview.add("Inventario")
        self.tabview.add("Ventas")
        self.tabview.add("Recetas")
        self.tabview.set("Inventario")

        # --- 4. BARRA DE HERRAMIENTAS (DENTRO DE INVENTARIO) ---
        self.inventory_tab = self.tabview.tab("Inventario")
        self.inventory_tab.grid_columnconfigure(0, weight=1)

        tool_frame = ctk.CTkFrame(self.inventory_tab, fg_color="transparent")
        tool_frame.pack(fill="x", padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(tool_frame, placeholder_text="Buscar medicamento...", width=350)
        self.search_entry.pack(side="left", padx=(0, 10))

        self.btn_new = ctk.CTkButton(tool_frame, text="+ Nuevo Producto", fg_color="#6366f1", hover_color="#4f46e5", command=self.open_add_window)
        self.btn_new.pack(side="right", padx=5)

        self.btn_delete = ctk.CTkButton(tool_frame, text="Eliminar Seleccionado", fg_color="#ef4444", hover_color="#dc2626", command=self.delete_product)
        self.btn_delete.pack(side="right", padx=5)

        # --- 5. TABLA DE DATOS (TREEVIEW) ---
        # CustomTkinter no tiene tabla nativa aún, usamos ttk.Treeview con estilo
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=30, fieldbackground="white", borderwidth=0)
        style.map("Treeview", background=[('selected', '#6366f1')])

        self.tree = ttk.Treeview(self.inventory_tab, columns=("ID", "Producto", "Marca", "Categoría", "Stock", "Costo", "Precio"), show="headings")
        
        # Encabezados
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.update_table()

    # --- LÓGICA DE FUNCIONAMIENTO ---

    def create_metric_card(self, col, title, value, icon, icon_color="#6366f1"):
        card = ctk.CTkFrame(self.metrics_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#f0f0f0")
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        
        lbl_title = ctk.CTkLabel(card, text=title, text_color="gray", font=ctk.CTkFont(size=12))
        lbl_title.pack(anchor="w", padx=15, pady=(10, 0))
        
        lbl_val = ctk.CTkLabel(card, text=value, text_color="black", font=ctk.CTkFont(size=22, weight="bold"))
        lbl_val.pack(anchor="w", padx=15, pady=(0, 10))

    def update_table(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Llenar con datos
        for p in self.inventory:
            self.tree.insert("", "end", values=(p["id"], p["prod"], p["marca"], p["cat"], p["stock"], f"${p['costo']:.2f}", f"${p['precio']:.2f}"))

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto para eliminar.")
            return
        
        item_values = self.tree.item(selected_item)['values']
        self.inventory = [p for p in self.inventory if p["id"] != item_values[0]]
        self.update_table()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente.")

    def open_add_window(self):
        # Ventana emergente para agregar
        self.add_win = ctk.CTkToplevel(self)
        self.add_win.title("Agregar Nuevo Producto")
        self.add_win.geometry("400x500")
        self.add_win.attributes("-topmost", True)

        ctk.CTkLabel(self.add_win, text="Nombre:").pack(pady=(20,0))
        self.e_nome = ctk.CTkEntry(self.add_win, width=250)
        self.e_nome.pack()

        ctk.CTkLabel(self.add_win, text="Marca:").pack(pady=(10,0))
        self.e_marca = ctk.CTkEntry(self.add_win, width=250)
        self.e_marca.pack()

        ctk.CTkLabel(self.add_win, text="Stock:").pack(pady=(10,0))
        self.e_stock = ctk.CTkEntry(self.add_win, width=250)
        self.e_stock.pack()

        ctk.CTkLabel(self.add_win, text="Precio:").pack(pady=(10,0))
        self.e_precio = ctk.CTkEntry(self.add_win, width=250)
        self.e_precio.pack()

        ctk.CTkButton(self.add_win, text="Guardar", command=self.save_new_product).pack(pady=30)

    def save_new_product(self):
        new_id = self.inventory[-1]["id"] + 1 if self.inventory else 1
        new_item = {
            "id": new_id,
            "prod": self.e_nome.get(),
            "marca": self.e_marca.get(),
            "cat": "General",
            "stock": int(self.e_stock.get()),
            "costo": 0.0,
            "precio": float(self.e_precio.get())
        }
        self.inventory.append(new_item)
        self.update_table()
        self.add_win.destroy()

if __name__ == "__main__":
    app = PharmacyApp()
    app.mainloop()