import pulp as pl
from pulp.apis import COIN_CMD

from .customization.add_constraints import ConstraintAdder
from .customization.add_objective import ObjectiveAdder
from .customization.add_variables import VariablesCreator


class CutPlaneOptimizer:
    def __init__(
        self, edge_vertex_dict: dict, demand_dict: dict, vertex_num: int, m: int, Q: int
    ):
        self.edge_vertex_dict = edge_vertex_dict
        self.demand_dict = demand_dict

        self.m = m
        self.Q = Q

        self.vertex_num = vertex_num
        self.model = None
        self.is_closed_circuit = None

    def optimize(self):
        # 問題の初期化
        self.model = pl.LpProblem("Base Traveling Salesman", pl.LpMinimize)

        # 変数を生成
        variables = VariablesCreator(vertex_num=self.vertex_num)
        variables.generate_variables()
        x = variables.x

        # 制約を追加
        self.model = ConstraintAdder.apply_edge_constraint(
            x=x, V=self.vertex_num, model=self.model, m=self.m
        )
        # 目的関数を設定
        self.model += ObjectiveAdder.add_objective(
            x=x, weight_dict=self.edge_vertex_dict
        )

        # 初期解を求める
        EPS = 1e-6
        self.model.__data = x
        status = self._solve()
        if status != pl.LpStatusOptimal:
            raise Exception("初期問題が解けませんでした。")

        # 切除平面法のループ
        count = 0
        while True:
            # 解の変数値を集計
            x_opt = self._aggregate()
            edges = [key for key, value in x_opt.items() if value > EPS]

            # サブツアー制約を追加
            self.model, self.is_closed_circuit, count = ConstraintAdder.apply_add_cut(
                model=self.model,
                x=x,
                V=self.vertex_num,
                edges=edges,
                demand=self.demand_dict,
                Q=self.Q,
                count=count,
            )

            # 全体が1つの閉じた巡回路になった場合、ループを終了
            if self.is_closed_circuit is False:
                break

            status = self._solve()

            # 無限ループ防止のための追加チェック
            if status != pl.LpStatusOptimal:
                raise Exception("切除平面法の最適化に失敗しました。")

            if count == 5:
                raise Exception("解が収束しません")

        # 最適解の取得
        x_opt = self._aggregate()
        best_edges = [pair for pair, val in x_opt.items() if val > EPS]
        return best_edges, pl.value(self.model.objective)

    def _solve(self):
        return self.model.solve(
            solver=COIN_CMD(msg=True, options=["seconds=80", "ratioGap=0.01"])
        )

    def _aggregate(self):
        x = self.model.__data
        x_opt = {
            key: var.varValue if isinstance(var, pl.LpVariable) else var
            for key, var in x.items()
        }
        return x_opt
