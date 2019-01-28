'''
This is a text-based Bao game for 1 or 2 players in a command-line console. The AI is beatable but challenging.
'''
from game_board import GameBoard

print(
    '  _____       ____              \n',
    ' |  __ \     |  _ \             \n',
    ' | |__) |   _| |_) | __ _  ___  \n',
    ' |  ___/ | | |  _ < / _` |/ _ \ \n',
    ' | |   | |_| | |_) | (_| | (_) |\n',
    ' |_|    \__, |____/ \__,_|\___/ \n',
    '         __/ |                  \n',
    '        |___/                   \n'
)

board = GameBoard()

def step_function(step):
    print(board)
    print('Next up pit number {0} in the {1}.\nStones in hand: {2}\n'.format(
        step[2]+1, step[1], step[3]
    ))

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
    print('Picking up the stones and taking the turn ...')
    return (player, row, pit_idx, step_function)

def get_best_turn(board, player):
    print('Player {0}s computer brain is thinking ...'.format(player))
    turns = []
    for row in board.pits[player]:
        for pit_idx in range(len(board.pits[player][row])):
            test_board = board.get_copy()
            turn_result = test_board.take_turn(player, row, pit_idx)
            if turn_result is not None:
                turns.append([(player, row, pit_idx, step_function), turn_result])
    result = max(turns, key=lambda turn: turn[1])
    print('Chose pit {0} in the {1}.\n'.format(result[0][2]+1, result[0][1]))
    return result[0]

print('Welcome to PyBao. This is your starting position:\n')
print(board)
active_player = 1
print('Player {0}, do you want to play against a human or the computer?'.format(active_player))
choice = None
while choice != 'h' and choice != 'c':
    choice = input('human/computer (\'h\'/\'c\') > ')
turn_result = None
while board.get_winner() is None:
    if choice == 'c' and active_player == 2:
        turn_result = board.take_turn(*get_best_turn(board, active_player))
    else:
        turn_result = board.take_turn(*get_turn(board, active_player))
    print(board)
    print('Turn finished and {0} stones taken.\n'.format(turn_result))
    active_player = active_player%2+1
if choice == 'c':
    if board.get_winner() == 1:
        print('Congratulations, you have beaten the computer.')
    else:
        print('The computer wins!')
else:
    print('Congratulations, player {0}, you have won!'.format(board.get_winner()))
