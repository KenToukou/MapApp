import math

import networkx
import pulp as pl


class ConstraintAdder:

    @classmethod
    def apply_add_cut(cls, model, x, edges, V, demand, Q, count):
        is_ok = None
        G = networkx.Graph()
        G.add_nodes_from([i for i in range(1, V + 1)])
        for i, j in edges:
            G.add_edge(i, j)
        components = list(networkx.connected_components(G))
        if len(components) == 1:
            is_ok = True
            print("切除平面", components)
            G_new = networkx.Graph()
            G_new.add_nodes_from([i for i in range(2, V + 1)])
            for i, j in edges:
                if i != 1 and j != 1:
                    G_new.add_edge(i, j)
            new_components = list(networkx.connected_components(G_new))
            for S in new_components:
                s_len = len(S)
                s_demand_amount = sum(demand[i] for i in S)
                NS = int(math.ceil(float(s_demand_amount) / Q))
                s_edges = list(
                    set([(i, j) for i in S for j in S if i < j and (i, j) in edges])
                )  # ここがミソ!!
                if s_len >= 3 and (len(s_edges) >= s_len or NS > 1):
                    is_ok = False
                    count += 1
                else:
                    is_ok = True
            if is_ok:
                return model, False, count
            else:
                return model, True, count

        """
        新しいedgeを再構築
        """
        G_new = networkx.Graph()
        G_new.add_nodes_from([i for i in range(1, V + 1)])
        for i, j in edges:
            if i != 1 and j != 1:
                G_new.add_edge(i, j)
        components = list(networkx.connected_components(G_new))

        for S in components:
            s_len = len(S)
            s_demand_amount = sum(demand[i] for i in S)
            NS = int(math.ceil(float(s_demand_amount) / Q))
            s_edges = list(
                set([(i, j) for i in S for j in S if i < j and (i, j) in edges])
            )  # ここがミソ!!
            if s_len >= 3 and (len(s_edges) >= s_len or NS > 1):
                model += pl.lpSum(x[i, j] for i, j in s_edges) <= s_len - NS
        return model, True, count

    @classmethod
    def apply_edge_constraint(cls, model, x, V, m):
        """
        対象巡回セールスマン問題
        """
        for i in range(1, V + 1):
            if i == 1:
                model += pl.lpSum(x[i, j] for j in range(1, V + 1) if i < j) == 2 * m
            else:
                model += (
                    pl.lpSum(x[i, j] for j in range(1, V + 1) if i < j)
                    + pl.lpSum(x[j, i] for j in range(1, V + 1) if i > j)
                    == 2
                )
        return model
