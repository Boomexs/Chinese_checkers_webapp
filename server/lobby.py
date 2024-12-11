class lobby():
    def __init__(self, lobby_name: str, needed_players: int):
        self.name = lobby_name
        self.players = []
        self.player_count = needed_players
        self.Board = None # create a board object for x players; x=needed_players

    def add_player(self, player):
        if len(self.players) < self.player_count:
            self.players.append(player)
            return True
        return False

    def remove_player(self, player):
        self.players.remove(player)

    def is_full(self):
        return len(self.players) >= self.player_count