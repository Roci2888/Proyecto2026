from models.incident import Incident

class MaxHeap:
    """
    ADT MaxHeap: heap máximo basado en array.
    El incidente con MAYOR prioridad siempre está en la raíz.

    Atributos:
        _data (list): array interno del heap

    Complejidades:
        insert       : O(log n)
        extract_max  : O(log n)
        peek         : O(1)
        top_k        : O(k log n)
        size         : O(1)
    """

    def __init__(self):
        """
        Postcondición: heap inicializado vacío
        Complejidad  : O(1)
        """
        self._data = []

    # ─── Operaciones principales ──────────────────────────────────

    def insert(self, incident: Incident) -> None:
        """
        Inserta un incidente en el heap.
        Precondición : incident debe ser instancia de Incident
        Postcondición: heap mantiene propiedad de máximo
        Complejidad  : O(log n)
        """
        self._data.append(incident)
        self._sift_up(len(self._data) - 1)

    def extract_max(self) -> Incident:
        """
        Extrae el incidente de mayor prioridad.
        Precondición : heap no debe estar vacío
        Postcondición: heap mantiene propiedad de máximo
        Complejidad  : O(log n)
        """
        if not self._data:
            return None

        # Intercambiar raíz con último elemento
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        max_item = self._data.pop()

        if self._data:
            self._sift_down(0)

        return max_item

    def peek(self) -> Incident:
        """
        Retorna el incidente de mayor prioridad sin extraerlo.
        Precondición : heap no debe estar vacío
        Complejidad  : O(1)
        """
        return self._data[0] if self._data else None

    def update_priority(self, id: str) -> bool:
        """
        Recalcula la prioridad de un incidente y reordena el heap.
        Precondición : id debe existir en el heap
        Postcondición: heap mantiene propiedad de máximo
        Complejidad  : O(n log n)
        """
        for i, incident in enumerate(self._data):
            if incident.id == id:
                incident.recalcular_prioridad()
                self._sift_up(i)
                self._sift_down(i)
                return True
        return False

    def top_k(self, k: int) -> list:
        """
        Retorna los k incidentes más críticos sin modificar el heap.
        Precondición : k debe ser mayor a 0
        Postcondición: heap original no se modifica
        Complejidad  : O(k log n)
        """
        if k <= 0:
            raise ValueError("k debe ser mayor a 0")

        # Trabajar sobre una copia
        temp      = MaxHeap()
        temp._data = self._data.copy()
        result    = []

        for _ in range(min(k, len(self._data))):
            result.append(temp.extract_max())

        return result

    # ─── Operaciones internas ─────────────────────────────────────

    def _sift_up(self, i: int) -> None:
        """
        Sube el elemento en posición i hasta su lugar correcto.
        Complejidad: O(log n)
        """
        parent = (i - 1) // 2
        while i > 0 and self._data[i] > self._data[parent]:
            self._data[i], self._data[parent] = self._data[parent], self._data[i]
            i      = parent
            parent = (i - 1) // 2
    def _sift_down(self, i: int) -> None:
        """
        Baja el elemento en posición i hasta su lugar correcto.
        Complejidad: O(log n)
        """
        n = len(self._data)
        while True:
            largest = i
            left    = 2 * i + 1
            right   = 2 * i + 2

            if left < n and self._data[left] > self._data[largest]:
                largest = left
            if right < n and self._data[right] > self._data[largest]:
                largest = right

            if largest == i:
                break

            self._data[i], self._data[largest] = self._data[largest], self._data[i]
            i = largest

    # ─── Utilidades ───────────────────────────────────────────────

    def size(self) -> int:
        """Retorna cantidad de elementos. Complejidad: O(1)"""
        return len(self._data)

    def is_empty(self) -> bool:
        """Retorna True si el heap está vacío. Complejidad: O(1)"""
        return len(self._data) == 0

    def __repr__(self):
        top = self.peek()
        return (f"MaxHeap(size={len(self._data)}, "
                f"top={top.id if top else None})")