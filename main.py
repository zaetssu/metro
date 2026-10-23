"""Консольная утилита для поиска кратчайших маршрутов в Московском метрополитене."""

import argparse
import sys
from collections.abc import Sequence

from exceptions import GraphError
from metro_data import build_metro_graph


def create_parser() -> argparse.ArgumentParser:
    """Создаёт и настраивает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="metro",
        description="Утилита расчёта кратчайшего пути и времени в Московском метро.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Режим работы")

    # Команда path (выводит список станций)
    path_parser = subparsers.add_parser("path", help="Вывести список станций маршрута")
    path_parser.add_argument("--from", dest="start", required=True, help="Станция отправления")
    path_parser.add_argument("--to", dest="end", required=True, help="Станция назначения")

    # Команда time (выводит только время)
    time_parser = subparsers.add_parser("time", help="Вывести время в пути в минутах")
    time_parser.add_argument("--from", dest="start", required=True, help="Станция отправления")
    time_parser.add_argument("--to", dest="end", required=True, help="Станция назначения")

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Точка входа консольного приложения."""
    parser = create_parser()
    args = parser.parse_args(argv)

    metro = build_metro_graph()

    try:
        if args.command == "time":
            print(metro.shortest_time(args.start, args.end))
        elif args.command == "path":
            for station in metro.shortest_path(args.start, args.end):
                print(station)
    except GraphError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
