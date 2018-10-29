"""
    Tim Coutinho
    Prof. Rhodes
    Implementation of the Kruskal and Dijkstra algorithms in Python.
"""

from sys import maxsize


class Graph():

    def __init__(self, nodes):
        self.graph = {vert: edge_list for vert, edge_list in nodes.items()}
        self.vset = {vert: maxsize for vert in nodes}       # Dijkstra
        self.ranks = {vert: 0 for vert in self.graph}       # Kruskal
        self.parents = {vert: vert for vert in self.graph}  # Kruskal

    def Dijkstra(self, start='A'):
        """Finds the shortest path from the starting node to every other."""
        print('Dijkstra:')
        vert = prev = start
        visited = {}  # Distance and path to each node, each only visited once
        visited[vert] = {'Distance': 0, 'Path': start}
        self.vset[vert] = 0

        while self.vset:  # Break once every node has been reached
            # Use the smallest available edge
            vert, dist = sorted(self.vset.items(), key=lambda v: v[1])[0]
            for adj, weight in self.graph[vert].items():
                if adj in visited:
                    prev = adj
                    continue
                new_dist = dist + weight
                if new_dist < self.vset[adj]:  # Found a shorter path to adj
                    self.vset[adj] = new_dist

            del self.vset[vert]      # Remove from set once seen
            if vert not in visited:  # Add to visited list with final path
                visited[vert] = {'Distance': dist,
                                 'Path': f'{visited[prev]["Path"]} -> {vert}'}

        print(f'Shortest path from {start} to each node:')
        for vert in sorted(visited):
            dist, path = visited[vert].values()
            print(f'Node {vert}: Value = {dist}, Path = {path}')
        return visited

    def Kruskal(self, start='A'):
        """Finds the Minimum Spanning Tree of a graph."""

        def ancestor(vert):
            """Finds the root parent of a node"""
            if self.parents[vert] != vert:
                self.parents[vert] = ancestor(self.parents[vert])
            return self.parents[vert]

        def merge(vert, adj):
            """Joins two sub trees into one tree"""
            if self.ranks[vert] > self.ranks[adj]:
                self.parents[adj] = vert
            elif self.ranks[vert] < self.ranks[adj]:
                self.parents[vert] = adj
            else:
                self.parents[adj] = vert
                self.ranks[vert] += 1

        print('Kruskal:')
        edge_set = set()  # Final list of edges included
        node_set = set()  # Final list of nodes reached
        total_weight = 0
        edges = ()        # List of edges in an easier format than the graph
        for vert in self.graph:
            for adj in self.graph[vert]:
                v = tuple(sorted([vert, adj]))
                edges += ((v, self.graph[vert][adj]),)
        edges = tuple(sorted(edges, key=lambda t: t[1]))

        for verts, weight in edges:
            vert, adj = verts
            vert_root, adj_root = ancestor(vert), ancestor(adj)
            if vert_root != adj_root:
                merge(vert_root, adj_root)
                total_weight += weight if verts not in edge_set else 0
                edge_set.add(f'{vert}-{adj}')  # Display format
                node_set.add(vert)
                node_set.add(adj)

        print(f'MST has a total weight of {total_weight}')
        print(f'Node set = {sorted(node_set)}, Edge set = {sorted(edge_set)}')


def main():
    """The graph in a (vertex: (neighbors: weight)) format."""
    nodes = {'A': {'B': 22, 'C': 9,  'D': 12},
             'B': {'A': 22, 'C': 35, 'F': 36, 'H': 34},
             'C': {'A': 9,  'B': 35, 'D': 4,  'E': 65, 'F': 42},
             'D': {'A': 12, 'C': 4,  'E': 33, 'I': 30},
             'E': {'C': 65, 'D': 33, 'F': 18, 'G': 23},
             'F': {'B': 36, 'C': 42, 'E': 18, 'G': 39, 'H': 24},
             'G': {'E': 23, 'F': 39, 'H': 25, 'I': 21},
             'H': {'B': 34, 'F': 24, 'G': 25, 'I': 19},
             'I': {'D': 30, 'G': 21, 'H': 19}}
    # Went for an object oriented approach, why not
    graph = Graph(nodes)
    graph.Dijkstra()
    print()
    graph.Kruskal()


if __name__ == '__main__':
    main()
