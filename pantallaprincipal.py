import customtkinter as ctk
from tkinter import ttk

from inventario import InventarioMixin
from recetas import RecetasMixin
from ventas import VentasMixin
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

conn = sqlite3.connect("labase.db")
cur = conn.cursor()
class PharmacyApp(ctk.CTk, InventarioMixin, VentasMixin, RecetasMixin):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestion de Farmacia - Panel Administrativo")
        self.geometry("1100x750")

        self.inventory = [
            {"id": 1, "prod": "Paracetamol 500mg", "marca": "Bayer", "cat": "Analgesico", "prov": "Drogueria Sur", "stock": 150, "costo": 0.50, "precio": 5.50},
            {"id": 2, "prod": "Loratadina 10mg", "marca": "Ultra-Health", "cat": "Antihistaminico", "prov": "Farmacity Dist", "stock": 5, "costo": 1.20, "precio": 3.00},
            {"id": 3, "prod": "Ibuprofeno 400mg", "marca": "Pfizer", "cat": "Antiinflamatorio", "prov": "Farmacity Dist", "stock": 85, "costo": 2.00, "precio": 7.00},
            {"id": 4, "prod": "Amoxicilina 500mg", "marca": "GlaxoSmithKline", "cat": "Antibiotico", "prov": "Drogueria Sur", "stock": 80, "costo": 5.00, "precio": 12.50},
            {"id": 5, "prod": "Omeprazol 20mg", "marca": "Generico", "cat": "Gastrico", "prov": "Medistore", "stock": 40, "costo": 8.00, "precio": 16.00},
            {"id": 6, "prod": "Aspirina 100mg", "marca": "Bayer", "cat": "Antiagregante", "prov": "Drogueria Sur", "stock": 120, "costo": 1.10, "precio": 3.80},
            {"id": 7, "prod": "Diclofenac 50mg", "marca": "Novartis", "cat": "Antiinflamatorio", "prov": "Medistore", "stock": 70, "costo": 1.80, "precio": 6.20},
            {"id": 8, "prod": "Cetirizina 10mg", "marca": "Generico", "cat": "Antihistaminico", "prov": "Farmacity Dist", "stock": 35, "costo": 1.00, "precio": 3.50},
            {"id": 9, "prod": "Salbutamol Inhalador", "marca": "GlaxoSmithKline", "cat": "Respiratorio", "prov": "Drogueria Norte", "stock": 18, "costo": 6.50, "precio": 14.00},
            {"id": 10, "prod": "Metformina 850mg", "marca": "Roemmers", "cat": "Antidiabetico", "prov": "Medistore", "stock": 60, "costo": 3.20, "precio": 8.90},
            {"id": 11, "prod": "Losartan 50mg", "marca": "Bago", "cat": "Antihipertensivo", "prov": "Drogueria Sur", "stock": 55, "costo": 2.70, "precio": 7.50},
            {"id": 12, "prod": "Atorvastatina 20mg", "marca": "Pfizer", "cat": "Cardiovascular", "prov": "Farmacity Dist", "stock": 42, "costo": 4.10, "precio": 10.50},
            {"id": 13, "prod": "Clonazepam 0.5mg", "marca": "Roche", "cat": "Psicotropico", "prov": "Drogueria Norte", "stock": 25, "costo": 2.40, "precio": 6.80},
            {"id": 14, "prod": "Vitamina C 1g", "marca": "Redoxon", "cat": "Suplemento", "prov": "Medistore", "stock": 90, "costo": 1.50, "precio": 4.90},
            {"id": 15, "prod": "Alcohol en Gel 500ml", "marca": "Porta", "cat": "Higiene", "prov": "Drogueria Sur", "stock": 110, "costo": 2.20, "precio": 5.00},
        ]

        self.sales_history = [
            {"id": "#1", "prod": "Paracetamol 500mg", "cant": 2, "total": 11.00, "fecha": "2026-03-15 10:30"},
            {"id": "#2", "prod": "Ibuprofeno 400mg", "cant": 1, "total": 7.00, "fecha": "2026-03-16 11:15"},
            {"id": "#3", "prod": "Amoxicilina 500mg", "cant": 3, "total": 37.50, "fecha": "2026-03-20 14:20"},
            {"id": "#4", "prod": "Omeprazol 20mg", "cant": 2, "total": 32.00, "fecha": "2026-02-25 09:45"},
        ]

        self.cart = []
        self.low_stock_limit = 25
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
        self.tabview.add("Recetas")

        self.setup_treeview_style()
        self.build_inventory_tab()
        self.build_sales_tab()
        self.build_recipes_tab()

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
