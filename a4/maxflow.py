import re
from pprint import pprint

#### Graphviz display
import graphviz
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
#### Graphviz display

def view(graph, path):
    g = graphviz.Digraph('', filename=path, format='png')
    for src, edges in graph.items():
        for dst, cap in edges.items():
            g.edge(str(src), str(dst), label=str(cap))
    g.view()


def bfs(start, dest, graph):
    work = [start]
    # key = visited node, val = source of node 
    visited = {start: start}

    # assumes path
    while len(work) > 0:
        node = work.pop(0)

        # have we found dest?
        if node == dest:
            path = []
            while node != start:
                path = [node] + path
                # backtrack through path
                node = visited[node]
            return [start] + path

        # visit next layer
        for d in graph[node].keys():
            if visited.get(d) == None:
                work.append(d)
                # in the visited entry, note path
                visited[d] = node
    
    # there is no connection from start to dest
    return None

def read_graph(path) -> dict:
    # graphviz edge format
    pat = re.compile(r'(.+) -> (.+) \[label="(.+)"\]')

    # key = vertex, value = [edjes]
    graph = {}

    with open(path) as file:
        for line in file.readlines()[1:-1]:
            # extract the source, destination and capacity
            src, dst, cap = map(int, pat.findall(line)[0])
            
            # if source/dest don't exist yet, add them
            if graph.get(src) == None:
                graph[src] = {}
            if graph.get(dst) == None:
                graph[dst] = {}

            graph[src][dst] = cap

    return graph

# Edmunds-Karp
def ek(path):
    # key = vertex, value = [edjes]
    graph = read_graph(path)

    vs = graph.keys() # vertices
    s, t = min(vs), max(vs)

    flow = {src:{} for src in vs}
    for src, edges in graph.items():
        for d in edges:
            flow[src][d] = 0
            flow[d][src] = 0

    while True:
        # calculate residual
        residual = {src:{} for src in vs}
        for src, edges in graph.items():
            for dst, cap in edges.items():
                cap -= flow[src][dst]

                if cap != 0:
                    residual[src][dst] = cap

                if flow[src][dst] != 0:
                    residual[dst][src] = flow[src][dst]

        p = bfs(s, t, residual)

        # view(graph, 'graph')
        # view(residual, 'residual')
        # view(flow, 'flow')

        if p == None:
            # we did it
            print(residual)
            return sum(residual[t].values()), flow

        mincap = min([residual[p[i]][p[i+1]] for i in range(len(p) - 1)])

        for i in range(len(p) - 1):
            # edge from i to i+1
            u, v = p[i], p[i+1]
            # flow incremented by residual capacity
            flow[u][v] += mincap


        graph = residual


path = 'k4-minus-edge.txt'
max_flow, witness = ek(path)

# remove 0 flows
# witness = {a:{c:d for c, d in b.items() if d != 0} for a, b in witness.items()}

view(read_graph(path), 'graph')
view(witness, 'flow')

print(max_flow)
print(witness)

# problems with this being accurate
# changing k4-minus-edge doesnt affect things (as long as not changing 3)
# printing witness, looks wrong, missing middle connection