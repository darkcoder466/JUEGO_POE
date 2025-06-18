from datetime import datetime
from modelo.conexion import conectar  # Asegúrate de que la ruta es correcta

class Partida:
    def __init__(self, id_jugador, resultado, tiempo_segundos,puntaje, fecha=None, id_partida=None):
        """
        Crea una instancia de una partida.
        """
        self.id_partida = id_partida
        self.id_jugador = id_jugador
        self.resultado = resultado
        self.tiempo_segundos = tiempo_segundos
        self.puntaje = puntaje
        self.fecha = fecha or datetime.now()

    def __str__(self):
        return (f"Partida #{self.id_partida or 'N/A'} - Jugador: {self.id_jugador} - "
                f"Resultado: {self.resultado} - Tiempo: {self.tiempo_segundos}s - "
                f"Puntaje: {self.puntaje} - Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
        
            




    def to_dict(self):
        """Devuelve un diccionario útil para insertar en base de datos o convertir a JSON."""
        return {
            "id_partida": self.id_partida,
            "id_jugador": self.id_jugador,
            "resultado": self.resultado,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "tiempo_segundos": self.tiempo_segundos,
            "puntaje": self.puntaje
        }
    
    def guardar(self):
        """
        Guarda la partida en la base de datos. Si se guarda correctamente, actualiza el id_partida.
        """
        try:
            conn = conectar()
            cursor = conn.cursor()

            query = """
                INSERT INTO partidas (id_jugador, resultado, fecha, tiempo_segundos, puntaje)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (self.id_jugador, self.resultado, self.fecha.strftime("%Y-%m-%d %H:%M:%S"), self.tiempo_segundos, self.puntaje)

            cursor.execute(query, valores)
            conn.commit()
            self.id_partida = cursor.lastrowid  # Guarda el ID generado por la base de datos

            cursor.close()
            conn.close()

            return True  # Éxito
        except Exception as e:
            print("Error al guardar la partida:", e)
            return False  # Fallo
