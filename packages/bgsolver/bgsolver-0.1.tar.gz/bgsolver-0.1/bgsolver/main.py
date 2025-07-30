import time
import random
import pandas as pd
from bgsolver.board import Board
from bgsolver.word import Word
from bgsolver.player import Player

pd.set_option('display.max_rows', None,
              'display.max_columns', None,
              'display.width', None)

def game_manual():
    board = Board()
    player = Player()
    while True: 
        original_count = len(player.letters)
        word = player.choose_word(board)
        if word:
            player.make_word(word, board)
        if len(player.letters) == 0:
            if not player.get_letters(board): break
        elif len(player.letters) == original_count:
            # stuck with leftover letter. try reordering
            if player.reorder(board):
                # player has used all letters, next iter will ask for more
                pass
            else:
                if not player.get_letters(board): break
                # player must have cancelled reorder() to input new letters

def game_auto(seed=random.randint(0,10000)):
    board = Board()
    player = Player()
    start = time.time()
    random.seed(seed)

    # choose first 21 letters
    player.letters = random.sample(board.letters, 21)
    # remove from board's letters
    for l in player.letters:
        board.letters.remove(l)
    
    while True: 
        current_time = time.time() - start
        print(f'Letters remaining: {len(board.letters)}',
              f'Time: {round(current_time, 2)}s',
              sep='\n')

        original_count = len(player.letters)
        word = player.choose_word(board)
        if word:
            player.make_word(word, board)
        if len(player.letters) == 0:
            if not player.get_letters(board, mode='auto'):
                total_time = time.time() - start
                print(f'Total time: {round(total_time, 2)}s')
                break
        elif len(player.letters) == original_count:
            # stuck with leftover letter. try reordering
            if player.reorder(board, mode='auto'):
                # player has used all letters, next iter will ask for more
                pass
            else:
                # reorder() returned False, stuck in infinite loop
                print('BGSolver was unable to resolve the board.')
                total_time = time.time() - start
                print(f'Total time: {round(total_time, 2)}s')
                break

def main():
    print(
r'''
############################################################################################
|  ____                                                                                    |
| |  _ \                                                                                   |
| | |_) |   __ _   _ __     __ _   _ __     __ _    __ _   _ __    __ _   _ __ ___    ___  |
| |  _ <   / _` | | '_ \   / _` | | '_ \   / _` |  / _` | | '__|  / _` | | '_ ` _ \  / __| |
| | |_) | | (_| | | | | | | (_| | | | | | | (_| | | (_| | | |    | (_| | | | | | | | \__ \ |
| |____/   \__,_| |_| |_|  \__,_| |_| |_|  \__,_|  \__, | |_|     \__,_| |_| |_| |_| |___/ |
|                                                   __/ |                                  |
|                                                  |___/                                   |
|                         _____           _                                                |
|                        / ____|         | |                                               |
|                       | (___     ___   | | __   __   ___   _ __                          |
|                        \___ \   / _ \  | | \ \ / /  / _ \ | '__|                         |
|                        ____) | | (_) | | |  \ V /  |  __/ | |                            |
|                       |_____/   \___/  |_|   \_/    \___| |_|                            |
|                                                                                          |
############################################################################################
''')
    mode = ''
    while not(mode.isnumeric()):
        mode = input(
'''Select game mode:
1 : Enter letters manually.
2+: Draw letters randomly until the game is complete (144 letters).
    - the number you enter will be used as the random seed
''')

    if mode == '1':
        game_manual()
    else:
        game_auto(int(mode))

myword = Word('FLABBERGASTED',
              [(0, i) for i in range(len('FLABBERGASTED'))],
              'horizontal',
              None)
next = Word('A',
            [(0,-2)],
            'horizontal',
            (5,5))

if __name__ == '__main__':
    main()
