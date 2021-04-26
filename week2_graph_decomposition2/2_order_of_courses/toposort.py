#Uses python3

import sys
from collections import defaultdict

class Vertex():
    def __init__(self, index):
        self.index = index

        self.visited = 0

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
   
        self.acyclic = True

        self.clock = 1
    
    def previst(self, v):
    
        v.pre = self.clock
        self.clock += 1
        
    def postvist(self, v):

        v.post = self.clock
        self.clock += 1

        v.visited = 1

    def explore(self, v):

        v.visited = -1
        # -1 indicates that the neighbours of this vertex is currently being explored in the recursion sub routines
        # pre-vist block
        self.previst(v)

        # explore each neighbour of the vertex 
        for neighbour in self.adj[v]:

            # if the neighbours point back to the original vertex, we have found a cycle (there is a series of edges which start from v and end at v)
            if neighbour.visited == -1:
                self.acyclic = False

            if neighbour.visited == 0:
                self.explore(neighbour)

        # post-visit block
        self.postvist(v)
        
            
    def DFS(self):
        
        for v in self.vertices:
            # explore each unvisited vertex 
            if v.visited == 0:
                self.explore(v)


def toposort(graph):
    # the topological order of a DAG is simply the vertices sorted by descending post vist index
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

