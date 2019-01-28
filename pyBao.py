
class PyBao:
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
        new_board = PyBao()
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
            '    '.join(['#']*9) + '\n',
            '# ' + rows[1]['front'] + ' #\n',
            '    '.join(['#']*9) + '\n',
            ''.join(['#']*(5*8 + 1)) + '\n',
            '    '.join(['#']*9) + '\n',
            '# ' + rows[2]['front'] + ' #\n',
            '    '.join(['#']*9) + '\n',
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

    def take_turn(self, player, row, pit_idx, tryout=False):
        if not tryout:
            print('Picking up the stones and taking the turn ...')
        stones_taken = 0
        next_step = self._step(player, row, pit_idx, 0, stones_taken)
        if next_step is None:
            return None
        if not tryout:
            print('Starting with {0} stones.\n'.format(next_step[3]))
        while next_step is not None:
            if not tryout:
                print(self)
                print('Next up pit number {0} in the {1}.\nStones in hand: {2}\n'.format(
                    next_step[2]+1, next_step[1], next_step[3]
                ))
            stones_taken = next_step[4]
            next_step = self._step(*next_step)
        if not tryout:
            print(self)
            print('Turn finished and {0} stones taken.\n'.format(stones_taken))
        if tryout:
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

def get_turn(board, player):
    print('It\'s your turn player {0}. Choose your row:'.format(player))
    row = None
    while row != 'b' and row != 'f':
        row = input('back/front (\'b\'/\'f\') > ')
    row = 'back' if row == 'b' else 'front' if row == 'f' else None
    print('Choose your pit number:')
    pit_idx = None
    while pit_idx is None or int(pit_idx) not in range(1, 9):
        pit_idx = input('[1-8] > ')
    pit_idx = int(pit_idx)-1
    if board.pits[player][row][pit_idx] <2:
        print('This pit contains less than two stones!')
        return get_turn(board, player)
    return (player, row, pit_idx)

def get_best_turn(board, player):
    print('Player {}s computer brain is thinking ...'.format(player))
    turns = []
    for row in board.pits[player]:
        for pit_idx in range(len(board.pits[player][row])):
            test_board = board.get_copy()
            turn_result = test_board.take_turn(player, row, pit_idx, tryout=True)
            if turn_result is not None:
                turns.append([(player, row, pit_idx), turn_result])
    result = max(turns, key=lambda turn: turn[1])
    print('Chose pit {0} in the {1}.\n'.format(result[0][2]+1, result[0][1]))
    return result[0]

board = PyBao()
print('Welcome to PyBao. This is your starting position:\n')
print(board)
active_player = 1
print('Player {0}, do you want to play against a human or the computer?'.format(active_player))
choice = None
while choice != 'h' and choice != 'c':
    choice = input('human/computer (\'h\'/\'c\') > ')
while board.get_winner() is None:
    if choice == 'c' and active_player == 2:
        board.take_turn(*get_best_turn(board, active_player))
    else:
        board.take_turn(*get_turn(board, active_player))
    active_player = active_player%2+1
print('Congratulations, player {0}, you have won!'.format(board.get_winner()))
