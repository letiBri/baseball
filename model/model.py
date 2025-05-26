import copy
import itertools
import warnings
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapTeams = {}
        self._allTeams = []
        self._graph = nx.Graph()

        self._bestPath = []
        self._bestScore = 0

    def getYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._allTeams = DAO.getTeamsOfYear(year)
        # self._idMapTeams = {}
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
        myedges = list(itertools.combinations(self._allTeams, 2))  # data una lista, restituisce tutte le tuple possibili di n elementi
        self._graph.add_edges_from(myedges)
        salariesOfTeams = DAO.getSalaryOfTeams(year, self._idMapTeams)
        for e in self._graph.edges:  # e è una tupla che rappresenta l'arco
            self._graph[e[0]][e[1]]['weight'] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]  # sommo i salari delle due squadre dell'arco per trovare il peso
        # return len(self._graph.nodes), len(self._graph.edges)

    def getNeighborsSorted(self, source):
        vicini = nx.neighbors(self._graph, source)  # lista di nodi [v0, v1, v2, ...]
        # vicini = self._graph.neighbors(source)
        viciniTuple = []  # lista di tuple [(v0, p0), (v1, p1), ...]
        for v in vicini:
            viciniTuple.append((v, self._graph[source][v]['weight']))
        viciniTuple.sort(key=lambda x: x[1], reverse=True)  # ordino in ordine decrescente i pesi
        return viciniTuple

    def printGraphDetails(self):
        print(f"Grafo creato con {len(self._graph.nodes)} nodi e {len(self._graph.edges)} archi")

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)  # posso usare anche il metodo number_of_nodes(), number_of_edges()

    # per il punto 2
    def getBestPath(self, start):
        self._bestPath = []
        self._bestScore = 0
        vicini = self._graph.neighbors(start)
        parziale = [start]
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)  # con questa versione non ottengo l'informazione sul peso degli archi
            parziale.pop()
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):  # non mi serve passare start perchè è già in parziale
        # 1) verifico che parziale sia una soluzione e verifico se è migliore della best
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)

        # 2) verifico se posso aggiungere un nuovo nodo
        # 3) aggiungo nodo e faccio ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale and self._graph[parziale[-2]][parziale[-1]]["weight"] > self._graph[parziale[-1]][parziale[v]]["weight"]:
                # il peso deve essere strettamente crescente
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def score(self, listOfNodes):
        if len(listOfNodes) < 2:
            warnings.warn("Errore in score: attesa lista lunga almeno 2")
        totPeso = 0
        for i in range(len(listOfNodes) - 1):
            totPeso += self._graph[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return totPeso

    def getRandomNode(self):
        index = random.randint(0, self._graph.number_of_nodes() - 1)
        return list(self._graph.nodes)[index]

    def getBestPathV2(self, start):
        self._bestPath = []
        self._bestScore = 0
        vicini = self._graph.neighbors(start)

        parziale = [start]

        viciniTuples = [(v, self._graph[start][v]["weight"]) for v in vicini]  # equivale a fare un for
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        # for v in vicini:
        parziale.append(viciniTuples[0][0])
        self._ricorsioneV2(parziale)
        # parziale.pop()
        return self.getWeightsOfPath(self._bestPath), self._bestScore

    def _ricorsioneV2(self, parziale):
        # 1) verifico che parziale sia una soluzione e verifico se è migliore della best
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)

        # 2) verifico se posso aggiungere un nuovo nodo
        # 3) aggiungo nodo e faccio ricorsione
        vicini = self._graph.neighbors(parziale[-1])

        viciniTuples = [(v, self._graph[parziale[-1]][v]["weight"]) for v in vicini]
        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        for t in viciniTuples:
            if t[0] not in parziale and self._graph[parziale[-2]][parziale[-1]]["weight"] > t[1]:  # controllo che il nodo corrente non sia in parziale e che il peso associato sia crescente
                parziale.append(t[0])  # metto solo i nodi dentro a parziale
                self._ricorsioneV2(parziale)
                parziale.pop()
                return  # non ha senso guardare tutti gli altri archi che pesano meno, ammazzo l'esplorazione dopo aver aggiunto l'arco migliore

    def getWeightsOfPath(self, path):
        pathTuple = [(path[0], 0)]
        for i in range(1, len(path)):
            pathTuple.append((path[i], self._graph[path[i-1]][path[i]]["weight"]))
        return pathTuple
