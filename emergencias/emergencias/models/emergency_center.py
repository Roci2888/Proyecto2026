class EmergencyCenter:
    """
    ADT EmergencyCenter: representa un centro de operaciones de emergencia.

    Atributos:
        id (str)        : identificador único del centro
        nombre (str)    : nombre del centro
        ubicacion (str) : nodo del grafo donde está ubicado

    Precondiciones:
        - id debe ser único en el sistema
        - ubicacion debe existir como nodo en RoadNetwork

    Postcondiciones:
        - el centro queda registrado y disponible para asignación de rutas
    """

    def __init__(self, id: str, nombre: str, ubicacion: str):
        """
        Crea un nuevo centro de emergencia.
        Complejidad: O(1)
        """
        # Precondiciones
        if not id or not nombre or not ubicacion:
            raise ValueError("id, nombre y ubicacion son obligatorios")

        self.id        = id
        self.nombre    = nombre
        self.ubicacion = ubicacion

    def __repr__(self):
        return (f"EmergencyCenter(id={self.id}, "
                f"nombre={self.nombre}, ubicacion={self.ubicacion})")