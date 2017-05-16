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

class MarkovState:
    def __init__(self, value):
        self.value = value
        self.transitions = {}

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def add_transition(self, state):
        if state in self.transitions:
            self.transitions[state] += 1
        else:
            self.transitions[state] = 1
