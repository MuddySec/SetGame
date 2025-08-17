class GameState:
    def __init__(self, list_cartas, list_tablero, selected, sets, points, hint,mark):
        self.list_cartas = list_cartas
        self.list_tablero = list_tablero
        self.selected = selected
        self.sets = sets
        self.points = points
        self.hint = hint
        self.mark = mark

    def save(self, filename="estado_juego.pkl"):
        import pickle
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename="estado_juego.pkl"):
        import pickle
        with open(filename, "rb") as f:
            return pickle.load(f)