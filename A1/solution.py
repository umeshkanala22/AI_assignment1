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
        self.phoneme_table = {}
        for key, values in phoneme_table.items():
            for value in values:
                if value not in self.phoneme_table:
                    self.phoneme_table[value] = [key]
                else:
                    self.phoneme_table[value].append(key)
        self.vocabulary = vocabulary
        self.best_state = None
        self.k = 1
        self.heap = []
        self.node = None

    # def heap_push(self, node):
    #     if len(self.heap) < self.k:
    #         heapq.heappush(self.heap, node)
    #     elif node.cost < self.heap[-1].cost:
    #         self.heap[-1]=node

    def asr_corrector(self, environment):
        self.best_state = environment.init_state
        cost = environment.compute_cost(environment.init_state)
        self.node = Node(environment.init_state, cost)
        print(self.best_state)
        self.search(environment)



    def search(self, environment):
        print(self.phoneme_table)
        isend=False
        start=0
        while isend==False:
            node =self.node
            flag1=False
            print(self.best_state)
          
            currstring=node.string
            for i in range(start,len(currstring)):
                for key in self.phoneme_table:
                    if currstring[i:i+len(key)] == key:
                        for phoneme in self.phoneme_table[key]:
                            new_string = currstring[:i] + phoneme + currstring[i+len(key):]
                            new_cost = environment.compute_cost(new_string)
                            if(new_cost<node.cost):
                                self.best_state=new_string
                                print(new_string)
                                self.node=Node(new_string,new_cost)
                                start=i
                                flag1=True
                                break
                    if flag1:
                        break
                if flag1:
                    break
            
            if(node.string==self.node.string):
                break
        print("I am Out of the while loop",self.best_state)
        print(self.vocabulary)
        for i in range(0,len(self.vocabulary)):
            new_string = self.vocabulary[i] + self.node.string
            new_cost = environment.compute_cost(new_string)
            if(self.node.cost>new_cost):
                self.node.cost=new_cost
                self.best_state=new_string
        self.node.string=self.best_state
        print("I am out of the 1st for loop",self.best_state)
                
        for i in range(0,len(self.vocabulary)):
            new_string = self.node.string+self.vocabulary[i]
            new_cost = environment.compute_cost(new_string)
            if(self.node.cost>new_cost):
                self.node.cost=new_cost
                self.best_state=new_string
        self.node.string=self.best_state
        print("I am out of the 2nd for loop",self.best_state)
                
        
            
            # node =self.node
            # currstring=node.string
            # for i in range(self.vocabulary.size):
            #     new_string = self.vocabulary[i] + currstring
            #     new_cost = environment.compute_cost(new_string)
            #     if(new_cost<node.cost):
            #         new_node = Node(new_string,new_cost)
            #         self.heap_push(new_node)
            #     new_string = currstring + self.vocabulary[i]
            #     new_cost = environment.compute_cost(new_string)
            #     if(new_cost<node.cost):
            #         new_node = Node(new_string,new_cost)
            #         self.heap_push(new_node)
            # self.best_state = self.heap[0].string if self.heap else None
            # qw=qw+1