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
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None
        self.k = 10
        self.heap = []

    def asr_corrector(self, environment):
        self.best_state = environment.init_state
        print("this is the best state before training", self.best_state)
        cost = environment.compute_cost(environment.init_state)
        print("this is the cost before  training",cost)
        node = Node(environment.init_state, cost)
        self.heap_push(node)
        self.search(environment)
        # environment.best_state = self.best_state.string

    def heap_push(self, node):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, node)
        else:
            heapq.heappushpop(self.heap, node)

    def search(self, environment):
        while self.heap:
            node = heapq.heappop(self.heap)
            currstring=node.string
            for i in range(len(currstring)):
                if currstring[i] in self.phoneme_table:
                    for phoneme in self.phoneme_table[currstring[i]]:
                        new_string = currstring[:i] + phoneme + currstring[i+1:]
                        new_cost = environment.compute_cost(new_string)
                        if(new_cost<node.cost):
                            new_node = Node(new_string,new_cost)
                            self.heap_push(new_node)
                

            self.best_state = heapq.top().string
        
        self.heap=[heapq.top()]
        heapq.clear()
        while self.heap:
            node = heapq.heappop(self.heap)
            currstring=node.string
            for i in range(-1,self.vocabulary.size):
                for j in range(i-1,self.vocabulary.size):
                    if(i!=-1):
                        new_string=self.vocabulary[i]+currstring
                    if(j!=i-1):
                        new_string=currstring+self.vocabulary[j]
                    new_cost = environment.compute_cost(new_string)
                    if(new_cost<node.cost):
                        new_node = Node(new_string,new_cost)
                        self.heap_push(new_node)
        
            environment.best_state = heapq[0].string
        print("this is the beat after update",heapq[0].string)
