from typing import DefaultDict
from collections import defaultdict
import heapq

from mensura.conversions import CONVERSIONS, Conversion
from mensura.exceptions import ConversionException, UnitNotFoundException


class Converter:
    """Converter class for units. Handles the graph building
    logic as well as the algorithm to find shortest path between
    units.
    """

    def __init__(self) -> None:
        self.graph: DefaultDict[str, dict[str, float]] = defaultdict(dict)
        self._register_conversions()

    def _register_conversions(self):
        """Register defined conversions"""
        for conversion in CONVERSIONS:
            self.add_conversion(conversion)

    def add_conversion(self, conversion: Conversion):
        """Add bidirectional conversion to graph"""
        src_unit = conversion.src_unit.lower()
        dest_unit = conversion.dest_unit.lower()

        self.graph[src_unit][dest_unit] = conversion.factor
        self.graph[dest_unit][src_unit] = 1 / conversion.factor

    def convert(self, value: int | float, from_unit: str, to_unit: str) -> int | float:
        """Apply Dijkstra's algorithm to convert units using shortest path."""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if from_unit not in self.graph or to_unit not in self.graph:
            raise UnitNotFoundException(
                f"Conversion from {from_unit} to {to_unit} not possible..."
            )

        priority_queue = [(1.0, from_unit)]
        visited = {from_unit: 1.0}

        while priority_queue:
            current_factor, current_unit = heapq.heappop(priority_queue)

            if current_unit == to_unit:
                return value * current_factor

            for neighbour, factor in self.graph[current_unit].items():
                updated_factor = current_factor * factor
                if neighbour not in visited or updated_factor < visited[neighbour]:
                    visited[neighbour] = updated_factor
                    heapq.heappush(priority_queue, (updated_factor, neighbour))

        raise ConversionException(f"Conversion from {from_unit} to {to_unit} failed.")
