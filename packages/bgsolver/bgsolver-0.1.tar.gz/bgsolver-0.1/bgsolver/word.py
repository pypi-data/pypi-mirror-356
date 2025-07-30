import importlib.resources

words_file = importlib.resources.read_text("bgsolver", "56k_valid_words.txt").rstrip()
WORD_LIST = [x.upper() for x in words_file.split('\n')]

class Word:
    def __init__(self, word, coordinates, orientation, overlap):
        self.word = word # string
        self.coordinates = coordinates # list of tuples
        self.orientation = orientation # 'horizontal' / 'vertical'
        self.overlap = overlap # tuple of slot overlapping with existing word

def word_priority(word: Word):
    difficulty_order = 'QJZXVKWYFBGHMPDUCLSNTOIRAE'
    score = 1
    for i, l in enumerate(difficulty_order):
        if l in word.word:
            score *= 1000*i
            break
    score -= len(word.word)
    return score
