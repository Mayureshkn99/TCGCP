class PlayerIterator:
    '''Creates iterator to cycle through active players'''

    def __init__(self, players):
        self.active_players = list(range(players))

    def __iter__(self):
        self.pos = 0
        return self
    
    def __next__(self):
        self.pos += 1
        if self.pos == len(self.active_players):
            self.pos = 0
        return self.active_players[self.pos]
    
    def set_loser(self, loser):
        self.pos = self.active_players.index(loser)

    def player_wins(self, winner):
        self.active_players.remove(winner)