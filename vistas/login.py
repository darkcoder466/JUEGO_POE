import tkinter as tk
from tkinter import messagebox
from controlador.controlador_partida import registrar_usuario, iniciar_sesion,mostrar_instrucciones
import threading as th
from .ventana_juego import ventana_juego

class Login():
    
    def __init__(self):
        self.ventana_inicio = tk.Tk()
        self.ventana_inicio.title("Pantalla de Inicio")
        self.ventana_inicio.geometry("400x300")
        self.ventana_inicio.resizable(0, 0)
        self.ventana_inicio.config(bg="lightblue")
        self.sesion = None
        mostrar_instrucciones()

        label_bienvenida = tk.Label(self.ventana_inicio, text="¡Bienvenido al juego!", font=("Arial", 16), bg="lightblue")
        label_bienvenida.pack(pady=40)

        btn_empezar = tk.Button(self.ventana_inicio, text="ingresar", font=("Arial", 14), bg="white", command=self.abrir_login)
        btn_empezar.pack()

        self.ventana_inicio.mainloop()

    def abrir_login(self):
        self.ventana_inicio.destroy()

        self.login = tk.Tk()
        self.login.title("Login")
        self.login.geometry("400x300")
        self.login.config(bg="lightgreen")
        self.login.resizable(0, 0)


        # Título
        tk.Label(self.login, text="Sistema de Usuario", font=("Arial", 16), bg="lightgreen").pack(pady=20)

        # Campos de entrada
        tk.Label(self.login, text="Usuario:", bg="lightgreen", font=("Arial", 12)).pack()
        self.txtUsuario = tk.Entry(self.login, bg="white", font=("Arial", 12))
        self.txtUsuario.pack(pady=5)

        tk.Label(self.login, text="Contraseña:", bg="lightgreen", font=("Arial", 12)).pack()
        self.txtpassword = tk.Entry(self.login, show="*", bg="white", font=("Arial", 12))
        self.txtpassword.pack(pady=5)

        # Botón para mostrar/ocultar contraseña
        self.btnVer = tk.Button(self.login, text="👁 Mostrar", bg="white", font=("Arial", 10))
        self.btnVer.pack(pady=5)
        self.btnVer.bind("<Button-1>", self.alternar_mostrar_password)

        # Frame para los botones principales
        frame_botones = tk.Frame(self.login, bg="lightgreen")
        frame_botones.pack(pady=20)

        # Botón de Iniciar Sesión
        btn_iniciar = tk.Button(frame_botones, text="Iniciar Sesión", 
                               command=self.iniciar_sesion, 
                               bg="lightblue", font=("Arial", 12), width=12)
        btn_iniciar.pack(side=tk.LEFT, padx=10)

        # Botón de Registrarse
        btn_registrar = tk.Button(frame_botones, text="Registrarse", 
                                 command=self.registrar_usuario, 
                                 bg="orange", font=("Arial", 12), width=12)
        btn_registrar.pack(side=tk.LEFT, padx=10)

    def alternar_mostrar_password(self, event):
        """Función para mostrar u ocultar la contraseña"""
        if  self.txtpassword.cget("show") == "*":
            self.txtpassword.config(show="")
            self.btnVer.config(text="👁 Ocultar")
        else:
            self.txtpassword.config(show="*")
            self.btnVer.config(text="👁 Mostrar")

    def iniciar_sesion(self):
        """Función para iniciar sesión con usuario existente"""
        usuario = self.txtUsuario.get().strip()
        contrasena = self.txtpassword.get().strip()
        
        # Verificar que los campos no estén vacíos
        if not usuario or not contrasena:
            messagebox.showwarning("Error", "Por favor ingrese usuario y contraseña.")
            return
        # iniciar sesión
        sesion = iniciar_sesion(usuario, contrasena)
        self.login.withdraw()
        ventana_juego(self.login,sesion)
        

    def registrar_usuario(self):
        """Función para registrar un nuevo usuario"""
        usuario = self.txtUsuario.get().strip()
        contrasena = self.txtpassword.get().strip()
        
        # Verificar que los campos no estén vacíos
        if not usuario or not contrasena:
            messagebox.showwarning("Error", "Por favor ingrese usuario y contraseña.")
            return
        
        registrar_usuario(usuario, contrasena)
        # Limpiar los campos después del registro
        self.txtUsuario.delete(0, tk.END)
        self.txtpassword.delete(0, tk.END)



    def cerrar_juego(self):
        """Se ejecuta al cerrar la ventana del juego"""

