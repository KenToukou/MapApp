from itertools import permutations

import pandas as pd
from geopy.distance import geodesic

from logic.mtzoptimization import MTZOptimizer


class TravelingSalesmanService:

    def __init__(self, base_df: pd.DataFrame):
        self.base_df = base_df
        self.edge_vertex_dict = None
        self.vertex_num = None

    def create_base_data(self):
        self.edge_vertex_dict = {}
        self.vertex_num = len(self.base_df.index)
        for (idx, city1), (idx2, city2) in permutations(self.base_df.iterrows(), 2):
            coord1 = (city1["緯度"], city1["経度"])
            coord2 = (city2["緯度"], city2["経度"])

            # 直線距離（キロメートル）を計算
            distance = geodesic(coord1, coord2).kilometers

            # 辞書に追加（キーは "(i,j)" の形式）
            key = (idx + 1, idx2 + 1)
            self.edge_vertex_dict[key] = distance

    def optimize(self):
        optimizer = MTZOptimizer(
            edge_vertex_dict=self.edge_vertex_dict, vertex_num=self.vertex_num
        )
        return optimizer.optimize()
