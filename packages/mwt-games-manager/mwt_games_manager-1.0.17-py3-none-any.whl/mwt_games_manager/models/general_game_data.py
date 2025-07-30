class GeneralGameData:
    def __init__(self, username="", game_name="", score=0, date_started=None, wins=0, loses=0):
        self.username = username
        self.game_name = game_name
        self.score = score
        self.date_started = date_started
        self.wins = wins
        self.loses = loses
