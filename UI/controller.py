import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedTeam = None

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text("Attenzione: selezionare un anno", color="red"))
            self._view.update_page()
            return
        year = self._view._ddAnno.value
        self._model.buildGraph(int(year))
        numNodi, numArchi = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {numNodi} vertici e {numArchi} archi."))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        if self._selectedTeam is None:  # quello selezionato dal dropdown
            self._view._txt_result.controls.append(ft.Text("Attenzione: selezionare un team", color="red"))
            self._view.update_page()
            return
        # [(v0, p0), (v1, p1), ...] # lista di tuple dove il primo elemento è un nood e il secondo il peso
        viciniSorted = self._model.getNeighborsSorted(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il vicinato conta {len(viciniSorted)} squadre."))
        for v in viciniSorted:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} -- peso: {v[1]}"))
        self._view.update_page()

    # per il punto 2
    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        if self._selectedTeam is None:
            self._view._txt_result.controls.append(ft.Text("Attenzione: selezionare un team", color="red"))
            self._view.update_page()
            return
        path, score = self._model.getBestPathV2(self._selectedTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"trovato un cammino che parte da {self._selectedTeam} con somma dei pesi uguali a {score}"))
        for v in path:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]} -- peso: {v[1]}"))
        self._view.update_page()


    def handleDDYearSelection(self, e):
        self._view._txtOutSquadre.controls.clear()
        if self._view._ddAnno.value is None or self._view._ddAnno.value == "":
            self._view._txtOutSquadre.controls.append(ft.Text("Attenzione: selezionare un anno", color="red"))
            self._view.update_page()
            return
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.append(ft.Text(f"Squadre presenti nell'anno {self._view._ddAnno.value} = {len(teams)} "))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode} ({t.name})"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(key=t.teamCode, data=t, on_click=self.readDDTeams))
        self._view.update_page()

    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        self._selectedTeam = e.control.data
        print(f"readDDTeams called -- {self._selectedTeam}")

    def fillDDYear(self):
        years = self._model.getYears()
        # yearsDD = []
        # for year in years:
        #     yearsDD.append(ft.dropdown.Option(year))
        yearsDD = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = yearsDD
        self._view.update_page()
