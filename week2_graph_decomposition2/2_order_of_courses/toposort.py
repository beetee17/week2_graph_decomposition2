#Uses python3

import sys
from collections import defaultdict

class Vertex():
    def __init__(self, index):
        self.index = index

        self.visited = 0
        self.component = None

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
        self.components = 0
        self.acyclic = True

        self.clock = 1
    
    def previst(self, v):
        v.component = self.components
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
                # once all neighbours of the vertex have been explored, they form a single connected component
                self.components += 1


def toposort(graph):

    graph.DFS()

    return [v.index for v in sorted(graph.vertices, key=lambda x: x.post, reverse=True)]

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]

    vertices = [Vertex(i) for i in range(n)]

    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))

    order = toposort(Graph(edges, vertices))

    for x in order:
        print(x + 1, end=' ')

