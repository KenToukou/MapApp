import networkx
import pulp as pl


class ConstraintAdder:

    @classmethod
    def apply_add_cut(cls, model, x, edges, V):
        G = networkx.Graph()
        G.add_nodes_from([i for i in range(1, V + 1)])
        for i, j in edges:
            G.add_edge(i, j)
        components = list(networkx.connected_components(G))
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
        for i in range(1, V + 1):
            model += (
                pl.lpSum(x[i, j] for j in range(1, V + 1) if i < j)
                + pl.lpSum(x[j, i] for j in range(1, V + 1) if i > j)
                == 2
            )
        return model
