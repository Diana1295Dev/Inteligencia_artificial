class Tarea:
    def __init__(self, tarea_id, titulo, descripcion, fecha_creacion, fecha_limite, responsable, estado):
        # Constructor que inicializa los atributos de la tarea.
        self.tarea_id = tarea_id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.fecha_limite = fecha_limite
        self.responsable = responsable   # Aquí se asigna directamente el objeto Usuario
        self.estado = estado             # El estado puede seguir siendo una cadena (Pendiente, En Progreso, Completada)

    def __str__(self):
        # Devuelve una representación en texto de la tarea.
        return (f"Tarea({self.tarea_id}, {self.titulo}, Estado: {self.estado}, "
                f"Responsable: {self.responsable.nombre}, Fecha Creación: {self.fecha_creacion}, "
                f"Fecha Límite: {self.fecha_limite})")

    def to_dict(self):
        # Convierte el objeto Tarea a un diccionario.
        return {
            "tarea_id": self.tarea_id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion,
            "fecha_limite": self.fecha_limite,
            "responsable": self.responsable.to_dict(),  # Convierte el usuario a diccionario
            "estado": self.estado
        }