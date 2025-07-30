class PublicGameUser:
    def __init__(self, username="", profile_picture_url="", score=0, date_started=None, wins=0, loses=0, **kwargs):
        self.username = username
        self.profile_picture_url = profile_picture_url
        self.score = score
        self.date_started = date_started
        self.wins = wins
        self.loses = loses
