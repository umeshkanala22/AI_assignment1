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

class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None

    def asr_corrector(self, environment):
        self.best_state = environment.init_state
        cost = environment.compute_cost(environment.init_state)

        # Implement search method to find best correction
        self.search(environment, environment.init_state, cost)

        # Update best state with the corrected text
        environment.best_state = self.best_state

    def search(self, environment, state, cost):
        # Simple beam search implementation
        beam_size = 10
        beam = [(state, cost)]

        for _ in range(10):  # Number of iterations
            new_beam = []
            for state, cost in beam:
                for word in state.split():
                    if word not in self.vocabulary:
                        # Generate corrections for the word
                        corrections = self.generate_corrections(word)
                        for correction in corrections:
                            new_state = state.replace(word, correction)
                            new_cost = environment.compute_cost(new_state)
                            new_beam.append((new_state, new_cost))

            # Select the top beam_size states with the lowest cost
            beam = sorted(new_beam, key=lambda x: x[1])[:beam_size]

        # Update best state with the corrected text
        self.best_state = beam[0][0]

    def generate_corrections(self, word):
        # Simple correction generation using phoneme table
        corrections = []
        for vocab_word in self.vocabulary:
            if self.phoneme_distance(word, vocab_word) <= 2:
                corrections.append(vocab_word)
        return corrections

    def phoneme_distance(self, word1, word2):
        # Implement phoneme distance calculation using phoneme table
        phonemes1 = self.phoneme_table[word1]
        phonemes2 = self.phoneme_table[word2]
        distance = 0
        for i in range(min(len(phonemes1), len(phonemes2))):
            if phonemes1[i] != phonemes2[i]:
                distance += 1
        distance += abs(len(phonemes1) - len(phonemes2))
        return distance

