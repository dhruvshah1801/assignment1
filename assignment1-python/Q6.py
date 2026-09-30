import heapq


def module_dependency_resolver():
    # Read number of modules and edges
    n, e = map(int, input().split())

    modules = []

    for _ in range(n):
        modules.append(input().strip())

    # Graph:
    # module -> modules that depend on it
    graph = {module: [] for module in modules}

    # Indegree = number of dependencies
    indegree = {module: 0 for module in modules}

    # Used to ignore duplicate edges
    edges = set()

    for _ in range(e):
        a, b = input().split()

        # a imports b
        # b must be loaded before a
        edge = (b, a)

        if edge not in edges:
            edges.add(edge)
            graph[b].append(a)
            indegree[a] += 1

    # Min-heap for lexicographically smallest module
    heap = []

    for module in modules:
        if indegree[module] == 0:
            heapq.heappush(heap, module)

    order = []

    while heap:
        current = heapq.heappop(heap)
        order.append(current)

        for dependent in graph[current]:
            indegree[dependent] -= 1

            if indegree[dependent] == 0:
                heapq.heappush(heap, dependent)

    # If all modules are processed, no cycle exists
    if len(order) == n:
        print(" ".join(order))
        return

    # Cycle exists
    print("CYCLE")

    # Find one cycle using DFS
    state = {module: 0 for module in modules}
    parent = {}
    cycle = []

    def dfs(node):
        state[node] = 1

        for nxt in graph[node]:

            if state[nxt] == 0:
                parent[nxt] = node

                if dfs(nxt):
                    return True

            elif state[nxt] == 1:
                # Back edge => cycle
                cycle.append(nxt)

                current = node

                while current != nxt:
                    cycle.append(current)
                    current = parent[current]

                cycle.append(nxt)
                cycle.reverse()

                return True

        state[node] = 2
        return False

    for module in modules:
        if state[module] == 0:
            if dfs(module):
                break

    print(" ".join(cycle))


if __name__ == "__main__":
    module_dependency_resolver()