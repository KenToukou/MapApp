import pulp as pl


class ObjectiveAdder:
    @classmethod
    def add_objective(cls, x: pl.LpVariable, wight_dict: dict):
        evaluation = pl.lpSum(x[key] * wight_dict[key] for key in wight_dict.keys())
        return evaluation
