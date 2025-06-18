from controlador.controlador_partida import obtener_partidas
import tkinter as tk
from tkinter import ttk

def mostrar_tabla_partidas(ventana_maestra):
    ventana = tk.Toplevel(ventana_maestra)
    ventana.title("Historial de Partidas")
    ventana.geometry("800x500")
    ventana.resizable(0,0)

    partidas = obtener_partidas()

    # Definir columnas
    columnas = ("id_partida", "jugador", "resultado", "puntaje", "fecha", "tiempo_segundos")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)

    # Encabezados
    tree.heading("id_partida", text="ID Partida")
    tree.heading("jugador", text="Jugador")
    tree.heading("resultado", text="Resultado")
    tree.heading("puntaje", text="Puntaje")
    tree.heading("fecha", text="Fecha")
    tree.heading("tiempo_segundos", text="Tiempo (s)")

    tree.column("id_partida", width=80, anchor="center")
    tree.column("jugador", width=150, anchor="center")
    tree.column("resultado", width=100, anchor="center")
    tree.column("puntaje", width=100, anchor="center")
    tree.column("fecha", width=180, anchor="center")
    tree.column("tiempo_segundos", width=120, anchor="center")

    tree.place(x=20, y=20, width=760, height=300)

    def llenar_tabla(datos):
        tree.delete(*tree.get_children())
        for partida in datos:
            tree.insert("", "end", values=(
                partida["id_partida"],
                partida["jugador"],
                partida["resultado"],
                partida["puntaje"],
                partida["fecha"],
                partida["tiempo_segundos"]
            ))

    # Funciones de ordenamiento
    def ordenar_por_puntaje():
        ordenados = sorted(partidas, key=lambda x: x["puntaje"], reverse=True)
        llenar_tabla(ordenados)

    def ordenar_por_tiempo():
        ordenados = sorted(partidas, key=lambda x: x["tiempo_segundos"])
        llenar_tabla(ordenados)

    def mostrar_todo():
        llenar_tabla(partidas)

    # Botones
    btn_todo = tk.Button(ventana, text="Mostrar Todo", command=mostrar_todo)
    btn_todo.place(x=150, y=350, width=120, height=30)

    btn_puntaje = tk.Button(ventana, text="Puntaje más alto", command=ordenar_por_puntaje)
    btn_puntaje.place(x=300, y=350, width=120, height=30)

    btn_tiempo = tk.Button(ventana, text="Menor tiempo", command=ordenar_por_tiempo)
    btn_tiempo.place(x=450, y=350, width=120, height=30)

    # Cargar datos al iniciar
    llenar_tabla(partidas)
