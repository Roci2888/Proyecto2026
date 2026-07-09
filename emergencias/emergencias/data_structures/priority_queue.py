from data_structures.heap import MaxHeap
from models.incident import Incident

class PriorityQueue:
    """
    ADT PriorityQueue: cola de prioridad basada en MaxHeap.
    Gestiona incidentes según su nivel de urgencia.

    Atributos:
        _heap (MaxHeap): heap interno

    Complejidades:
        enqueue     : O(log n)
        dequeue     : O(log n)
        peek        : O(1)
        top_k       : O(k log n)
    """

    def __init__(self):
        """
        Postcondición: cola inicializada vacía
        Complejidad  : O(1)
        """
        self._heap = MaxHeap()

    def enqueue(self, incident: Incident) -> None:
        """
        Agrega un incidente a la cola.
        Precondición : incident debe ser instancia de Incident
        Postcondición: incidente insertado según su prioridad
        Complejidad  : O(log n)
        """
        self._heap.insert(incident)

    def dequeue(self) -> Incident:
        """
        Extrae el incidente más urgente.
        Precondición : cola no debe estar vacía
        Postcondición: incidente de mayor prioridad extraído
        Complejidad  : O(log n)
        """
        if self.is_empty():
            raise IndexError("La cola de prioridad está vacía")
        return self._heap.extract_max()

    def peek(self) -> Incident:
        """
        Muestra el incidente más urgente sin extraerlo.
        Complejidad: O(1)
        """
        return self._heap.peek()

    def top_k(self, k: int) -> list:
        """
        Retorna los k incidentes más críticos.
        Complejidad: O(k log n)
        """
        return self._heap.top_k(k)

    def update_priority(self, id: str) -> bool:
        """
        Actualiza la prioridad de un incidente.
        Complejidad: O(n log n)
        """
        return self._heap.update_priority(id)

    def is_empty(self) -> bool:
        """Complejidad: O(1)"""
        return self._heap.is_empty()

    def size(self) -> int:
        """Complejidad: O(1)"""
        return self._heap.size()

    def __repr__(self):
        return f"PriorityQueue(size={self._heap.size()})"