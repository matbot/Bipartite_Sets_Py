#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Author: Mathew McDade
    Date: 2/17/2019
    Class: CS325.400 Winter 2019
    Assignment: HW5: Wrestler
    Description: This program takes input from a txt file passed by name as an argument from the CLI. An adjacency list
    graph is built using the txt file input. The primary algorithm attempts to separate the graph into bipartite sets
    using a breadth first search. The sets are then separated into babyfaces and heels and returned. If bipartite sets
    are not possible, the algorithm returns false.
"""

import sys      # for argv
import queue    # threadable queue data structure.


# build_graph: takes a list of vertices and edges and builds a dict with an adjacency list.
def build_graph(vertices, edges):
    graph = {}
    for vertex in vertices:                                         # Theta(V)
        graph.update({vertex: {'rivals': [], 'color': 'white'}})
    for edge in edges:                                              # + Theta(E)
        graph[edge[0]]['rivals'].append(edge[1])
        graph[edge[1]]['rivals'].append(edge[0])
    return graph


# bfs_classify: performs a breadth first search on the graph using a queue and a 2-color marking to track each
#   bipartite set.
def bfs_classify(royal_rumble):
    q = queue.Queue(maxsize=len(royal_rumble))
    # Outer for loop ensures that disconnected vertices will process. Should only run once for a connected graph.
    #   Will have an inverse relation to the number of edges: r has a max n - 1 - #disconnected sets.
    for wrestler in royal_rumble:
        if royal_rumble[wrestler]['color'] == 'white':
            royal_rumble[wrestler]['color'] = 'blue'            # Initialize an arbitrary vertex as babyface.
            for rival in royal_rumble[wrestler]['rivals']:
                q.put(rival)
            while q.qsize() > 0:
                current = q.get()
                for rival in royal_rumble[current]['rivals']:
                    if royal_rumble[current]['color'] == 'white':
                        if royal_rumble[rival]['color'] == 'red':
                            royal_rumble[current]['color'] = 'blue'
                        elif royal_rumble[rival]['color'] == 'blue':
                            royal_rumble[current]['color'] = 'red'
                    elif royal_rumble[current]['color'] == royal_rumble[rival]['color']:
                        return False                # If two neighbors share a color, the graph is not bipartite.
                    if royal_rumble[rival]['color'] == 'white':
                        q.put(rival)
    babyfaces = []
    heels = []
    for wrestler in royal_rumble:
        if royal_rumble[wrestler]['color'] == 'blue':
            babyfaces.append(wrestler)
        else:
            heels.append(wrestler)
    return [babyfaces, heels]


# MAIN
if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:  # read and parse arguments from filename passed from cli.
        wrestler_count = int(f.readline())
        wrestlers = []
        for i in range(wrestler_count):
            wrestlers.append(f.readline().rstrip())
        rivalry_count = int(f.readline())
        rivalries = []
        for i in range(rivalry_count):
            rivalries.append(f.readline().split())

        graph = build_graph(wrestlers, rivalries)

        output = bfs_classify(graph)
        if output:
            print("Yes possible")
            print("Babyfaces: {}".format(" ".join(output[0])))
            print("Heels: {}".format(" ".join(output[1])))
        else:
            print("Impossible")
