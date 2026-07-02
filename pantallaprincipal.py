import customtkinter as ctk
from tkinter import ttk

from inventario import InventarioMixin
from estadisticas import EstadisticasMixin
from ventas import VentasMixin
import sqlite3
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

conn = sqlite3.connect("labase.db")
cur = conn.cursor()
class PharmacyApp(ctk.CTk, InventarioMixin, VentasMixin, EstadisticasMixin):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestion de Farmacia - Panel Administrativo")
        self.geometry("1100x750")

        self.inventory = []
        self.load_inventory_from_db()

        self.sales_history = []
        self.load_sales_from_db()

        self.cart = []
        self.low_stock_limit = 5
        self.metric_values = {}
 
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.create_metric_card(0, "Productos", str(len(self.inventory)), value_key="products")
        self.create_metric_card(1, "Ventas Totales", f"${sum(s['total'] for s in self.sales_history):.2f}", value_key="sales_total")
        self.create_metric_card(2, "Ganancia Potencial", self.calculate_potential_profit(), value_key="profit")
        self.create_metric_card(3, "Stock Bajo", "0", value_key="low_stock")

        self.alert_frame = ctk.CTkFrame(self, fg_color="#fff4e6", border_color="#d97706", border_width=1)
        self.alert_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.alert_label = ctk.CTkLabel(self.alert_frame, text="", text_color="#d97706", font=ctk.CTkFont(size=13, weight="bold"))
        self.alert_label.pack(side="left", padx=15, pady=10)

        self.tabview = ctk.CTkTabview(self, segmented_button_selected_color="#6366f1")
        self.tabview.grid(row=2, column=0, padx=20, pady=0, sticky="nsew", rowspan=3)
        self.tabview.add("Inventario")
        self.tabview.add("Ventas")
        
        self.role = sys.argv[1] if len(sys.argv) > 1 else "admin"

        if self.role != "empleado":
            self.tabview.add("Estadisticas")

        self.setup_treeview_style()
        self.build_inventory_tab()
        self.build_sales_tab()
        
        
        if self.role != "empleado":
            self.build_stats_tab()

        self.update_metric_cards()
        self.update_stock_alert()
        self.tabview.set("Ventas")

    def setup_treeview_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=35, fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#3f3f3f", foreground="white", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#6366f1")])

    def create_metric_card(self, col, title, value, value_key=None):
        card = ctk.CTkFrame(self.metrics_frame, fg_color="#2b2b2b", corner_radius=10)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        ctk.CTkLabel(card, text=title, text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15, pady=(10, 0))
        value_label = ctk.CTkLabel(card, text=value, text_color="white", font=ctk.CTkFont(size=22, weight="bold"))
        value_label.pack(anchor="w", padx=15, pady=(0, 10))
        if value_key:
            self.metric_values[value_key] = value_label

    def calculate_potential_profit(self):
        total = sum((p["precio"] - p["costo"]) * p["stock"] for p in self.inventory)
        return f"${total:.2f}"

    def update_metric_cards(self):
        if "products" in self.metric_values:
            self.metric_values["products"].configure(text=str(len(self.inventory)))
        if "sales_total" in self.metric_values:
            self.metric_values["sales_total"].configure(text=f"${sum(s['total'] for s in self.sales_history):.2f}")
        if "profit" in self.metric_values:
            self.metric_values["profit"].configure(text=self.calculate_potential_profit())

    def update_stock_alert(self):
        low_stock_products = [p for p in self.inventory if p["stock"] <= self.low_stock_limit]

        if "low_stock" in self.metric_values:
            self.metric_values["low_stock"].configure(text=str(len(low_stock_products)))

        if not low_stock_products:
            self.alert_frame.grid_remove()
            return

        product_names = ", ".join(p["prod"] for p in low_stock_products)
        self.alert_label.configure(text=f"Alertas de Stock Bajo: {product_names} necesitan reabastecimiento.")
        self.alert_frame.grid()


if __name__ == "__main__":
    app = PharmacyApp()
    app.mainloop()
