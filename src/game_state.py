class GameState:
    def __init__(self,
                list_cartas = None,
                list_tablero = None,
                cartas = None,
                sets = None,
                selected = None,
                points = 0,
                hint = False,
                hint_card = None,
                ended = False,
                mark = None,
                hint_counts = 0,
                error_counts = 0,
                change3_counts = 0,
                time = 0,
                minutes = 0,
                seconds = 0):
        
        self.list_cartas = list_cartas if list_cartas is not None else []
        self.list_tablero = list_tablero if list_tablero is not None else []
        self.selected = selected if selected is not None else []
        self.sets = sets if sets is not None else []
        self.cartas = cartas if cartas is not None else []
        self.points = points
        self.hint = hint
        self.hint_card = hint_card
        self.ended = ended
        self.mark = mark
        self.hint_counts = hint_counts
        self.error_counts = error_counts
        self.change3_counts = change3_counts
        self.time = time
        self.minutes = minutes
        self.seconds = seconds

    def save(self, filename="estado_juego.pkl"):
        import pickle
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename="estado_juego.pkl"):
        import pickle
        with open(filename, "rb") as f:
            return pickle.load(f)
        

    def final_score(self):
        return 1000 + self.points*100 - ((self.minutes*60+self.seconds)*3) - (self.hint_counts*36) - (self.change3_counts*24) - (self.error_counts*15)