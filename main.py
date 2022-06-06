import random
import sys
import pygame
from math import sqrt

def num_of_paths(number_of_cities):
    sum = 0
    for i in range(number_of_cities):
        sum += i
    return sum

def create_points(number_of_cities):
    cities = []
    for i in range(number_of_cities):
        cities.append([random.randint(-100, 100), random.randint(-100, 100)])
    return cities

def create_paths(number_of_cities, per_of_paths):
    connections = []
    for i in range(number_of_cities):
        for n in range(i):
                connections.append([i, n])
    if per_of_paths > 1:
        sys.exit("error, percentage > 100")
    elif per_of_paths != 1:
        for i in range(round(num_of_paths(number_of_cities) * (1 - per_of_paths))):
            connections.pop(random.randrange(len(connections)))
    return connections


def travel_cost(start, finish, cities):
    return sqrt((cities[start][0] - cities[finish][0])**2 + (cities[start][1] - cities[finish][1])**2)


def weighted_graph(cities, paths, path_to_light):
    font = pygame.font.SysFont('chalkduster.ttf', 20)
    img = []
    for i in range(len(cities)):
        img.append(font.render(str(i + 1), True, pygame.Color('white')))
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color('black'))
        draw_borders()
        draw_connections(cities, paths)
        if path_to_light:
            highlight_path(path_to_light, cities)
        draw_cities(cities, img)

        pygame.display.flip()

    pygame.quit()


def draw_cities(cities, img):
    for i in range(len(cities)):
        pygame.draw.circle(screen, pygame.Color('blue'), (cities[i][0] * 4 + screen.get_width() / 2, cities[i][1] * 4 + screen.get_height() / 2), 10)
        screen.blit(img[i], (cities[i][0] * 4 + screen.get_width() / 2 - 4, cities[i][1] * 4 + screen.get_height() / 2 - 6))

def draw_borders():
    pygame.draw.rect(screen, pygame.Color('white'), [(40, 40), (820, 820)], 1)

def draw_connections(cities, paths):
    for i in range(len(paths)):
        pygame.draw.line(screen, pygame.Color('red'), (cities[paths[i][0]][0] * 4 + screen.get_width() / 2, cities[paths[i][0]][1] * 4 + screen.get_height() / 2), (cities[paths[i][1]][0] * 4 + screen.get_width() / 2, cities[paths[i][1]][1] * 4 + screen.get_height() / 2))

def highlight_path(path, cities):
    for i in range(len(path[1:])):
        pygame.draw.line(screen, pygame.Color('green'), (
        cities[path[i]][0] * 4 + screen.get_width() / 2,
        cities[path[i]][1] * 4 + screen.get_height() / 2), (
                         cities[path[i + 1]][0] * 4 + screen.get_width() / 2,
                         cities[path[i + 1]][1] * 4 + screen.get_height() / 2))

def create_graph(paths, number_of_cities):
    graph = {}
    for i in range(number_of_cities):
        graph[i] = []
    for i in paths:
        graph[i[1]].append(i[0])
        if i[1] not in graph[i[0]]:
            graph[i[0]].append(i[1])
    return graph

def bfs(graph, start_node, number_of_cities):
    pathways = []
    for way in graph[start_node]:
        pathways.append([start_node, way])
    for _ in range(number_of_cities - 2):
        queue = pathways.copy()
        pathways = []
        while queue:
            current_path = queue.pop()
            for way in possible_paths(current_path, graph, current_path[-1]):
                temp_list = current_path.copy()
                temp_list.append(way)
                pathways.append(temp_list)
    return pathways

def bfs_for_salesman_problem(graph, start_node, number_of_cities):
    pathways = bfs(graph, start_node, number_of_cities)
    if pathways:
        for way in pathways:
            if start_node in graph[way[-1]] and len(way) == number_of_cities:
                way.append(start_node)
            else:
                way.clear()
    pathways = list(filter(None, pathways))
    return pathways

def dfs_for_salesman_problem(graph, start_node, number_of_cities):
    pathways = []
    taken_path = []
    for way in graph[start_node]:
        taken_path.append([start_node, way])
        while taken_path:
            current_path = taken_path.pop()
            for way2 in possible_paths(current_path, graph, current_path[-1]):
                temp_path = current_path.copy()
                temp_path.append(way2)
                if len(temp_path) == number_of_cities:
                    if 0 in graph[temp_path[-1]]:
                        temp_path.append(0)
                        pathways.append(temp_path)
                else:
                    taken_path.append(temp_path)
    return pathways


def greedy_search(graph, start_node, number_of_cities, cities):
    pathways = []
    for way in graph[start_node]:
        pathways.append([start_node, way])
    best_path = find_shortest_distance(pathways, cities)[0]
    for _ in range(number_of_cities - 2):
        pathways = []
        for way in possible_paths(best_path, graph, best_path[-1]):
            temp_list = best_path.copy()
            temp_list.append(way)
            pathways.append(temp_list)
        best_path = find_shortest_distance(pathways, cities)[0]
    best_path.append(0)
    return best_path

def find_shortest_distance(pathways, cities):
    shortest_length = -1
    shortest_pathway = []
    for pathway in pathways:
        length = calculate_path_cost(pathway, cities)
        if shortest_length > length or shortest_length == -1:
            shortest_length = length
            shortest_pathway = pathway
    return shortest_pathway, shortest_length

