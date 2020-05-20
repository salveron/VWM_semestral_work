from abc import ABC, abstractmethod

from preprocessor.collection_parser import CollectionParser
from preprocessor.term_inverter import TermInverter


weights_holder = CollectionParser().start()
inverted_terms_holder = TermInverter(weights_holder).start()


class WeightToken(ABC):
    """This is an abstract class for the tokens that can return weights (WordToken, NotToken and OpeningBracketToken)"""

    def __init__(self, id_value):
        self.id = id_value

    @abstractmethod
    def get_weight_ebm(self, parser):
        pass

    @abstractmethod
    def get_weight_seq(self, parser):
        pass


class OperatorToken(ABC):
    """This is an abstract class for the operator tokens (AndToken and OrToken)"""

    def __init__(self, id_value):
        self.id = id_value

    @abstractmethod
    def evaluate_operator(self, operands):
        pass


class InvalidQueryException(Exception):
    """This an exception class for raising when the user entered an invalid query."""
    pass


class InvalidTokenException(Exception):
    """This an exception class for raising when the user entered an invalid operator."""
    pass
