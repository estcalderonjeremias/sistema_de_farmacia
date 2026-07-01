import customtkinter as ctk  # Importamos la librería para la interfaz moderna
import tkinter as tk
from tkinter import messagebox  # Importamos el módulo para ventanas emergentes (alertas)
import os
import subprocess
import sys
import sqlite3
from PIL import Image, ImageTk # Importamos PIL para manejo avanzado de imágenes

conn = sqlite3.connect("labase.db")
cur = conn.cursor()
# --- CONFIGURACIÓN GLOBAL ---
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")  

# --- DEFINICIÓN DE LA CLASE PRINCIPAL ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()  # Inicializa la configuración de la ventana padre (CTk)

        # Configuración básica de la ventana
        self.title("Inicio de Sesión")  # Texto que aparece en la barra superior
        self.geometry("400x550")        # Aumentar un poco la altura para la imagen
        self.resizable(False, False)    # Evita que se deforme el fondo al estirar la ventana

        # Configuración del sistema de cuadrícula (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # --- NUEVO: AGREGAR IMAGEN DE FONDO ---
        # ==========================================
        # PON AQUÍ LA DIRECCIÓN DE TU FOTO DE FONDO
        ruta_fondo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes", "fondo.png")
        
        if not os.path.exists(ruta_fondo):
            print(f"Advertencia: No se encontró el fondo '{ruta_fondo}'. Usando fondo gris de demo.")
            pil_fondo = Image.new('RGB', (400, 550), color = (220, 220, 220))
        else:
            pil_fondo = Image.open(ruta_fondo)

        # Convertir a CTkImage adaptada al tamaño de la ventana
        self.imagen_fondo_ctk = ctk.CTkImage(
            light_image=pil_fondo,
            dark_image=pil_fondo,
            size=(800, 750)
        )

        # Crear el Label del fondo y posicionarlo para que ocupe TODO
        self.label_fondo = ctk.CTkLabel(self, image=self.imagen_fondo_ctk, text="")
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        # ==========================================

        # --- CREACIÓN DEL CONTENEDOR (FRAME) ---
        # Añadimos fg_color para controlar el color del cuadro blanco del login
        # Puedes usar "white" o un tono grisáceo para que contraste con tu fondo
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#F0F0F0") 
        self.main_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

        # --- AGREGAR LA IMAGEN DE LOGO ---
        ruta_imagen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes", "logoo.png")
        
        if not os.path.exists(ruta_imagen):
             print(f"Advertencia: No se encontró la imagen '{ruta_imagen}'. Usando una imagen de demostración.")
             pil_image_for_logo = Image.new('RGB', (100, 100), color = (0, 120, 215)) 
        else:
             try:
                 pil_image_for_logo = Image.open(ruta_imagen)
                 pil_image_for_logo = pil_image_for_logo.resize((300, 50)) 
             except Exception as e:
                 print(f"Error cargando imagen: {e}")
                 pil_image_for_logo = Image.new('RGB', (100, 100), color = 'red') 

        self.logo_image = ctk.CTkImage(
            light_image=pil_image_for_logo, 
            dark_image=pil_image_for_logo, 
            size=(250, 100) 
        )

        self.image_label = ctk.CTkLabel(
            self.main_frame, 
            image=self.logo_image, 
            text="" 
        )
        self.image_label.pack(pady=(20, 10)) 

        # --- ETIQUETA DE TÍTULO PRINCIPAL ---
      
        # --- ETIQUETA DE TÍTULO DE INICIO ---
        self.label_iniciar = ctk.CTkLabel(
            self.main_frame, 
            text="Iniciar Sesión para continuar", 
            font=ctk.CTkFont(size=13, weight="bold") 
        )
        self.label_iniciar.pack(pady=(5, 5)) 
        
        # --- CAMPO DE TEXTO: USUARIO ---   
        self.mail_entry = ctk.CTkEntry(
            self.main_frame, 
            width=250, 
            placeholder_text="Email" 
        )
        self.mail_entry.pack(pady=10) 

        # --- CAMPO DE TEXTO: CONTRASEÑA ---
        self.pass_entry = ctk.CTkEntry(
            self.main_frame, 
            width=250, 
            placeholder_text="Contraseña", 
            show="*" 
        )
        self.pass_entry.pack(pady=10)

        # --- BOTÓN DE ENTRADA ---
        self.login_button = ctk.CTkButton(
            self.main_frame, 
            text="Entrar", 
            command=self.login_event, 
            width=250
        )
        self.login_button.pack(pady=(25, 20)) 


    # --- LÓGICA DE VALIDACIÓN ---
    def login_event(self):
        email = self.mail_entry.get()
        password = self.pass_entry.get()
        
        if email == "admin@farmacia.com" and password == "1234":
            messagebox.showinfo("Éxito", f"Bienvenido Administrador")
            subprocess.Popen(
                [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pantallaprincipal.py"), "admin"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            self.destroy()
            
        elif email == "empleado@farmacia.com" and password == "1234":
            messagebox.showinfo("Éxito", f"Bienvenido Empleado")
            subprocess.Popen(
                [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pantallaprincipal.py"), "empleado"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            self.destroy()
            
        elif "@" not in email or ".com" not in email:
            messagebox.showinfo("Error", f"campo de email sin @ o .com")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # --- PUNTO DE ENTRADA DEL PROGRAMA ---
if __name__ == "__main__":
    app = App()       
    app.mainloop()
