"""Реализация взвешенного графа и алгоритма Дейкстры."""

import heapq

from exceptions import (
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    InvalidWeightError,
    PathNotFoundError,
    VertexAlreadyExistsError,
    VertexNotFoundError,
)


class Graph:
    """Неориентированный взвешенный граф для метро."""

    def __init__(self) -> None:
        self._adj: dict[str, dict[str, float]] = {}

    def add_vertex(self, vertex: str) -> None:
        """Добавить станцию."""
        if vertex in self._adj:
            raise VertexAlreadyExistsError(vertex)
        self._adj[vertex] = {}

    def remove_vertex(self, vertex: str) -> None:
        """Удалить станцию и все связанные с ней перегоны."""
        if vertex not in self._adj:
            raise VertexNotFoundError(vertex)
        del self._adj[vertex]
        for neighbors in self._adj.values():
            neighbors.pop(vertex, None)

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """Добавить двусторонний перегон между станциями с заданным временем."""
        if u not in self._adj:
            raise VertexNotFoundError(u)
        if v not in self._adj:
            raise VertexNotFoundError(v)
        if weight <= 0:
            raise InvalidWeightError(weight)
        if v in self._adj[u]:
            raise EdgeAlreadyExistsError(u, v)

        self._adj[u][v] = float(weight)
        self._adj[v][u] = float(weight)

    def remove_edge(self, u: str, v: str) -> None:
        """Удалить перегон."""
        if u not in self._adj:
            raise VertexNotFoundError(u)
        if v not in self._adj:
            raise VertexNotFoundError(v)
        if v not in self._adj[u]:
            raise EdgeNotFoundError(u, v)

        del self._adj[u][v]
        del self._adj[v][u]

    def _dijkstra(self, start: str, end: str) -> tuple[float, list[str]]:
        """Алгоритм Дейкстры для поиска кратчайшего времени и пути."""
        if start not in self._adj:
            raise VertexNotFoundError(start)
        if end not in self._adj:
            raise VertexNotFoundError(end)

        distances = {v: float("inf") for v in self._adj}
        previous: dict[str, str | None] = dict.fromkeys(self._adj)
        distances[start] = 0.0

        pq = [(0.0, start)]
        visited = set()

        while pq:
            current_dist, curr_v = heapq.heappop(pq)

            if curr_v in visited:
                continue
            visited.add(curr_v)

            if curr_v == end:
                break

            for neighbor, weight in self._adj[curr_v].items():
                if neighbor in visited:
                    continue
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = curr_v
                    heapq.heappush(pq, (new_dist, neighbor))

        if distances[end] == float("inf"):
            raise PathNotFoundError(start, end)

        path = []
        curr: str | None = end
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()

        return distances[end], path

    def shortest_time(self, start: str, end: str) -> float:
        """Вернуть минимальное время в пути."""
        total_time, _ = self._dijkstra(start, end)
        return round(total_time, 2)

    def shortest_path(self, start: str, end: str) -> list[str]:
        """Вернуть список станций оптимального маршрута."""
        _, path = self._dijkstra(start, end)
        return path
