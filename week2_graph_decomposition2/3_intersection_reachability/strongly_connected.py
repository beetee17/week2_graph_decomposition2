#Uses python3

import sys

sys.setrecursionlimit(200000)

from collections import defaultdict

class Vertex():
    def __init__(self, index):
        self.index = index

        self.visited = 0
        self.scc = None

        self.pre = None
        self.post = None


class Graph():
    def __init__(self, edges, vertices):

        # create a dict with vertex as key and list of its neighbours as values
        self.adj = defaultdict(list)
    
        self.edges = edges

        # for a directed graph, b is adjacent to a but not vice versa
        for (a, b) in edges:
            self.adj[vertices[a-1]].append(vertices[b-1])
                    
        self.vertices = vertices
        self.num_scc = 1
        self.acyclic = True

        self.clock = 1
    
    def previst(self, v):
        v.scc = self.num_scc
        v.pre = self.clock
        self.clock += 1
        
    def postvist(self, v):
        v.post = self.clock
        self.clock += 1

        v.visited = 1

    def explore(self, v):

        v.visited = -1
        # pre-vist block
        self.previst(v)

        # explore each neighbour of the vertex 
        for neighbour in self.adj[v]:
            if neighbour.visited == -1:
                self.acyclic = False

            if neighbour.visited == 0:
                self.explore(neighbour)

        # post-visit block
        self.postvist(v)
        
            
    def DFS(self):
        
        for v in self.vertices:
            # explore each vertex (and its neighbours)
            if v.visited == 0:
                self.explore(v)
     

    def find_strongly_connected_components(self, reverse_postorder):
        for v in self.vertices:
            v.visited = 0

        for v in reverse_postorder:
            
            if v.visited == 0:
                self.explore(v)
                # once all neighbours of the vertex have been explored, they form a single strongly connected component
                self.num_scc += 1

        self.num_scc -= 1


def number_of_strongly_connected_components(edges, vertices):
    # The vertex with the single largest post order number in the entire graph has to come from a component with no other components pointing to it. That vertex needs to be the source component
    # the reverse graph and the orig graph have the same strongly connected componenets (scc)
    # however, source component of reverse graph are sink componente of orig graph
    # therefore, by performing DFS on the reverse graph, we find its source components which give us the sink components of the original graph, which is what we want

    graph = Graph(edges, vertices)

    # let the reverse_graph be the graph obtained by flipping the direction of all its edges
    reverse_edges = []

    for (a, b) in edges:
        reverse_edges.append([b, a])
        reverse_graph = Graph(reverse_edges, vertices)


    # perfrom DFS on reverse graph to populate post visit indices for each vertex
    reverse_graph.DFS()

    # sort by descending post visit index
    reverse_postorder = [v for v in sorted(reverse_graph.vertices, key=lambda x: x.post, reverse=True)]

    # a sink scc has no outgoing edges from the component
    # if v is in a sink component, explore(v) will find all the vertices reachable from v, which is the definition of a scc
    graph.find_strongly_connected_components(reverse_postorder)


    return graph.num_scc

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]

    vertices = [Vertex(i) for i in range(n)]

    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))

    print(number_of_strongly_connected_components(edges, vertices))
