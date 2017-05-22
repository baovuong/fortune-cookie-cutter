import json
from nltk import word_tokenize
from random import randrange

# bigrams by default
DEFAULT_SIZE = 2


class MarkovState:

    def __init__(self, value):
        self.value = value
        self.transitions = {}

    def __eq__(self, other):
        return type(other) is MarkovState and self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __iter__(self):
        yield 'value', dict(self.value)

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

    def disconnect(self, state):
        if state in self.transitions:
            self.transitions[state] -= 1
            if self.transitions[state] <= 0:
                del self.transitions[state]


    def transition(self, steps=None):
        steps = randrange(self.count()) if steps == None else steps
        i = 0
        states = list(self.transitions.keys())
        while steps > 0:
            if self.transitions[states[i]] <= steps:
                i += 1
            steps -= self.transitions[states[i]]
        return states[i]

class MarkovChain:

    def __init__(self, root=None):        
        self.root = root
        self.states = [self.root]

    def add_state(self, new_state, prev=None):
        # check if prev is an existing state
        prev = self.root if prev == None else prev
        if prev == None:
            self.states.append(new_state)
            self.root = new_state
            return

        # look for prev
        for state in self.states:
            if prev == state:
                state.connect(new_state)
                if new_state not in self.states:
                    self.states.append(new_state)

    def __iter__(self):
        states = {}
        transitions = []
        for state in self.states:
            states[hash(state)] = dict(state)
            for transition in state.transitions:
                transitions.append({'from': hash(state), 'to': hash(transition), 'count': state.transitions[transition]})
        yield 'states', states
        yield 'transitions', transitions

class NGram:

    def __init__(self, words, size=DEFAULT_SIZE):
        self.words = words
        while size > len(self.words):
            self.words.insert(0, '<NULL>')

    def size(self):
        return len(self.words)

    __len__ = size

    def __eq__(self, other):

        if type(other) is not NGram or len(self) != len(other):
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

    def __iter__(self):
        yield 'words', self.words

    def can_transition_to(self, other):
        if len(self) != len(other):
            return False
        return self.words[1:] == other.words[:-1]
    
    def word(self):
        return self.words[len(self.words)-1] if len(self.words) > 0 else '' 

class NGramModel(MarkovChain):

    def __init__(self, n=DEFAULT_SIZE):
        super().__init__(MarkovState(NGram(['<START>'], n)))

    def add_state(self, new_state, prev_state=None):
        # look for the state it can connect to
        prev_state = self.root if prev_state == None else prev_state;
        valid = [s for s in self.states if s.value.can_transition_to(state.value)]
        if prev_state.value.can_transition_to(new_state.value):
            super().add(new_state, prev_state)
        if len(valid) == 0:
            return      
        super().add_state(state, valid[0])

    def add_ngram(self, new_value, prev_value=None):
        self.add_state(MarkovState(new_value), MarkovState(prev_value) if prev_value != None else None)

def words_from_sentence(sentence):
    words = word_tokenize(sentence)
    words.insert(0, '<START>')
    words.append('<END>')
    return words

def ngrams_from_words(words, n=DEFAULT_SIZE):
    ngrams = []
    for i in range(0, len(words)):
        ngrams.append(NGram(words[max(0, i-n+1):i+1], n))
    return ngrams

def ngrams_from_dict(structure):
    pass 

def ngrams_from_json(structure):
    pass 


if __name__ == '__main__':
    test = 'Hello. My name is Bao.'
    print(test)
    ngrams = ngrams_from_words(words_from_sentence(test))
    model = NGramModel()
    print(ngrams)
    for ngram in ngrams:
        model.add_ngram(ngram)
    print([s.value for s in model.states])
    sentence = []
    current = model.root
    while len(current.transitions) > 0 and current.value.word() != '<END>':
        print(current.value)
        sentence.append(current.value.word())
        current = current.transition()
    print(sentence)
    print(json.dumps(model.states, sort_keys=True,indent=2, separators=(',', ': ')))
    