import tkinter as tk
from controlador.controlador_partida import obtener_palabra_aleatoria,ParteCuerpo
from modelo.partida import Partida
from tkinter import messagebox
import pygame
import threading
from .ventana_puntajes import mostrar_tabla_partidas



# Función que abre la ventana de juego
def ventana_juego(ventana_maestra, sesion):
    for widget in ventana_maestra.winfo_children(): #recorre todos los widgets de la ventana principal
        if isinstance(widget, tk.Toplevel): # Si es una ventana secundaria, la destruye
            widget.destroy()
        
    
    # Lista global para evitar recolección de basura
    sonidos_reproducidos = []# Lista global para evitar eliminación del objeto
    puntaje = 100000# Inicializar el puntaje
    partes_visibles = []# Lista para almacenar las partes del cuerpo visibles
    contador_segundos = 0  # Tiempo total en segundos
    palabra = obtener_palabra_aleatoria() # Obtener una palabra aleatoria al inicio
    letras_visibles = ['_' for _ in palabra.palabra]  # Inicializar letras visibles con guiones bajos
    cont = 0  # indice para las partes del cuerpo
    juego_terminado = False  # Flag de control

    def reproducir_sonido(ruta, bucle=False):
        def tarea():
            try:
                sonido = pygame.mixer.Sound(ruta)
                loops = -1 if bucle else 0
                sonido.play(loops=loops)
                sonidos_reproducidos.append(sonido)
            except Exception as e:
                print(f"Error: {e}")

        threading.Thread(target=tarea).start()


    def calcular_puntaje():
        """Calcula el puntaje basado en el tiempo transcurrido."""
        nonlocal puntaje, contador_segundos,juego_terminado
        if juego_terminado:
            return
        
        puntaje -= 50  # Penalización de 50 puntos por segundo
        if contador_segundos > 60:
            puntaje -= 30  # Penalización adicional de 30 puntos si pasa de 60 segundos
        label_puntaje.config(text=f"Puntaje: {puntaje}")
        
        if puntaje <= 0:
            juego_terminado = True # Terminar el juego si el puntaje llega a 0
            sonidos_reproducidos[0].stop()
            reproducir_sonido(r"sonidos\game-over-deep-male-voice-clip-352695.mp3")
            Partida(sesion.id_usuario, "Perdió", contador_segundos,puntaje).guardar()
            messagebox.showerror("¡Perdiste!", f"La palabra era: {palabra.palabra} puntaje: {puntaje}")
            ventana.destroy()
            ventana_maestra.deiconify()
        
        label_puntaje.after(1000, calcular_puntaje)  # Recalcular cada segundo


    def actualizar_tiempo():
        nonlocal contador_segundos
        contador_segundos += 1

        minutos, segundos = divmod(contador_segundos, 60)
        tiempo_formateado = f"Tiempo: {minutos:02d}:{segundos:02d}"

        label_tiempo.config(text=tiempo_formateado)
        label_tiempo.after(1000, actualizar_tiempo)
    
   
    def verificar(event):
        reproducir_sonido(r"sonidos\purchase-succesful-ingame-230550.mp3")
        nonlocal cont, partes, intentos_restantes, partes_visibles,puntaje
        nonlocal palabra, letras_visibles

        # Obtener letra y deshabilitar botón
        letra = event.widget["text"]
        event.widget.config(state="disabled")
        event.widget.unbind("<Button-1>")

        es_correcta = letra.lower() in palabra.palabra.lower()

        if es_correcta:
            reproducir_sonido(r"sonidos\purchase-succesful-ingame-230550.mp3")
            for i, l in enumerate(palabra.palabra):
                if l.lower() == letra.lower():
                    letras_visibles[i] = l.upper()
            label_palabra.config(text=' '.join(letras_visibles))
        else:
            intentos_restantes -= 1
            puntaje -= 1000  # Penalización de 1000 puntos por error
            label_intentos.config(text=f"Intentos restantes: {intentos_restantes}")
            reproducir_sonido(r"sonidos\negative_beeps-6008.mp3")
            if cont < total_partes:
                parte = partes[cont]
                parte.mostrar()
                partes_visibles.append(parte)
                cont += 1

        if '_' not in letras_visibles:
            sonidos_reproducidos[0].stop()
            reproducir_sonido(r"sonidos\winning-218995.mp3")
            Partida(sesion.id_usuario, "ganó", contador_segundos,puntaje).guardar()
            ventana.destroy()
            messagebox.showinfo("¡Ganaste!", f"La palabra era: {palabra.palabra} puntaje: {puntaje}")
            
            ventana_maestra.deiconify()

        elif intentos_restantes <= 0:
            sonidos_reproducidos[0].stop()
            reproducir_sonido(r"sonidos\game-over-deep-male-voice-clip-352695.mp3")
            puntaje = 0  # Puntaje a 0 al perder
            Partida(sesion.id_usuario, "Perdió", contador_segundos,puntaje).guardar()
            ventana.destroy()
            messagebox.showerror("¡Perdiste!", f"La palabra era: {palabra.palabra} puntaje: {puntaje}")
            
            ventana_maestra.deiconify()

    ventana = tk.Toplevel(ventana_maestra)
    ventana.title("Ventana de Sesión")
    ventana.geometry("1000x600")
    ventana.resizable(0, 0)
    pygame.mixer.init()  # Inicializar el mezclador de pygame
    reproducir_sonido(r"sonidos\game-intro-345507.mp3", bucle=True)  # Reproducir sonido de fondo
    marco_principal = tk.Frame(ventana, width=1000, height=600, bg="gray")
    marco_principal.pack(fill="both", expand=True)

    canvas_izquierdo = tk.Canvas(marco_principal, width=500, height=600, bg="lightblue")
    canvas_izquierdo.pack(side="left", fill="y")
    # Coordenadas base para las partes del cuerpo
    x_base, y_base = 310, 335
    arbol = ParteCuerpo(canvas_izquierdo, "arbol", (200, 300), r"imagenes/arbol.png", 300, 650) # Mostrar el árbol al inicio
    arbol.mostrar()  # Mostrar el árbol al inicio
    partes_visibles.append(arbol)  # Agregar el árbol a la lista de partes visibles
    # Botón para mostrar la ventana de puntajes
    boton_Puntajes = tk.Button(marco_principal, text="Puntajes", command=lambda:mostrar_tabla_partidas(ventana), bg="lightgreen", font=("Arial", 14))
    boton_Puntajes.place(x=10, y=10)

    # Deinir las partes del cuerpo
    partes = [
        ParteCuerpo(canvas_izquierdo, "cabeza", (x_base, y_base),r"imagenes/caveza.png",248,312),
        ParteCuerpo(canvas_izquierdo, "torso", (x_base, y_base),r"imagenes/torzo.png",248,312),
        ParteCuerpo(canvas_izquierdo, "brazo_izq", (x_base, y_base),r"imagenes/brazo_izq.png",248,312),
        ParteCuerpo(canvas_izquierdo, "brazo_der", (x_base, y_base),r"imagenes/brazo_der.png",248,312),
        ParteCuerpo(canvas_izquierdo, "pierna_izq", (x_base, y_base),r"imagenes/pierna_izq.png",248,312),
        ParteCuerpo(canvas_izquierdo, "pierna_der", (x_base, y_base),r"imagenes/pierna_der.png",248,312)
    ]
    
    total_partes = len(partes)  # Índice para las partes del cuerpo
    intentos_restantes = total_partes
    marco_derecho = tk.Frame(marco_principal, width=500, height=600, bg="lightgreen")
    marco_derecho.pack(side="right", fill="y")

    
        # Botones del abecedario (manual, sin bucles)
    boton_A = tk.Button(marco_derecho, text="A", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_A.place(x=20, y=20)

    boton_B = tk.Button(marco_derecho, text="B", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_B.place(x=85, y=20)

    boton_C = tk.Button(marco_derecho, text="C", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_C.place(x=150, y=20)

    boton_D = tk.Button(marco_derecho, text="D", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_D.place(x=215, y=20)

    boton_E = tk.Button(marco_derecho, text="E", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_E.place(x=280, y=20)

    boton_F = tk.Button(marco_derecho, text="F", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_F.place(x=345, y=20)

    boton_G = tk.Button(marco_derecho, text="G", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_G.place(x=410, y=20)

    boton_H = tk.Button(marco_derecho, text="H", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_H.place(x=20, y=90)

    boton_I = tk.Button(marco_derecho, text="I", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_I.place(x=85, y=90)

    boton_J = tk.Button(marco_derecho, text="J", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_J.place(x=150, y=90)

    boton_K = tk.Button(marco_derecho, text="K", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_K.place(x=215, y=90)

    boton_L = tk.Button(marco_derecho, text="L", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_L.place(x=280, y=90)

    boton_M = tk.Button(marco_derecho, text="M", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_M.place(x=345, y=90)

    boton_N = tk.Button(marco_derecho, text="N", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_N.place(x=410, y=90)

    boton_O = tk.Button(marco_derecho, text="O", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_O.place(x=20, y=160)

    boton_P = tk.Button(marco_derecho, text="P", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_P.place(x=85, y=160)

    boton_Q = tk.Button(marco_derecho, text="Q", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_Q.place(x=150, y=160)

    boton_R = tk.Button(marco_derecho, text="R", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_R.place(x=215, y=160)

    boton_S = tk.Button(marco_derecho, text="S", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_S.place(x=280, y=160)

    boton_T = tk.Button(marco_derecho, text="T", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_T.place(x=345, y=160)

    boton_U = tk.Button(marco_derecho, text="U", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_U.place(x=410, y=160)

    boton_V = tk.Button(marco_derecho, text="V", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_V.place(x=20, y=230)

    boton_W = tk.Button(marco_derecho, text="W", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_W.place(x=85, y=230)

    boton_X = tk.Button(marco_derecho, text="X", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_X.place(x=150, y=230)

    boton_Y = tk.Button(marco_derecho, text="Y", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_Y.place(x=215, y=230)

    boton_Z = tk.Button(marco_derecho, text="Z", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_Z.place(x=280, y=230)

    boton_Ñ = tk.Button(marco_derecho, text="Ñ", width=4, height=2, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
    boton_Ñ.place(x=345, y=230)

    boton_A.bind("<Button-1>", verificar)
    boton_B.bind("<Button-1>", verificar)
    boton_C.bind("<Button-1>", verificar)
    boton_D.bind("<Button-1>", verificar)
    boton_E.bind("<Button-1>", verificar)
    boton_F.bind("<Button-1>", verificar)
    boton_G.bind("<Button-1>", verificar)
    boton_H.bind("<Button-1>", verificar)
    boton_I.bind("<Button-1>", verificar)
    boton_J.bind("<Button-1>", verificar)
    boton_K.bind("<Button-1>", verificar)
    boton_L.bind("<Button-1>", verificar)
    boton_M.bind("<Button-1>", verificar)
    boton_N.bind("<Button-1>", verificar)
    boton_Ñ.bind("<Button-1>", verificar)
    boton_O.bind("<Button-1>", verificar)
    boton_P.bind("<Button-1>", verificar)
    boton_Q.bind("<Button-1>", verificar)
    boton_R.bind("<Button-1>", verificar)
    boton_S.bind("<Button-1>", verificar)
    boton_T.bind("<Button-1>", verificar)
    boton_U.bind("<Button-1>", verificar)
    boton_V.bind("<Button-1>", verificar)
    boton_W.bind("<Button-1>", verificar)
    boton_X.bind("<Button-1>", verificar)
    boton_Y.bind("<Button-1>", verificar)
    boton_Z.bind("<Button-1>", verificar)

    
    # Etiqueta para mostrar los intentos restantes
    label_intentos = tk.Label(marco_derecho, text=f"Intentos restantes: {intentos_restantes}", font=("Helvetica", 14, "bold"), bg="lightgreen", fg="black")
    label_intentos.place(x=20, y=550)

    # Etiqueta para mostrar el tiempo
    label_tiempo = tk.Label(marco_derecho, text="Tiempo: 00:00", font=("Helvetica", 14, "bold"), bg="lightgreen", fg="black")
    label_tiempo.place(x=350, y=550)

    # Etiqueta para mostrar el puntaje  
    label_puntaje = tk.Label(marco_derecho, text="Puntaje: 100000", font=("Arial", 14),bg="lightgreen", fg="black")
    label_puntaje.place(x=20,y=500)
    
    calcular_puntaje()  # Iniciar el cálculo del puntaje

    label_palabra = tk.Label(marco_derecho, text=" ".join(letras_visibles), font=("Helvetica", 24, "bold"), bg="lightgreen", fg="black")
    label_palabra.place(x=150, y=350)

    label_categoria = tk.Label(marco_derecho, text=f"Categoría: {palabra.categoria}", font=("Helvetica", 14, "bold"), bg="lightgreen", fg="black")
    label_categoria.place(x=150 , y=300)


    


    
    actualizar_tiempo()  # Iniciar el contador de tiempo

