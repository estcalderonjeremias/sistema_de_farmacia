import customtkinter as ctk  # Importamos la librería para la interfaz moderna
from tkinter import messagebox  # Importamos el módulo para ventanas emergentes (alertas)
import os


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
        self.geometry("400x450")        # Tamaño: 400 píxeles de ancho por 450 de alto

        # Configuración del sistema de cuadrícula (Grid)
        # Esto asegura que los elementos se mantengan centrados
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- CREACIÓN DEL CONTENEDOR (FRAME) ---
        # El Frame es como una "tarjeta" que agrupa los elementos internos
        self.main_frame = ctk.CTkFrame(self, corner_radius=15) # Esquinas redondeadas de 15px
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # --- ETIQUETA DE TÍTULO ---
        self.label = ctk.CTkLabel(
            self.main_frame, 
            text="Iniciar Sesión", 
            font=ctk.CTkFont(size=24, weight="bold") # Fuente grande y en negrita
        )
        self.label.pack(pady=(40, 20)) # Margen superior de 40 y inferior de 20

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
        self.login_button.pack(pady=(30, 10))

        # --- CHECKBOX (CASILLA DE SELECCIÓN) ---
        self.remember_checkbox = ctk.CTkCheckBox(
            self.main_frame, 
            text="Recordarme"
        )
        self.remember_checkbox.pack(pady=10)

    # --- LÓGICA DE VALIDACIÓN ---
    def login_event(self):
        # .get() extrae el texto actual que el usuario escribió en los campos
        email = self.mail_entry.get()
        password = self.pass_entry.get()
        
        # Validación condicional: Comparamos con datos fijos (hardcoded)
        if email == "admin@farmacia.com" and password == "1234":
            # Si coinciden, muestra ventana de información (icono azul)
            messagebox.showinfo("Éxito", f"Bienvenido de nuevo, {email}")
            os.system('python pantallaprincipal.py')
            
        elif "@" not in email or  email not in ".com":
            messagebox.showinfo("Error", f"campo de email sin @ o .com")
        else:
            # Si fallan, muestra ventana de error (icono rojo)
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# --- PUNTO DE ENTRADA DEL PROGRAMA ---
if __name__ == "__main__":
    app = App()       # Creamos la instancia de nuestra clase
    app.mainloop()    # Iniciamos el bucle para que la ventana no se cierre