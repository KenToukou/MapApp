import pulp as pl


class VariablesCreator:

    def __init__(self, vertex_num: int):
        self.vertex_num: int = vertex_num

        self._x: dict = {}

    def generate_variables(self):
        for i in range(1, self.vertex_num + 1):
            for j in range(2, self.vertex_num + 1):
                if i < j:
                    self._x[(i, j)] = pl.LpVariable(f"edge_{(i,j)}", cat="Binary")

    @property
    def x(self):
        return self._x
