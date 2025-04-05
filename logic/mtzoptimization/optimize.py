import pulp as pl
from pulp.apis import COIN_CMD

from .customization.add_constraints import ConstraintAdder
from .customization.add_objective import ObjectiveAdder
from .customization.add_variables import VariablesCreator


class MTZOptimizer:
    def __init__(self, edge_vertex_dict: dict, vertex_num: int):
        self.edge_vertex_dict = edge_vertex_dict
        self.vertex_num = vertex_num
        self.model = None

    def _read(self):
        self.model = pl.LpProblem("Base Traveling Salseman", pl.LpMinimize)
        variables = VariablesCreator(
            edge_vertex_info=self.edge_vertex_dict, vertex_num=self.vertex_num
        )
        variables.generate_variables()
        x = variables.x
        u = variables.u
        self.model = ConstraintAdder.apply_traveling_salesman_constraint(
            x=x, u=u, vertex_num=self.vertex_num, model=self.model
        )
        self.model += ObjectiveAdder.add_objective(
            x=x, wight_dict=self.edge_vertex_dict
        )
        self.model.__data = x, u

    def _solve(self):
        return self.model.solve(
            solver=COIN_CMD(msg=True, options=["seconds=80", "ratioGap=0.01"])
        )

    def _aggregate(self):
        x, u = self.model.__data
        x_opt = {
            key: var.varValue if isinstance(var, pl.LpVariable) else var
            for key, var in x.items()
        }
        u_opt = {
            key: var.varValue if isinstance(var, pl.LpVariable) else var
            for key, var in u.items()
        }
        return x_opt, u_opt, self.model.objective.value()

    def optimize(self):
        self._read()
        self._solve()
        return self._aggregate()


class CutPlaneOptimizer:
    def __init__(self, edge_vertex_dict: dict, vertex_num: int):
        self.edge_vertex_dict = edge_vertex_dict
        self.vertex_num = vertex_num
        self.model = None

    def _read(self):
        self.model = pl.LpProblem("Base Traveling Salseman", pl.LpMinimize)
        variables = VariablesCreator(
            edge_vertex_info=self.edge_vertex_dict, vertex_num=self.vertex_num
        )
        variables.generate_variables()
        x = variables.x
        self.model = ConstraintAdder.apply_traveling_salesman_constraint(
            x=x, vertex_num=self.vertex_num, model=self.model
        )
        self.model += ObjectiveAdder.add_objective(
            x=x, wight_dict=self.edge_vertex_dict
        )
        self.model.__data = x
