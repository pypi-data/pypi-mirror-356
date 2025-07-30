import random
import pandas as pd
from bgsolver.board import Board
from bgsolver.word import Word, word_priority, WORD_LIST

class Player:
    def __init__(self, letters=[]):
        self.letters = letters

    def get_letters(self, board, letters='', mode='manual'):
        new_letters = letters
        while not(new_letters.isalpha()):
            if mode == 'manual':
                new_letters = input('Enter letters:\n')
            else: ## mode == 'auto'
                try:
                    new_letters = random.choice(board.letters)
                except IndexError:
                    print('You Win!')
                    return False
                board.letters.remove(new_letters)
            
            if new_letters.isalpha():
                self.letters.extend(list(new_letters.upper()))
            elif new_letters == '00':
                return False
            else:
                print('Invalid input. Only letters are allowed.')
        return True
    
    def can_i_spell(self, word: str):
        for l in set(word):
            if word.count(l) > self.letters.count(l):
                return False
        return True

    def possible_words(self, board: Board):
        possible_words = []
        if board.words_made == []:
            for w in WORD_LIST:
                if self.can_i_spell(w):
                    new_coords = list(zip([0]*len(w), range(len(w))))
                    possible_words.append(Word(w, new_coords, 'horizontal', None))
        else:    
            for w in board.words_made:
                for pos, l in zip(w.coordinates, w.word):
                    self.letters.append(l)
                    new_words = [word for word in WORD_LIST \
                                if l in word and self.can_i_spell(word)]
                    self.letters.pop(-1)
                    for word in new_words:
                        idx = word.index(l)
                        if w.orientation == 'horizontal':
                            new_orient = 'vertical'
                            new_coords = list(zip(
                                range(pos[0]-idx, pos[0]-idx+len(word)),
                                [pos[1]]*len(word)))
                        else:
                            new_orient = 'horizontal'
                            new_coords = list(zip([pos[0]]*len(word),
                                    range(pos[1]-idx, pos[1]-idx+len(word))))
                        possible_words.append(Word(word, new_coords,
                                                new_orient, pos))
        return [w for w in possible_words if board.room_for_word(w)]

    def choose_word(self, board: Board, priority=False):
        choices = self.possible_words(board)
        if choices == []:
            return None
        if priority:
            choices.sort(key=word_priority)
        else:
            choices.sort(key=lambda x: -len(x.word))
        return choices[0]
    
    def make_word(self, word: Word, board: Board):
        if board.room_for_word(word):
            for pos, l in zip(word.coordinates, word.word):
                if pd.isna(board.board.at[pos[0], pos[1]]):
                    board.board.at[pos[0], pos[1]] = l
                    self.letters.pop(self.letters.index(l))
            board.words_made.append(word)
            print('Making', word.word, 'at position', word.coordinates[0])
            print('\n')
            print(board.board.dropna(axis=0, how='all').dropna(axis=1, how='all').fillna(' '))
            print(self.letters)
            return word

    def break_word(self, board: Board): # the last word made
        last_word = board.words_made.pop(-1)
        # give 'QQQ' as first input, tries to break_word when there are none..
        for row, col in last_word.coordinates:
            if (row, col) != last_word.overlap:
                self.letters.append(board.board.at[row, col])
                board.board.at[row, col] = pd.NA
        print('Breaking', last_word.word, 'at position',
              last_word.coordinates[0])
        print('\n')
        print(board.board.dropna(axis=0, how='all').dropna(axis=1, how='all').fillna(' '))
        print(self.letters)
        return last_word

    def reorder(self, board: Board, mode='manual'):
        # stuck with leftover letter. how to deal?
        # break last word, apply priority word building, see if resolves.
        # if not, reset. break last 2 words, apply priority building, see if resolves.
        # repeat until resolved. but after each iteration, stop and ask user if it should keep trying.
        #  (user would answer no if new letters have come in from someone calling peel)
        #  so if answer is no, should return the player to game loop, leading to get_letters call
        original_self_letters = self.letters[:]
        original_board = board.board.copy()
        original_words_made = board.words_made[:]
        print('Attempting to reorder the board...')

        break_words = 1
        while self.letters != []:
            for i in range(break_words):
                try:
                    self.break_word(board)
                except IndexError:
                    print('No words have been made yet.')
                    return False

            while self.letters != []:
                new = self.choose_word(board, priority=True)
                if new:
                    if not self.make_word(new, board):
                        # terminate due to infinite loop
                        return False
                elif break_words == len(original_words_made): 
                    # whole board has been broken. 
                    # try reordering the board from its current state...
                    user_input = 'reorder' if mode != 'manual' else input('Whole board has been broken. Attempt reordering from new state?\n')
                    if user_input != '': # ^ force return False to terminate infinite loop during auto mode.
                        return False
                    else:
                        return self.reorder(board, mode=mode)
                else:
                    break

            if self.letters != []:
            # tried breaking last and fixing, didnt work, stuck with leftover letter and no words to make again.
            # reset, try the whole process with 2 breaks this time
                self.letters = original_self_letters[:]
                board.board = original_board.copy()
                board.words_made = original_words_made[:]
                break_words += 1

                user_input = '' if mode != 'manual' else input(f'Continue trying to reorder? (iter={break_words})\nEnter: Yes   Any key: No\n')
                if user_input != '':
                    # user doesn't want to keep trying, function returns
                    return False # was reorder attempt successful? no. 
                                 #  but player prob has more letters to input and is cancelling the attempt
                
            # otherwise, attempt to reorder was successful, letters == [], loop will end now
        print('Reorder attempt successful!')
        return True # reorder attempt succesful
    