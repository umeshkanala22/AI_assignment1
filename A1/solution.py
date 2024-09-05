class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None

    def asr_corrector(self, environment):
        self.best_state = environment.init_state
        cost = environment.compute_cost(environment.init_state)

        vocab = self.vocabulary
        phoneme = self.phoneme_table
        s = environment.init_state
        c = environment.compute_cost(s)
        sentence = s
        cost = c

        transition = {}
        for key in phoneme:
            for v in phoneme[key]:
                if v not in transition:
                    transition[v] = []
                transition[v].append(key)

        n = len(s)
        subs = 0
        for i in range(n - 2):
            if (s[i] in transition):
                subs += 1
            elif (s[i:i + 2] in transition):
                subs += 1
            elif (s[i:i + 3] in transition):
                subs += 1

        if (subs == 0):
            max_dep = 100
        else:
            max_dep = 1000 // subs
            
        max_dep = max(max_dep, 10)
        
        dp = [False] * n
        dep = 0
        while (True):
            dep += 1
            if (dep > max_dep):
                break
            flag = False
            trans = []
            ndp = dp.copy()
            for i in range(n):
                if not dp[i]:
                    if s[i] in transition:
                        for v in transition[s[i]]:
                            ns = s[:i] + v + s[i + 1:]
                            nc = environment.compute_cost(ns)
                            if (nc < cost):
                                cost = nc
                                sentence = ns
                                flag = True
                                trans = [i]
                                self.best_state = sentence
                    if (i < n - 1) and (not dp[i + 1]):
                        if s[i:i + 2] in transition:
                            for v in transition[s[i:i + 2]]:
                                ns = s[:i] + v + s[i + 2:]
                                nc = environment.compute_cost(ns)
                                if (nc < cost):
                                    cost = nc
                                    sentence = ns
                                    flag = True
                                    trans = [i, i + 1]
                                    self.best_state = sentence
                        if (i < n - 2) and (not dp[i + 2]):
                            if s[i:i + 3] in transition:
                                for v in transition[s[i:i + 3]]:
                                    ns = s[:i] + v + s[i + 3:]
                                    nc = environment.compute_cost(ns)
                                    if (nc < cost):
                                        cost = nc
                                        sentence = ns
                                        flag = True
                                        trans = [i, i + 1, i + 2]
                                        self.best_state = sentence

            if not flag:
                break
            l = len(sentence)
            if (l >= n):
                for i in trans:
                    dp[i] = True
                for i in range(l - n):
                    dp.insert(trans[0], True)
                n = l
                s = sentence
                self.best_state = s
            else:
                for i in trans:
                    dp[i] = True
                for i in range(n - l):
                    del dp[trans[0]]
                n = l
                s = sentence
                self.best_state = s

        bestfront = []

        for i in range(len(vocab)):
            v = vocab[i]
            ns = v + ' ' + s
            nc = environment.compute_cost(ns)
            bestfront.append((nc, ns))
            
        bestfront.sort(key=lambda x: x[0])
        
        for i in range(min(3, len(bestfront))):
            s1 = bestfront[i][1]
            for i in range(len(vocab)):
                v = vocab[i]
                ns = s1 + ' ' + v
                nc = environment.compute_cost(ns)
                if (nc < cost):
                    cost = nc
                    sentence = ns
                    self.best_state = sentence

        s = sentence
        self.best_state = s
        print(s)