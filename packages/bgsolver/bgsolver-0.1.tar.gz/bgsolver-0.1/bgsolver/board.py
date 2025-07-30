import pandas as pd
from bgsolver.word import Word

class Board:
    all_letters = list('JKQXZ'*2 + 'BCFHMPVWY'*3 + 'G'*4 + 'L'*5 + 'DSU'*6 + \
                       'N'*8 + 'TR'*9 + 'O'*11 + 'I'*12 + 'A'*13 + 'E'*18)
    
    def __init__(self):
        self.board = pd.DataFrame(index=range(-100,100), columns=range(-100,100))
        self.letters = Board.all_letters
        self.words_made = []

    def room_for_word(self, word: Word):        
        must_be_free = []
        must_be_free.extend(word.coordinates)
        if word.overlap:
            must_be_free.pop(must_be_free.index(word.overlap))
            if word.orientation == 'horizontal':
                for row, col in word.coordinates:
                    if col != word.overlap[1]:
                        must_be_free.append((row+1, col))    
                        must_be_free.append((row-1, col))
                first_row, first_col = word.coordinates[0] 
                must_be_free.append((first_row, first_col-1))    
                last_row, last_col = word.coordinates[-1]
                must_be_free.append((last_row, last_col+1))
            else: # word is vertical
                for row, col in word.coordinates:
                    if row != word.overlap[0]:
                        must_be_free.append((row, col+1))    
                        must_be_free.append((row, col-1))
                first_row, first_col = word.coordinates[0] 
                must_be_free.append((first_row-1, first_col))    
                last_row, last_col = word.coordinates[-1]
                must_be_free.append((last_row+1, last_col))
        for row, col in must_be_free:
            if not pd.isna(self.board.at[row, col]):
                return False
        return True
