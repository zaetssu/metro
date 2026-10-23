"""Тесты для графа[cite: 1]."""

import pytest

from exceptions import (
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    InvalidWeightError,
    PathNotFoundError,
    VertexAlreadyExistsError,
    VertexNotFoundError,
)
from graph import Graph
from metro_data import STATIONS, build_metro_graph


def test_add_vertex() -> None:
    """Проверка добавления вершин."""
    g = Graph()
    g.add_vertex("A")
    assert "A" in g._adj


def test_add_duplicate_vertex_raises() -> None:
    """Ошибка при дублировании вершины."""
    g = Graph()
    g.add_vertex("A")
    with pytest.raises(VertexAlreadyExistsError):
        g.add_vertex("A")


def test_remove_vertex() -> None:
    """Проверка удаления вершины со связями."""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", 2.0)
    g.remove_vertex("B")
    with pytest.raises(VertexNotFoundError):
        g.shortest_time("A", "B")


def test_remove_missing_vertex_raises() -> None:
    """Ошибка при удалении несуществующей вершины."""
    g = Graph()
    with pytest.raises(VertexNotFoundError):
        g.remove_vertex("X")


def test_add_edge_duplicate_raises() -> None:
    """Ошибка при дублировании ребра."""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", 2.0)
    with pytest.raises(EdgeAlreadyExistsError):
        g.add_edge("A", "B", 3.0)


@pytest.mark.parametrize("weight", [0.0, -2.5])
def test_add_edge_invalid_weight(weight: float) -> None:
    """Ошибка при некорректном весе."""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    with pytest.raises(InvalidWeightError):
        g.add_edge("A", "B", weight)


def test_remove_edge() -> None:
    """Успешное удаление ребра."""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", 2.0)
    g.remove_edge("A", "B")
    with pytest.raises(EdgeNotFoundError):
        g.remove_edge("A", "B")


def test_remove_missing_edge_raises() -> None:
    """Ошибка при удалении несуществующего ребра."""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    with pytest.raises(EdgeNotFoundError):
        g.remove_edge("A", "B")


@pytest.mark.parametrize(
    ("start", "end", "time"),
    [
        ("А", "В", 3.0),
        ("Б", "Б", 0.0),
    ],
)
def test_dijkstra_paths(start: str, end: str, time: float) -> None:
    """Проверка работы алгоритма Дейкстры."""
    g = Graph()
    for v in ("А", "Б", "В"):
        g.add_vertex(v)
    g.add_edge("А", "Б", 1.0)
    g.add_edge("Б", "В", 2.0)
    assert g.shortest_time(start, end) == time


def test_unreachable_path_raises() -> None:
    """Ошибка, если путь не существует."""
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    with pytest.raises(PathNotFoundError):
        g.shortest_path("A", "B")


def test_metro_integration() -> None:
    """Интеграционный тест на реальных данных метро[cite: 3, 5]."""
    metro = build_metro_graph()
    assert len(STATIONS) >= 30
    assert metro.shortest_time("Арбатская (Арбатско-Покровская)", "Таганская (Кольцевая)") == 9.5
