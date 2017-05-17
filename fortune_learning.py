from nltk import word_tokenize
from random import randrange

class MarkovState:
    def __init__(self, value):
        self.value = value
        self.transitions = {}

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def count(self):
        c = 0
        for key in self.transitions:
            c += self.transitions[key]
        return c

    def connect(self, state):
        if state in self.transitions:
            self.transitions[state] += 1
        else:
            self.transitions[state] = 1

    def delete_transition(self, state):
        if state in self.transitions:
            self.transitions[state] -= 1
            if self.transitions[state] <= 0:
                del self.transitions[state]


    def transition(self, steps=None):
        steps = randrange(self.count()) if steps == None else steps
        i = 0
        states = self.transitions.keys()
        while steps > 0:
            if self.transitions[states[i]] <= steps:
                i += 1
            steps -= self.transitions[states[i]]
        return states[i]

class MarkovChain:
    
    def __init__(self, root):
        self.states = []
        self.root = root
    
    def add_state(self, parent):
        pass 

class NGram:
    def __init__(self, words, size=0):
        self.words = words
        while size > len(self.words):
            self.words.insert(0, '<NULL>')

    def size(self):
        return len(self.words)

    __len__ = size

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(0, self.size()):
            if self.words[i] != other.words[i]:
                return False
        return True

    def __str__(self):
        return '(' + ' '.join(self.words) + ')'

    __repr__ = __str__

    def __hash__(self):
        return hash(str(self))
    
    def can_transition_to(self, other):
        if len(self) != len(other):
            return False 
        return self.words[:-1] == other.words[1:]

class NGramModel(MarkovChain):
    pass 
def words_from_sentence(sentence):
    words = word_tokenize(sentence)
    words.insert(0, '<START>')
    words.append('<END>')
    return words

def ngrams_from_words(words, n=2):
    ngrams = []
    for i in range(0, len(words)):
        ngrams.append(NGram(words[max(0, i-n+1):i+1], n))
    return ngrams



if __name__ == '__main__':
    test = 'watashi wa bitch desu.'
    print(test)
    ngrams = ngrams_from_words(words_from_sentence(test))
    for ngram in ngrams:
        print(ngram)
