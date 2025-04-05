from typing import Dict, Tuple

import pulp as pl


class VariablesCreator:

    def __init__(self, edge_vertex_info: Dict[Tuple, float], vertex_num: int):
        self.edge_vertex_info: dict = edge_vertex_info
        self.vertex_num: int = vertex_num

        self._x: dict = {}
        self._u: dict = {}

    def generate_variables(self):
        for key in self.edge_vertex_info.keys():
            self._x[key] = pl.LpVariable(f"edge_{key}", cat="Binary")
        for i in range(1, self.vertex_num + 1):
            self._u[i] = pl.LpVariable(
                f"point_{i}", lowBound=0, upBound=self.vertex_num - 1, cat="Integer"
            )

    @property
    def x(self):
        return self._x

    @property
    def u(self):
        return self._u
