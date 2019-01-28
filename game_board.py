'''
A class that implements a simple Bao game board and the rules for taking a turn.
'''

class GameBoard:
    def __init__(self, game='standard'):
        self.game = game
        self.pits = {
            1: {
                'front': [0] * 8,
                'back': [0] * 8
            },
            2: {
                'front': [0] * 8,
                'back': [0] * 8
            }
        }
        self.new_game()

    def get_copy(self):
        new_board = GameBoard()
        for player in self.pits:
            for row in self.pits[player]:
                for pit_idx, stones in enumerate(self.pits[player][row]):
                    new_board.pits[player][row][pit_idx] = stones
        return new_board

    def __str__(self):
        rows = {
            player: {
                row: ' # '.join([str(num).zfill(2) for num in self.pits[player][row]]) for row in self.pits[player]
            } for player in self.pits
        }
        return ''.join([
            ''.join(['#']*(5*8 + 1)) + '\n',
            '    '.join(['#']*9) + '\n',
            '# ' + rows[1]['back'] + ' #\n',
            '    '.join(['#']*9) + '  Player 1\n',
            '# ' + rows[1]['front'] + ' #\n',
            '    '.join(['#']*9) + '\n',
            ''.join(['#']*(5*8 + 1)) + '\n',
            '    '.join(['#']*9) + '\n',
            '# ' + rows[2]['front'] + ' #\n',
            '    '.join(['#']*9) + '  Player 2\n',
            '# ' + rows[2]['back'] + ' #\n',
            '    '.join(['#']*9) + '\n',
            ''.join(['#']*(5*8 + 1)) + '\n',
        ])

    def new_game(self):
        if self.game == 'standard':
            for player in self.pits:
                for row in self.pits[player]:
                    self.pits[player][row] = [2] * 8
            self.pits[1]['front'][0] = 0
            self.pits[2]['front'][7] = 0

    def take_turn(self, player, row, pit_idx, step_callback=None):
        stones_taken = 0
        next_step = self._step(player, row, pit_idx, 0, stones_taken)
        if next_step is None:
            return None
        if step_callback is not None:
            step_callback(next_step)
        while next_step is not None:
            if step_callback is not None:
                step_callback(next_step)
            stones_taken = next_step[4]
            next_step = self._step(*next_step)
        return stones_taken

    def get_winner(self):
        for player in self.pits:
            if max(self.pits[player]['back'] + self.pits[player]['front']) < 2 or max(self.pits[player]['front']) < 1:
                return player%2+1
        return None

    def _step(self, player, row, pit_idx, stones, stones_taken):
        if stones > 0:
            self.pits[player][row][pit_idx] += 1
            stones -= 1
        if stones == 0 and self.pits[player][row][pit_idx] <= 1:
            return None
        if stones == 0:
            stones = self.pits[player][row][pit_idx]
            self.pits[player][row][pit_idx] = 0
            if row == 'front':
                stones += self.pits[player%2+1]['front'][pit_idx]
                stones_taken += self.pits[player%2+1]['front'][pit_idx]
                self.pits[player%2+1]['front'][pit_idx] = 0
        next_row = 'front' if row == 'back' and ((player == 1 and pit_idx == 7) or (player == 2 and pit_idx == 0))\
            else 'back' if row == 'front' and ((player == 1 and pit_idx == 0) or (player == 2 and pit_idx == 7))\
            else row
        next_pit_idx = pit_idx+1 if (player == 1 and row == 'back') or (player == 2 and row == 'front')\
            else pit_idx-1
        next_pit_idx = 0 if next_pit_idx == -1\
            else 7 if next_pit_idx == 8\
            else next_pit_idx
        return (player, next_row, next_pit_idx, stones, stones_taken)
