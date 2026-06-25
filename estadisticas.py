from collections import defaultdict
from datetime import datetime, timedelta
import tkinter as tk

import customtkinter as ctk


class EstadisticasMixin:
    MONTH_NAMES = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
    }

    def build_stats_tab(self):
        self.stats_tab = self.tabview.tab("Estadisticas")
        self.stats_tab.grid_columnconfigure(0, weight=1)

        self.stats_month_var = ctk.StringVar(value="Todos los meses")
        self.stats_employee_var = ctk.StringVar(value="Todos los empleados")

        self.stats_scroll = ctk.CTkScrollableFrame(self.stats_tab, fg_color="transparent")
        self.stats_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self.stats_scroll.grid_columnconfigure((0, 1), weight=1)

        header = ctk.CTkFrame(self.stats_scroll, fg_color="#4f46e5", corner_radius=8)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        ctk.CTkLabel(header, text="Analisis de Ventas", text_color="white", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=16, pady=(12, 0))
        ctk.CTkLabel(header, text="Reportes y estadisticas detalladas", text_color="#e0e7ff").pack(anchor="w", padx=16, pady=(0, 12))

        filters = ctk.CTkFrame(self.stats_scroll, fg_color="#2b2b2b", corner_radius=8)
        filters.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        filters.grid_columnconfigure((0, 1, 2), weight=1)

        self._build_filter(filters, 0, "Mes", self.stats_month_var, self.get_stats_month_options())
        self._build_filter(filters, 1, "Empleado", self.stats_employee_var, self.get_stats_employee_options())
        ctk.CTkButton(filters, text="Limpiar Filtros", fg_color="#6b7280", hover_color="#4b5563", command=self.clear_stats_filters).grid(row=1, column=2, sticky="ew", padx=12, pady=(0, 12))

        cards = ctk.CTkFrame(self.stats_scroll, fg_color="transparent")
        cards.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        cards.grid_columnconfigure((0, 1, 2), weight=1)

        self.stats_income_value = self._build_stat_card(cards, 0, "Ingresos Totales", "$0.00", "#052e16", "#22c55e")
        self.stats_transactions_value = self._build_stat_card(cards, 1, "Transacciones", "0", "#172554", "#3b82f6")
        self.stats_ticket_value = self._build_stat_card(cards, 2, "Ticket Promedio", "$0.00", "#3b0764", "#a855f7")

        self.daily_canvas = self._build_chart_card("Ventas Diarias", 3, 0)
        self.monthly_canvas = self._build_chart_card("Ventas Mensuales", 3, 1)
        self.employee_canvas = self._build_chart_card("Ventas por Empleado", 4, 0)
        self.products_canvas = self._build_chart_card("Top 5 Productos Mas Vendidos", 4, 1)

        self.update_stats_dashboard()

    def _build_filter(self, parent, col, label, variable, values):
        ctk.CTkLabel(parent, text=label, text_color="gray").grid(row=0, column=col, sticky="w", padx=12, pady=(12, 2))
        combo = ctk.CTkComboBox(parent, values=values, variable=variable, command=lambda _: self.update_stats_dashboard())
        combo.grid(row=1, column=col, sticky="ew", padx=12, pady=(0, 12))

    def _build_stat_card(self, parent, col, title, value, bg_color, accent):
        card = ctk.CTkFrame(parent, fg_color=bg_color, border_color=accent, border_width=1, corner_radius=8)
        card.grid(row=0, column=col, sticky="ew", padx=6)
        ctk.CTkLabel(card, text=title, text_color=accent, font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=14, pady=(12, 2))
        value_label = ctk.CTkLabel(card, text=value, text_color="white", font=ctk.CTkFont(size=24, weight="bold"))
        value_label.pack(anchor="w", padx=14, pady=(0, 12))
        return value_label

    def _build_chart_card(self, title, row, col):
        card = ctk.CTkFrame(self.stats_scroll, fg_color="#2b2b2b", corner_radius=8)
        card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))
        canvas = tk.Canvas(card, height=230, bg="#2b2b2b", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        return canvas

    def get_stats_month_options(self):
        months = []
        for sale in self.sales_history:
            date = self._parse_sale_date(sale["fecha"])
            if date:
                months.append(f"{self.MONTH_NAMES[date.month]} {date.year}")
        return ["Todos los meses"] + sorted(set(months), reverse=True)

    def get_stats_employee_options(self):
        employees = sorted({sale.get("empleado", "Empleado") for sale in self.sales_history})
        return ["Todos los empleados"] + employees

    def get_filtered_stats_sales(self):
        month = self.stats_month_var.get()
        employee = self.stats_employee_var.get()
        filtered = []
        for sale in self.sales_history:
            date = self._parse_sale_date(sale["fecha"])
            sale_month = f"{self.MONTH_NAMES[date.month]} {date.year}" if date else ""
            sale_employee = sale.get("empleado", "Empleado")
            if month != "Todos los meses" and sale_month != month:
                continue
            if employee != "Todos los empleados" and sale_employee != employee:
                continue
            filtered.append(sale)
        return filtered

    def update_stats_dashboard(self):
        if not hasattr(self, "stats_income_value"):
            return

        sales = self.get_filtered_stats_sales()
        total = sum(sale["total"] for sale in sales)
        ticket = total / len(sales) if sales else 0

        self.stats_income_value.configure(text=f"${total:.2f}")
        self.stats_transactions_value.configure(text=str(len(sales)))
        self.stats_ticket_value.configure(text=f"${ticket:.2f}")

        self.draw_line_chart(self.daily_canvas, self.get_daily_totals(sales), "#6366f1")
        self.draw_bar_chart(self.monthly_canvas, self.get_monthly_totals(sales), "#4f46e5")
        self.draw_bar_chart(self.employee_canvas, self.get_employee_totals(sales), "#06b6d4")
        self.draw_bar_chart(self.products_canvas, self.get_product_totals(sales), "#10b981", horizontal=True)

    def clear_stats_filters(self):
        self.stats_month_var.set("Todos los meses")
        self.stats_employee_var.set("Todos los empleados")
        self.update_stats_dashboard()

    def get_daily_totals(self, sales):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=29)
        totals = defaultdict(float)
        for sale in sales:
            date = self._parse_sale_date(sale["fecha"])
            if date and start_date <= date.date() <= end_date:
                totals[date.strftime("%d/%m")] += sale["total"]
        return [(day.strftime("%d/%m"), totals[day.strftime("%d/%m")]) for day in (start_date + timedelta(days=i) for i in range(30))]

    def get_monthly_totals(self, sales):
        totals = defaultdict(float)
        for sale in sales:
            date = self._parse_sale_date(sale["fecha"])
            if date:
                totals[date.strftime("%m/%Y")] += sale["total"]
        return sorted(totals.items())

    def get_employee_totals(self, sales):
        totals = defaultdict(float)
        for sale in sales:
            totals[sale.get("empleado", "Empleado")] += sale["total"]
        return sorted(totals.items(), key=lambda item: item[1], reverse=True)

    def get_product_totals(self, sales):
        totals = defaultdict(float)
        for sale in sales:
            totals[sale["prod"]] += sale["cant"]
        return sorted(totals.items(), key=lambda item: item[1], reverse=True)[:5]

    def draw_line_chart(self, canvas, data, color):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 320)
        height = 230
        margin = 34
        self._draw_empty_chart(canvas, data, width, height)
        if not data or max(value for _, value in data) == 0:
            return

        max_value = max(value for _, value in data)
        points = []
        for index, (_, value) in enumerate(data):
            x = margin + index * ((width - margin * 2) / max(len(data) - 1, 1))
            y = height - margin - (value / max_value) * (height - margin * 2)
            points.append((x, y))

        for idx in range(len(points) - 1):
            canvas.create_line(*points[idx], *points[idx + 1], fill=color, width=2)
        for x, y in points[:: max(len(points) // 8, 1)]:
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline=color)

    def draw_bar_chart(self, canvas, data, color, horizontal=False):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 320)
        height = 230
        margin = 42
        self._draw_empty_chart(canvas, data, width, height)
        if not data:
            return

        max_value = max(value for _, value in data) or 1
        if horizontal:
            bar_height = max(16, (height - margin * 2) / max(len(data), 1) - 8)
            for index, (label, value) in enumerate(data):
                y = margin + index * (bar_height + 8)
                bar_width = (value / max_value) * (width - margin * 2 - 80)
                canvas.create_text(margin, y + bar_height / 2, text=label[:18], fill="#e5e7eb", anchor="w", font=("Arial", 8))
                canvas.create_rectangle(margin + 100, y, margin + 100 + bar_width, y + bar_height, fill=color, outline="")
                canvas.create_text(margin + 106 + bar_width, y + bar_height / 2, text=f"{value:.0f}", fill="#e5e7eb", anchor="w", font=("Arial", 8))
            return

        bar_width = max(24, (width - margin * 2) / max(len(data), 1) - 20)
        for index, (label, value) in enumerate(data):
            x = margin + index * (bar_width + 20) + 10
            bar_height = (value / max_value) * (height - margin * 2)
            y = height - margin - bar_height
            canvas.create_rectangle(x, y, x + bar_width, height - margin, fill=color, outline="")
            canvas.create_text(x + bar_width / 2, height - 18, text=label, fill="#e5e7eb", font=("Arial", 8))
            canvas.create_text(x + bar_width / 2, y - 8, text=f"${value:.0f}", fill="#e5e7eb", font=("Arial", 8))

    def _draw_empty_chart(self, canvas, data, width, height):
        margin = 34
        for line in range(4):
            y = margin + line * ((height - margin * 2) / 3)
            canvas.create_line(margin, y, width - margin, y, fill="#3f3f46", dash=(2, 3))
        canvas.create_line(margin, height - margin, width - margin, height - margin, fill="#52525b")
        if not data:
            canvas.create_text(width / 2, height / 2, text="Sin datos para mostrar", fill="#9ca3af", font=("Arial", 12, "bold"))

    def _parse_sale_date(self, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            return None
