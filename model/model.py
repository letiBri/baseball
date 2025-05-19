import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapTeams = {}
        self._allTeams = []
        self._graph = nx.Graph()

    def getYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._allTeams = DAO.getTeamsOfYear(year)
        self._idMapTeams = {}
        for team in self._allTeams:
            self._idMapTeams[team.ID] = team
        return self._allTeams

    def buildGraph(self, year):
        self._graph.clear()
        if len(self._allTeams) == 0:
            print("Lista squadre vuota")
            return
        self._graph.add_nodes_from(self._allTeams)

        # for n1 in self._graph.nodes:
        #     for n2 in self._graph.nodes:
        #         if n1 != n2:
        #             self._graph.add_edge(n1, n2)
        # oppure
        myedges = itertools.combinations(self._allTeams, 2)  # data una lista, restituisce tutte le tuple possibili di n elementi
        self._graph.add_edges_from(myedges)
        salariesOfTeams = DAO.getSalaryOfTeams(year, self._idMapTeams)
        for e in self._graph.edges:  # e è una tupla che rappresenta l'arco
            self._graph[e[0]][e[1]]['weight'] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]  # sommo i salari delle due squadre dell'arco per trovare il peso
        return len(self._graph.nodes), len(self._graph.edges)

    def printGraphDetails(self):
        print(f"Grafo creato con {len(self._graph.nodes)} nodi e {len(self._graph.edges)} archi")
