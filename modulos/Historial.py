class Historial:
    def __init__(self, historial_id, tarea_id, usuario_id, fecha_cambio, descripcion):
        # Constructor que inicializa los atributos del historial.
        self.historial_id = historial_id
        self.tarea_id = tarea_id
        self.usuario_id = usuario_id
        self.fecha_cambio = fecha_cambio
        self.descripcion = descripcion

    def __str__(self):
        # Devuelve una representación en texto del historial.
        return (f"Historial({self.historial_id}, Tarea: {self.tarea_id}, Usuario: {self.usuario_id}, "
                f"Fecha: {self.fecha_cambio}, Descripción: {self.descripcion})")

    def to_dict(self):
        # Convierte el objeto Historial a un diccionario.
        return {
            "historial_id": self.historial_id,
            "tarea_id": self.tarea_id,
            "usuario_id": self.usuario_id,
            "fecha_cambio": self.fecha_cambio,
            "descripcion": self.descripcion
        }
