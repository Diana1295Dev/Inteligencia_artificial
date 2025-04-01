class Usuario:
    # Constructor que inicializa los atributos del usuario.
    def __init__(self, usuario_id, nombre, correo, fecha_creacion=None):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.correo = correo
        self.fecha_creacion = fecha_creacion

    def __str__(self):
        # Devuelve una representación en texto del usuario.
        return f"Usuario({self.usuario_id}, {self.nombre}, {self.correo}, {self.fecha_creacion})"

    def to_dict(self):
        # Convierte el objeto Usuario a un diccionario.
        return {
            "usuario_id": self.usuario_id,
            "nombre": self.nombre,
            "correo": self.correo,
            "fecha_creacion": self.fecha_creacion
        }