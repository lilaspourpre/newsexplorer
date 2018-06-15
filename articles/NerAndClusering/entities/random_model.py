# -*- coding: utf-8 -*-
import random
from collections import Counter
from bisect import bisect_right
from entities.model import Model


class RandomModel(Model):
    def __init__(self):
        super().__init__()
        self.list_of_distributed_probabilities = [(0.010665804783451843, 'UORG'), (0.012540400775694894, 'ILOC'),
             (0.020361990950226245, 'UPER'), (0.04715578539107951, 'ULOC'),
             (0.05138978668390433, 'LLOC'), (0.06709760827407886, 'BPER'),
             (0.9377828054298643, 'O'), (0.9534906270200387, 'LPER'),
             (0.9681965093729799, 'IORG'), (0.9697155785391078, 'IPER'),
             (0.9827407886231414, 'BORG'), (0.995765998707175, 'LORG'),
             (1, 'BLOC')]


    def predict(self, vector):
        random_number = random.uniform(0, 1)
        new_index = bisect_right(self.list_of_distributed_probabilities, (random_number, ''))
        return self.list_of_distributed_probabilities[new_index][1]

    def __repr__(self):
        return 'random_model'

