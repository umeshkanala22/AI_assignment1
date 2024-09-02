# class Agent(object):
#     def __init__(self, phoneme_table, vocabulary) -> None:
#         """
#         Your agent initialization goes here. You can also add code but don't remove the existing code.
#         """
#         self.phoneme_table = phoneme_table
#         self.vocabulary = vocabulary
#         self.best_state = None

#     def asr_corrector(self, environment):
#         """
#         Your ASR corrector agent goes here. Environment object has following important members.
#         - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
#         - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

#         Your agent must update environment.best_state with the corrected text discovered so far.
#         """
#         self.best_state = environment.init_state
#         cost = environment.compute_cost(environment.init_state)

import heapq

class Node(object):
    def __init__(self, string, cost):
        self.string = string
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        self.phoneme_table = {value: key for key, values in phoneme_table.items() for value in values}
        self.vocabulary = vocabulary
        self.best_state = None
        self.k = 3
        self.heap = []

    def asr_corrector(self, environment):
        self.best_state = environment.init_state
        cost = environment.compute_cost(environment.init_state)
        node = Node(environment.init_state, cost)
        self.heap_push(node)
        self.search(environment)
        environment.best_state = self.best_state

    def heap_push(self, node):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, node)
        else:
            heapq.heappushpop(self.heap, node)

    def search(self, environment):
        print(self.phoneme_table)
        qw=0
        while self.heap and qw<1000000:
            print(qw)

            node = heapq.heappop(self.heap)
            currstring=node.string
            for i in range(len(currstring)):
                for key in self.phoneme_table:
                    if currstring[i:i+len(key)] == key:
                        for phoneme in self.phoneme_table[key]:
                            new_string = currstring[:i] + phoneme + currstring[i+len(key):]
                            new_cost = environment.compute_cost(new_string)
                            if(new_cost<node.cost):
                                new_node = Node(new_string,new_cost)
                                self.heap_push(new_node)
            self.best_state = self.heap[0].string if self.heap else None
            qw=qw+1

        self.heap = [Node(self.best_state, environment.compute_cost(self.best_state))]
        print(self.best_state)
        qw=0
        while self.heap and qw<1000000:
            print(qw)
            node = heapq.heappop(self.heap)
            currstring=node.string
            for i in range(self.vocabulary.size):
                new_string = self.vocabulary[i] + currstring
                new_cost = environment.compute_cost(new_string)
                if(new_cost<node.cost):
                    new_node = Node(new_string,new_cost)
                    self.heap_push(new_node)
                new_string = currstring + self.vocabulary[i]
                new_cost = environment.compute_cost(new_string)
                if(new_cost<node.cost):
                    new_node = Node(new_string,new_cost)
                    self.heap_push(new_node)
            self.best_state = self.heap[0].string if self.heap else None
            qw=qw+1