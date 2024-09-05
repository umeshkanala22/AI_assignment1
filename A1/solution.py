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
        self.node = None

    def asr_corrector(self, environment):
        self.best_state = environment.init_state
        cost = environment.compute_cost(environment.init_state)
        self.node = Node(environment.init_state, cost)
        print(self.best_state)
        self.search(environment)



    def search(self, environment):
        isend=False
        while isend==False:
            node =self.node
            refstring=node.string
            print(self.best_state)
          
            currstring=node.string
            for i in range(0,len(currstring)):
                for key in self.phoneme_table:
                    if currstring[i:i+len(key)] == key:
                        for phoneme in self.phoneme_table[key]:
                            new_string = currstring[:i] + phoneme + currstring[i+len(key):]
                            new_cost = environment.compute_cost(new_string)
                            if(new_cost<self.node.cost):
                                self.best_state=new_string
                                print("my cost is low",new_string)
                                self.node.string=new_string
                                self.node.cost=new_cost
                             
                
            
            if(refstring==self.node.string):
                break
        print("I am Out of the while loop",self.best_state)
        for i in range(0,len(self.vocabulary)):
            new_string = self.vocabulary[i] +" "+ self.node.string
            new_cost = environment.compute_cost(new_string)
            if(self.node.cost>new_cost):
                self.node.cost=new_cost
                self.best_state=new_string
        self.node.string=self.best_state
        print("I am out of the 1st for loop",self.best_state)
                
        for i in range(0,len(self.vocabulary)):
            new_string = self.node.string+ " "+self.vocabulary[i]
            new_cost = environment.compute_cost(new_string)
            if(self.node.cost>new_cost):
                self.node.cost=new_cost
                self.best_state=new_string
        self.node.string=self.best_state
        print("I am out of the 2nd for loop",self.best_state)