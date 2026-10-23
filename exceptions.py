"""Исключения для графа и поиска маршрутов."""


class GraphError(Exception):
    """Базовая ошибка графа."""


class VertexAlreadyExistsError(GraphError):
    """Станция уже есть в графе."""

    def __init__(self, vertex: str) -> None:
        super().__init__(f"Станция '{vertex}' уже существует.")


class VertexNotFoundError(GraphError):
    """Станция не найдена."""

    def __init__(self, vertex: str) -> None:
        super().__init__(f"Станция '{vertex}' не найдена.")


class EdgeAlreadyExistsError(GraphError):
    """Перегон между станциями уже существует."""

    def __init__(self, u: str, v: str) -> None:
        super().__init__(f"Перегон между '{u}' и '{v}' уже существует.")


class EdgeNotFoundError(GraphError):
    """Перегон не найден."""

    def __init__(self, u: str, v: str) -> None:
        super().__init__(f"Перегон между '{u}' и '{v}' не найден.")


class InvalidWeightError(GraphError):
    """Некорректный вес ребра."""

    def __init__(self, weight: float) -> None:
        super().__init__(f"Время перегона должно быть больше 0, передано: {weight}.")


class PathNotFoundError(GraphError):
    """Путь между станциями не найден."""

    def __init__(self, start: str, end: str) -> None:
        super().__init__(f"Невозможно построить маршрут от '{start}' до '{end}'.")
