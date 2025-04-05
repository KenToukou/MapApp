import pulp as pl


class ObjectiveAdder:
    @classmethod
    def add_objective(cls, x: pl.LpVariable, weight_dict: dict):
        evaluation = pl.lpSum(x[key] * weight_dict[key] for key in weight_dict.keys())
        return evaluation
