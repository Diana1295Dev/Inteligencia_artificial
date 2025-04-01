class Estado:
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADA = "Completada"

    # Lista de estados válidos (para validaciones futuras)
    ESTADOS_VALIDOS = [PENDIENTE, EN_PROGRESO, COMPLETADA]

    def __init__(self, estado_id, nombre):
        # Validar que el nombre del estado sea válido
        if nombre not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nombre}. Los estados válidos son: {', '.join(self.ESTADOS_VALIDOS)}")
        
        # Constructor que inicializa los atributos del estado
        self.estado_id = estado_id
        self.nombre = nombre

    def __str__(self):
        # Devuelve una representación en texto del estado
        return f"Estado({self.estado_id}, {self.nombre})"

    def to_dict(self):
        # Convierte el objeto Estado a un diccionario
        return {
            "estado_id": self.estado_id,
            "nombre": self.nombre
        }