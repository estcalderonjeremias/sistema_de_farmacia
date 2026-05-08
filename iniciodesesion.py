import customtkinter as ctk  # Importamos la librería para la interfaz moderna
import tkinter as tk
from tkinter import messagebox  # Importamos el módulo para ventanas emergentes (alertas)
import os
from PIL import Image, ImageTk # Importamos PIL para manejo avanzado de imágenes


# --- CONFIGURACIÓN GLOBAL ---
# Establece el modo oscuro (puedes cambiar "dark" por "light")
ctk.set_appearance_mode("dark")  
# Establece el color de los botones y acentos (azul por defecto)
ctk.set_default_color_theme("blue")  

# --- DEFINICIÓN DE LA CLASE PRINCIPAL ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()  # Inicializa la configuración de la ventana padre (CTk)

        # Configuración básica de la ventana
        self.title("Sistema de Acceso")  # Texto que aparece en la barra superior
        self.geometry("400x550")        # Aumentar un poco la altura para la imagen

        # Configuración del sistema de cuadrícula (Grid)
        # Esto asegura que los elementos se mantengan centrados
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- CREACIÓN DEL CONTENEDOR (FRAME) ---
        
        # El Frame es como una "tarjeta" que agrupa los elementos internos
        self.main_frame = ctk.CTkFrame(self, corner_radius=15) # Esquinas redondeadas de 15px
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # --- AGREGAR LA IMAGEN ---
        # 1. Cargar la imagen con PIL
        # REEMPLAZA "logo_farmacia.png" CON TU ARCHIVO DE IMAGEN
        ruta_imagen = "marca.png"
        
        # DEMO: Lógica para crear una imagen de demostración si no existe tu archivo
        if not os.path.exists(ruta_imagen):
             print(f"Advertencia: No se encontró la imagen '{ruta_imagen}'. Usando una imagen de demostración.")
             # Crear una imagen azul de demostración de 100x100
             pil_image_for_logo = Image.new('RGB', (100, 100), color = (0, 120, 215)) # Color azul ctk
        else:
             # Cargar con PIL
             try:
                 pil_image_for_logo = Image.open(ruta_imagen)
                 # Redimensionar la imagen si es necesario
                 pil_image_for_logo = pil_image_for_logo.resize((300, 50)) # Tamaño de 100x100
             except Exception as e:
                 print(f"Error cargando imagen: {e}")
                 pil_image_for_logo = Image.new('RGB', (100, 100), color = 'red') # Imagen de error

        # 2. Convertir a un formato CTkImage
        # Esto es necesario para que ctk lo maneje correctamente
        self.logo_image = ctk.CTkImage(
            light_image=pil_image_for_logo, 
            dark_image=pil_image_for_logo, 
            size=(250, 100) # Tamaño de visualización
        )

        # 3. Crear el widget de imagen y colocarlo arriba
        self.image_label = ctk.CTkLabel(
            self.main_frame, 
            image=self.logo_image, 
            text="" # Sin texto para que solo sea imagen
        )
        # pack() con un poco de margen superior e inferior
        self.image_label.pack(pady=(30, 10)) 

        # --- ETIQUETA DE TÍTULO PRINCIPAL ---
        # Código original: self.label = ctk.CTkLabel(..., pady=(40, 20))
        # Ahora ajustamos el pady para que esté cerca de la imagen
        self.label_titulo = ctk.CTkLabel(
            self.main_frame, 
            text="Sistema de Farmacia", 
            font=ctk.CTkFont(size=24, weight="bold") # Fuente grande y en negrita
        )
        self.label_titulo.pack(pady=(0, 20)) # Margen superior 0, inferior 20

        # --- ETIQUETA DE TÍTULO DE INICIO ---
        self.label_iniciar = ctk.CTkLabel(
            self.main_frame, 
            text="Iniciar Sesión para continuar", 
            font=ctk.CTkFont(size=13, weight="bold") # Fuente grande y en negrita
        )
        self.label_iniciar.pack(pady=(10, 5)) 
        
        # --- CAMPO DE TEXTO: USUARIO ---
        self.mail_entry = ctk.CTkEntry(
            self.main_frame, 
            width=250, 
            placeholder_text="email" # Texto que desaparece al escribir
        )
        self.mail_entry.pack(pady=10) # Espaciado vertical entre elementos

        # --- CAMPO DE TEXTO: CONTRASEÑA ---
        self.pass_entry = ctk.CTkEntry(
            self.main_frame, 
            width=250, 
            placeholder_text="Contraseña", 
            show="*" # Oculta los caracteres con asteriscos por seguridad
        )
        self.pass_entry.pack(pady=10)

        # --- BOTÓN DE ENTRADA ---
        self.login_button = ctk.CTkButton(
            self.main_frame, 
            text="Entrar", 
            command=self.login_event, # Llama a la función 'login_event' al hacer clic
            width=250
        )
        self.login_button.pack(pady=(30, 20)) # Margen inferior para el final



    # --- LÓGICA DE VALIDACIÓN (sin cambios) ---
    def login_event(self):
        # .get() extrae el texto actual que el usuario escribió en los campos
        email = self.mail_entry.get()
        password = self.pass_entry.get()
        
        # Validación condicional: Comparamos con datos fijos (hardcoded)
        if email == "admin@farmacia.com" and password == "1234":
            # Si coinciden, muestra ventana de información (icono azul)
            self.destroy()
            messagebox.showinfo("Éxito", f"Bienvenido de nuevo, {email}")
            # Descomenta la siguiente línea para ejecutar tu otra pantalla
            os.system('python pantallaprincipal.py')
            
           
            
        elif "@" not in email or email not in ".com":
            messagebox.showinfo("Error", f"campo de email sin @ o .com")
        else:
            # Si fallan, muestra ventana de error (icono rojo)
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# --- PUNTO DE ENTRADA DEL PROGRAMA ---
if __name__ == "__main__":
    app = App()       # Creamos la instancia de nuestra clase
    app.mainloop()    # Iniciamos el bucle para que la ventana no se cierre