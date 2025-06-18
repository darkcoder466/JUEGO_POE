class Palabra:
    
    def __init__(self, palabra, categoria=None, id_palabra=None):
        self.palabra = palabra
        self.categoria = categoria
        self.id_palabra = id_palabra
        

    def __str__(self):
        return f"ID: {self.id_palabra} - Palabra: '{self.palabra}' - Categoría: '{self.categoria}'"

    def to_dict(self):
        """Retorna un diccionario representando el objeto, útil para guardar en DB o JSON."""
        return {
            "id": self.id_palabra,
            "palabra": self.palabra,
            "categoria": self.categoria
        }
