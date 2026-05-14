import customtkinter as ctk  # Librería para una interfaz moderna (botones redondeados, modo oscuro, etc.)
from tkinter import ttk, messagebox  # ttk para la tabla (Treeview) y messagebox para alertas emergentes

# --- CONFIGURACIÓN GLOBAL ---
# Establece el tema oscuro y el color principal (azul) para toda la aplicación
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class PharmacyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana principal
        self.title("Sistema de Gestión de Farmacia - Panel Administrativo")
        self.geometry("1000x700")

        # --- BASE DE DATOS SIMULADA ---
        # Lista de diccionarios que actúa como memoria temporal (mientras la app esté abierta)
        self.inventory = [
            {"id": 1, "prod": "Paracetamol", "marca": "Genérico", "cat": "Analgésico", "stock": 150, "costo": 0.50, "precio": 1.50},
            {"id": 2, "prod": "Loratadina 10mg", "marca": "Ultra-Health", "cat": "Antihistamínico", "stock": 5, "costo": 1.20, "precio": 3.00},
            {"id": 3, "prod": "Ibuprofeno", "marca": "Bayer", "cat": "Antiinflamatorio", "stock": 85, "costo": 2.00, "precio": 4.50},
        ]

        # Llamada al método que construye la interfaz gráfica
        self.setup_ui()

    def setup_ui(self):
        """Define la estructura visual y distribución de los elementos (widgets)"""
        
        # Configuración del sistema de rejilla (Grid) para que la app sea responsiva
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # --- 1. TARJETAS DE MÉTRICAS (Indicadores superiores) ---
        # Contenedor para los cuadros de resumen
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.metrics_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Creación de 4 tarjetas usando la función auxiliar 'create_metric_card'
        self.create_metric_card(0, "Productos", "5", "📦")
        self.create_metric_card(1, "Ventas Hoy", "$215.00", "💰")
        self.create_metric_card(2, "Ganancia Potencial", "$2442.50", "📈")
        self.create_metric_card(3, "Stock Bajo", "1", "⚠️", icon_color="#e67e22")

        # --- 2. BANNER DE ALERTA ---
        # Cuadro de color llamativo para avisar sobre productos agotándose
        self.alert_frame = ctk.CTkFrame(self, fg_color="#fff4e6", border_color="#d97706", border_width=1)
        self.alert_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        alert_label = ctk.CTkLabel(self.alert_frame, text="⚠️ Alertas de Stock Bajo: Loratadina 10mg necesitan reabastecimiento.", 
                                  text_color="#d97706", font=ctk.CTkFont(size=13, weight="bold"))
        alert_label.pack(side="left", padx=15, pady=10)

        # --- 3. PANEL DE PESTAÑAS (Tabview) ---
        # Permite organizar la app en secciones (Inventario, Ventas, etc.)
        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#6366f1")
        self.tabview.grid(row=2, column=0, padx=20, pady=0, sticky="nsew")
        self.tabview.add("Inventario")
        self.tabview.add("Ventas")
        self.tabview.add("Recetas")
        self.tabview.set("Inventario") # Pestaña por defecto

        # --- 4. BARRA DE HERRAMIENTAS DE INVENTARIO ---
        self.inventory_tab = self.tabview.tab("Inventario")
        self.inventory_tab.grid_columnconfigure(0, weight=1)

        tool_frame = ctk.CTkFrame(self.inventory_tab, fg_color="transparent")
        tool_frame.pack(fill="x", padx=10, pady=10)

        # Buscador
        self.search_entry = ctk.CTkEntry(tool_frame, placeholder_text="Buscar medicamento...", width=350)
        self.search_entry.pack(side="left", padx=(0, 10))

        # Botón para añadir (abre ventana nueva)
        self.btn_new = ctk.CTkButton(tool_frame, text="+ Nuevo Producto", fg_color="#6366f1", 
                                     hover_color="#4f46e5", command=self.open_add_window)
        self.btn_new.pack(side="right", padx=5)

        # Botón para borrar el elemento seleccionado en la tabla
        self.btn_delete = ctk.CTkButton(tool_frame, text="Eliminar Seleccionado", fg_color="#ef4444", 
                                        hover_color="#dc2626", command=self.delete_product)
        self.btn_delete.pack(side="right", padx=5)

        # --- 5. TABLA DE DATOS (Treeview) ---
        # Como CustomTkinter no tiene tabla oficial, adaptamos la de Tkinter estándar con estilos
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=30, fieldbackground="white", borderwidth=0)
        style.map("Treeview", background=[('selected', '#6366f1')]) # Color al seleccionar fila

        self.tree = ttk.Treeview(self.inventory_tab, columns=("ID", "Producto", "Marca", "Categoría", "Stock", "Costo", "Precio"), show="headings")
        
        # Define los nombres de las columnas y su alineación
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Carga los datos iniciales de la lista 'self.inventory' a la tabla visual
        self.update_table()

    # --- MÉTODOS DE LÓGICA Y FUNCIONALIDAD ---

    def create_metric_card(self, col, title, value, icon, icon_color="#6366f1"):
        """Crea un pequeño cuadro informativo (Widget reutilizable)"""
        card = ctk.CTkFrame(self.metrics_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#f0f0f0")
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        
        lbl_title = ctk.CTkLabel(card, text=title, text_color="gray", font=ctk.CTkFont(size=12))
        lbl_title.pack(anchor="w", padx=15, pady=(10, 0))
        
        lbl_val = ctk.CTkLabel(card, text=value, text_color="black", font=ctk.CTkFont(size=22, weight="bold"))
        lbl_val.pack(anchor="w", padx=15, pady=(0, 10))

    def update_table(self):
        """Refresca visualmente la tabla con los datos actuales de la lista de inventario"""
        # Elimina todo lo que hay en la tabla actualmente
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Recorre la 'base de datos' y los inserta de nuevo
        for p in self.inventory:
            self.tree.insert("", "end", values=(p["id"], p["prod"], p["marca"], p["cat"], p["stock"], f"${p['costo']:.2f}", f"${p['precio']:.2f}"))

    def delete_product(self):
        """Elimina el producto seleccionado en la tabla"""
        selected_item = self.tree.selection() # Obtiene el ID visual de la fila
        if not selected_item:
            messagebox.showwarning("Atención", "Por favor, selecciona un producto para eliminar.")
            return
        
        # Obtiene los valores de la fila y filtra la lista para quitar ese ID
        item_values = self.tree.item(selected_item)['values']
        self.inventory = [p for p in self.inventory if p["id"] != item_values[0]]
        
        self.update_table() # Actualiza la vista
        messagebox.showinfo("Éxito", "Producto eliminado correctamente.")

    def open_add_window(self):
        """Abre una ventana secundaria (Pop-up) para ingresar datos de un nuevo producto"""
        self.add_win = ctk.CTkToplevel(self)
        self.add_win.title("Agregar Nuevo Producto")
        self.add_win.geometry("400x500")
        self.add_win.attributes("-topmost", True) # Asegura que esté al frente

        # Campos de entrada (Labels y Entrys)
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

        # Botón para confirmar el guardado
        ctk.CTkButton(self.add_win, text="Guardar", command=self.save_new_product).pack(pady=30)

    def save_new_product(self):
        """Toma los datos de la ventana emergente y los guarda en la lista principal"""
        try:
            # Genera un ID nuevo sumando 1 al último existente
            new_id = self.inventory[-1]["id"] + 1 if self.inventory else 1
            
            # Crea el nuevo diccionario de producto
            new_item = {
                "id": new_id,
                "prod": self.e_nome.get(),
                "marca": self.e_marca.get(),
                "cat": "General",
                "stock": int(self.e_stock.get()), # Convierte a número entero
                "costo": 0.0,
                "precio": float(self.e_precio.get()) # Convierte a número decimal
            }
            
            self.inventory.append(new_item) # Lo añade a la "base de datos"
            self.update_table() # Refresca la tabla principal
            self.add_win.destroy() # Cierra la ventana emergente
        except ValueError:
            # Error si el usuario pone letras en campos numéricos (Stock/Precio)
            messagebox.showerror("Error", "Asegúrate de que Stock y Precio sean números válidos.")

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    app = PharmacyApp() # Instancia la clase
    app.mainloop()      # Inicia el bucle de eventos (mantiene la ventana abierta)