def possible_paths(taken_path, graph, node):
    queue = []
    queue.append(node)
    visited = taken_path.copy()
    while queue:
        s = queue.pop(0)

    for neighbour in graph[s]:
        if neighbour not in visited:
            visited.append(neighbour)
            queue.append(neighbour)
    return queue


def calculate_path_cost(pathway, cities):
    length = 0
    for i in range(len(pathway[1:])):
        length += travel_cost(pathway[i], pathway[i + 1], cities)
    return length


def bidirectional_search(start_node, end_node, graph, cities):
    if end_node in graph[start_node]:
        return [end_node, start_node]
    running = True
    i = 2
    pathways_from_start = []
    pathways_from_end = []
    while running:
        pathways_from_start = bfs(graph, start_node, i)
        pathways_from_end = bfs(graph, end_node, i)
        for way_from_start in pathways_from_start:
            for way_from_end in pathways_from_end:
                if way_from_start[-1] == way_from_end[-1]:
                    running = False
                    break
        i += 1
        if i > len(cities) - 2:
            return None
    connecting_paths = []
    for way_from_start in pathways_from_start:
        for way_from_end in pathways_from_end:
            if way_from_start[-1] == way_from_end[-1]:
                connecting_paths.append(way_from_start[:-1] + way_from_end[::-1])
    return find_shortest_distance(connecting_paths, cities)[0]

def min_spanning_tree(graph, paths, cities, start_node):
    path_cost = []
    spanning_tree_connections = []
    for path in paths:
        path_cost.append([travel_cost(path[0], path[1], cities), path])
    path_cost.sort(reverse=True)
    for i in range(len(cities) - 1):
        path_to_check = path_cost.pop()[1]
        while path_cost and does_tree_close(path_to_check, spanning_tree_connections, i, len(graph)):
            path_to_check = path_cost.pop()[1]
        if not path_cost:
            return None
        spanning_tree_connections.append(path_to_check)
    possible_ways = create_paths_from_connections(spanning_tree_connections, start_node, len(graph))
    return find_shortest_distance(finish_conncections(possible_ways, start_node, graph), cities)[0]

def finish_conncections(possible_ways, start_node, graph):
    node_to_connect = []
    for way in possible_ways:
        while way and len(way) <= len(graph):
            if len(way) < len(graph) - 1:
                way.clear()
            if len(way) == len(graph):
                if start_node in graph[way[-1]]:
                    way.append(0)
                else:
                    way.clear()
            elif len(way) == len(graph) - 1:
                for i in range(len(graph)):
                    if i not in way:
                        node_to_connect = i
                        break
                if node_to_connect in graph[way[-1]]:
                    way.append(node_to_connect)
                else:
                    way.clear()
    possible_ways = list(filter(None, possible_ways))
    return possible_ways

def does_tree_close(path, paths, number_of_nodes, number_of_cities):
    is_conncected = False
    graph_of_nodes = create_graph(paths, number_of_cities)
    running = True
    i = 1
    while running:
        pathways_from_start = bfs(graph_of_nodes, path[0], i)
        pathways_from_end = bfs(graph_of_nodes, path[1], i)
        for way_from_start in pathways_from_start:
            for way_from_end in pathways_from_end:
                if way_from_start[-1] == way_from_end[-1]:
                    running = False
        i += 1
        if i > number_of_nodes - 2 and running == True:
            return False
    return True

def create_paths_from_connections(connections, start_node, number_of_cities):
    paths = []
    graph_of_conncections = create_graph(connections, number_of_cities)
    paths = bfs(graph_of_conncections, start_node, 1)
    i = 2
    while bfs(graph_of_conncections, start_node, i):
        paths = bfs(graph_of_conncections, start_node, i)
        i += 1
    return paths


if __name__ == '__main__':

    number_of_cities = 6
    per_of_paths = 1
    choice = 0
    city1 = 0
    city2 = 0
    while not 1 <= choice <= 5:
        choice = int(input(
            "input \n1 for bfs\n2 for dfs\n3 for greedy_search\n4 for min spanning tree\n5 for bidirectional search\n"))

    cities = create_points(number_of_cities)
    paths = create_paths(number_of_cities, per_of_paths)
    graph = create_graph(paths, number_of_cities)

    if choice == 1:
        pathways = bfs_for_salesman_problem(graph, 0, number_of_cities)
        shortest_path = find_shortest_distance(pathways, cities)[0]
    elif choice == 2:
        pathways = dfs_for_salesman_problem(graph, 0, number_of_cities)
        shortest_path = find_shortest_distance(pathways, cities)[0]
    elif choice == 3:
        shortest_path = greedy_search(graph, 0, number_of_cities, cities)
        if shortest_path == [0]:
            print("Greedy search lost path")
    elif choice == 4:
        shortest_path = min_spanning_tree(graph, paths, cities, 0)
        if shortest_path == []:
            print("Spanning tree longest branch was to short to find route")
    else:
        while not 1 <= city1 <= number_of_cities:
            city1 = int(input("input start city\n"))
        while not 1 <= city2 <= number_of_cities:
            city2 = int(input("input end city\n"))
        shortest_path = bidirectional_search(city1 - 1, city2 - 1, graph, cities)
        if shortest_path == None:
            print("path doesn't exist")

    pygame.init()
    screen = pygame.display.set_mode([900, 900])
    weighted_graph(cities, paths, shortest_path)