class GameController:
    def __init__(self, num_players):
        self.num_players = num_players
        self.current_state = 'Settings'
        self.current_player = 0
        self.players = [f"Player {i+1}" for i in range(num_players)]
        self.winner = None

    def transition(self):
        if self.current_state == 'Settings':
            self.start_game()
        elif self.current_state == 'PlayerTurns':
            self.next_turn()
        elif self.current_state == 'GameEnd':
            print(f"Game over! The winner is {self.winner}")

    def start_game(self):
        print(f"Starting the game with {self.num_players} players...")
        self.current_state = 'PlayerTurns'
        self.next_turn()

    def next_turn(self):
        print(f"{self.players[self.current_player]}'s turn.")
        self.current_player = (self.current_player + 1) % self.num_players
        if self.current_player == 0:
            self.end_game()
        else:
            self.transition()

    def end_game(self):
        self.winner = self.players[(self.current_player - 1) % self.num_players]
        self.current_state = 'GameEnd'
        self.transition()


# Example usage
game = GameController(num_players=4)
game.transition()  # Start the game and proceed with turns
