import pandas as pd


class TermInverter:
    def __init__(self, weights):
        self.w_matrix = weights

    def invert_term(self, term):
        return self.w_matrix.loc[term, self.w_matrix.loc[term] != 0.0]

    def start(self):
        return [self.invert_term(term) for term in self.w_matrix.index]
