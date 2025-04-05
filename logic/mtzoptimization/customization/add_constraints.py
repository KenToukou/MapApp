import networkx
import pulp as pl


class ConstraintAdder:
    @classmethod
    def apply_traveling_salesman_constraint(
        cls, x: pl.LpVariable, u: pl.LpVariable, vertex_num: int, model
    ):
        """
        非対称の巡回セールスマン問題
        """

        for i in range(1, vertex_num + 1):
            model += pl.lpSum(x[i, j] for j in range(1, vertex_num + 1) if i != j) == 1
            model += pl.lpSum(x[j, i] for j in range(1, vertex_num + 1) if i != j) == 1
            for j in range(2, vertex_num + 1):
                if i != j:
                    model += (u[i] + 1) - (vertex_num * (1 - x[i, j])) + (
                        vertex_num - 2
                    ) * x[j, i] <= u[j]
            for i in range(2, vertex_num + 1):
                model += 1 + (1 - x[1, i]) + (vertex_num - 3) * x[i, 1] <= u[i]
                model += vertex_num - 2 + x[i, 1] - (vertex_num - 3) * x[1, i] >= u[i]

        return model

    @classmethod
    def apply_add_cut(cls, model, x, edges, V):
        G = networkx.Graph()
        G.add_nodes_from(V)
        for i, j in edges:
            G.add_edge(i, j)
        components = networkx.connected_components(G)
        if len(components) == 1:
            return model, False

        for S in components:
            model += pl.lpSum(x[i, j] for i in S for j in S if i < j) <= len(S) - 1
        return model, True

    @classmethod
    def apply_edge_constraint(cls, model, x, V):
        """
        対象巡回セールスマン問題
        """
        for i in V:
            model += (
                pl.lpSum(x[i, j] for j in V if i < j)
                + pl.lpSum(x[j, i] for j in V if i > j)
                == 2
            )
        return model
