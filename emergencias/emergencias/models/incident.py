import time

class Incident:
    """
    ADT Incident: representa un incidente de emergencia reportado.

    Atributos:
        id (str)        : identificador único
        ubicacion (str) : zona geográfica
        tipo (str)      : tipo de incidente
        severidad (int) : nivel de gravedad 1-10
        timestamp (float): tiempo Unix del reporte
        estado (str)    : 'pendiente' | 'en_proceso' | 'resuelto'
        prioridad (float): calculada como severidad × factor_tiempo

    Precondiciones:
        - severidad debe estar entre 1 y 10
        - id debe ser único en el sistema

    Postcondiciones:
        - prioridad se calcula automáticamente al crear el incidente
        - estado inicial siempre es 'pendiente'
    """

    ESTADOS_VALIDOS = ["pendiente", "en_proceso", "resuelto"]
    TIPOS_VALIDOS   = ["incendio", "derrumbe", "herido", "inundacion", "rescate"]

    def __init__(self, id: str, ubicacion: str, tipo: str, severidad: int, timestamp: float):
        """
        Crea un nuevo incidente.
        Complejidad: O(1)
        """
        # Precondiciones
        if not (1 <= severidad <= 10):
            raise ValueError(f"Severidad debe estar entre 1 y 10, recibido: {severidad}")
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido: {tipo}. Válidos: {self.TIPOS_VALIDOS}")

        self.id        = id
        self.ubicacion = ubicacion
        self.tipo      = tipo
        self.severidad = severidad
        self.timestamp = timestamp
        self.estado    = "pendiente"
        self.prioridad = self._calcular_prioridad()

    def _calcular_prioridad(self) -> float:
        """
        Calcula la prioridad del incidente.
        prioridad = severidad × factor_tiempo
        factor_tiempo aumenta mientras más tiempo lleva sin atenderse.
        Complejidad: O(1)
        """
        horas_esperando = (time.time() - self.timestamp) / 3600
        factor_tiempo   = 1 + horas_esperando
        return round(self.severidad * factor_tiempo, 4)

    def actualizar_estado(self, nuevo_estado: str) -> None:
        """
        Actualiza el estado del incidente.
        Precondición : nuevo_estado debe ser válido
        Postcondición: estado queda actualizado
        Complejidad  : O(1)
        """
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nuevo_estado}")
        self.estado = nuevo_estado

    def recalcular_prioridad(self) -> float:
        """
        Recalcula la prioridad según el tiempo actual.
        Complejidad: O(1)
        """
        self.prioridad = self._calcular_prioridad()
        return self.prioridad

    # Comparadores para el Heap
    def __lt__(self, other): return self.prioridad < other.prioridad
    def __le__(self, other): return self.prioridad <= other.prioridad
    def __gt__(self, other): return self.prioridad > other.prioridad
    def __ge__(self, other): return self.prioridad >= other.prioridad
    def __eq__(self, other): return self.prioridad == other.prioridad

    def __repr__(self):
        return (f"Incident(id={self.id}, zona={self.ubicacion}, "
                f"tipo={self.tipo}, prioridad={self.prioridad}, estado={self.estado})")