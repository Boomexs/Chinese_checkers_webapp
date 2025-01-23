class GameController:
    def __init__(self, num_players):
        self.num_players = num_players
        self.current_state = 'Settings'
        self.current_player = 0
        self.players = [f"Player {i+1}" for i in range(num_players)]
        self.winner = None

    def start_game(self):
        self.current_state = 'PlayerTurns'
        self.current_player = 0  # Start with the first player

    def next_turn(self):
        if self.winner:
            self.current_state = 'GameEnd'
        else:
            self.current_player = (self.current_player + 1) % self.num_players

    def get_current_player(self):
        return self.current_player + 1  # Return 1-based player index

    def set_winner(self, player):
        self.winner = player
        self.current_state = 'GameEnd'
