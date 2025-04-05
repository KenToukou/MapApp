from itertools import combinations

import pandas as pd
from geopy.distance import geodesic

from logic.CVRoptimization import CutPlaneOptimizer


class CVRPService:
    def __init__(self, base_df: pd.DataFrame, m: int, Q: int = 15):
        """
        m: 運搬車の数
        Q: 運搬車の最大積載容量
        """
        self.base_df = base_df
        self.m = m
        self.Q = Q

    def set_base_data(self):
        self.edge_vertex_dict = {}
        self.demand_dict = {}
        self.vertex_num = len(self.base_df.index)
        for (idx, city1), (idx2, city2) in combinations(self.base_df.iterrows(), 2):
            coord1 = (city1["緯度"], city1["経度"])
            coord2 = (city2["緯度"], city2["経度"])

            # 直線距離（キロメートル）を計算
            distance = geodesic(coord1, coord2).kilometers

            # 辞書に追加（キーは "(i,j)" の形式）
            key = (idx + 1, idx2 + 1)
            self.edge_vertex_dict[key] = distance
        self.demand_dict = {
            idx + 1: row["乗客"] for idx, row in self.base_df.iterrows()
        }

    def optimize(self):
        optimizer = CutPlaneOptimizer(
            edge_vertex_dict=self.edge_vertex_dict,
            demand_dict=self.demand_dict,
            vertex_num=self.vertex_num,
            m=self.m,
            Q=self.Q,
        )
        best_edges, objective = optimizer.optimize()
        print(best_edges)
        print(objective)
        return best_edges, objective
