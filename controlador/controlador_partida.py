from modelo.conexion import conectar
from modelo.palabra import Palabra  
from tkinter import messagebox as mb
from modelo.usuario import Usuario
from PIL import Image, ImageTk
import os
import random
# Controlador de la partida, maneja la lógica del juego y la interacción con la base de datos


def obtener_palabra_aleatoria():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        # Obtener todas las palabras de la base de datos
        cursor.execute("SELECT * FROM palabras;")
        resultados = cursor.fetchall()

        if resultados:
            # Seleccionar una palabra aleatoria en Python
            resultado = random.choice(resultados)
            palabra = resultado["palabra"]
            categoria = resultado["categoria"] if resultado["categoria"] else "Sin categoría"
            id_palabra = resultado["id"]

            return Palabra(palabra=palabra, categoria=categoria, id_palabra=id_palabra)
        else:
            return None  # No hay palabras en la DB

    except Exception as e:
        print("Error al obtener palabra aleatoria:", e)
        return None

    finally:
        if conn:
            conn.close()

def obtener_partidas():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                p.id_partida,
                u.nombre_usuario AS jugador,
                p.resultado,
                p.puntaje,
                p.fecha,
                p.tiempo_segundos
            FROM 
                partidas p
            JOIN 
                usuarios u ON p.id_jugador = u.id_usuario;
        """)
        
        resultados = cursor.fetchall()

        partidas = []
        for fila in resultados:
            partidas.append({
                "id_partida": fila["id_partida"],
                "jugador": fila["jugador"],
                "resultado": fila["resultado"],
                "puntaje": fila["puntaje"],
                "fecha": fila["fecha"],
                "tiempo_segundos": fila["tiempo_segundos"]
            })

        return partidas

    except Exception as e:
        print("Error al obtener partidas:", e)
        return []

    finally:
        if conn:
            conn.close()


def iniciar_sesion(usuario, contrasena):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        # Verificar si el usuario existe
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s;", (usuario, contrasena))
        resultado = cursor.fetchone()

        if resultado:
            return Usuario(
                nombre_usuario=resultado["nombre_usuario"],
                contrasena=resultado["contrasena"],
                id_usuario=resultado["id_usuario"]
            )
        else:
            mb.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos.")
            return None  # Usuario o contraseña incorrectos

    except Exception as e:
        mb.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
        print("Error al iniciar sesión:", e)
        return None

    finally:    
        if conn:
            conn.close()


def registrar_usuario(usuario, contrasena):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s;", (usuario,))
        if cursor.fetchone():
            mb.showerror("Error de registro", "El nombre de usuario ya está en uso.")
            return False  # Usuario ya existe

        # Insertar nuevo usuario
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s);", (usuario, contrasena))
        conn.commit()

        mb.showinfo("Registro exitoso", "Usuario registrado correctamente.")
        return True  # Registro exitoso

    except Exception as e:
        mb.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
        print("Error al registrar usuario:", e)
        return False  # Error al registrar

    finally:
        if conn:
            conn.close()



# Clase ParteCuerpo 
class ParteCuerpo:
    def __init__(self, canvas, tipo, posicion, ruta_imagen=None, ancho=None, alto=None):
        self.canvas = canvas
        self.tipo = tipo
        self.posicion = posicion
        self.ruta_imagen = ruta_imagen
        self.ancho = ancho
        self.alto = alto
        self.imagen_tk = None
        self.color = "#3498db"

    def mostrar(self):
        x, y = self.posicion

        if self.ruta_imagen and os.path.exists(self.ruta_imagen):
            img = Image.open(self.ruta_imagen)
            if self.ancho and self.alto:
                img = img.resize((self.ancho, self.alto))
            self.imagen_tk = ImageTk.PhotoImage(img)
            self.dibujo = self.canvas.create_image(x, y, image=self.imagen_tk, anchor="center")
        else:
            print("⚠️ Imagen no encontrada:", self.ruta_imagen)





def mostrar_instrucciones():
    mensaje = (
        "🎮 Instrucciones del Juego:\n\n"
        "- Adivina la palabra secreta letra por letra.\n"
        "- Cada vez que aciertes una letra, se mostrará en su posición.\n"
        "- Si fallas, se dibuja una parte del cuerpo en el ahorcado.\n"
        "- Pierdes si se completa todo el ahorcado sin adivinar la palabra.\n\n"
        "🏆 Sistema de Puntaje:\n"
        "- Cada partida inicia con 10,000 puntos.\n"
        "- Por cada error, se restan 1,000 puntos.\n"
        "- Si adivinas la palabra antes de agotar los intentos, conservas los puntos restantes.\n"
        "- ¡Cada segundo que pasa se restan 50 puntos y después de un minuto se restan 80 puntos cada segundo!\n"
    )
    mb.showinfo("Bienvenido", mensaje)