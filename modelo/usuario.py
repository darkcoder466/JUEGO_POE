class Usuario:
    def __init__(self, nombre_usuario, contrasena, id_usuario=None):
        
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena

    def __str__(self):
        return f"ID: {self.id_usuario} - Usuario: {self.nombre_usuario}"

    
