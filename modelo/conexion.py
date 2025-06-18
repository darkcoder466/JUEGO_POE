import mysql.connector

def conectar():
    try:
        conn = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            port=3307,
            database="JUEGO"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos:")
        return None
