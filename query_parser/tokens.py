import math
from string import punctuation

from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller

from preprocessor.document_parser import get_wordnet_pos
from utils import WeightToken, OperatorToken, InvalidQueryException


class WordToken(WeightToken):
    """This is a word literal token class. It has a get_weight method to return the word weight from the parser's
    vector of weights."""

    speller = Speller(lang="en")
    snowball_stemmer = SnowballStemmer("english")
    wordnet_lemmatizer = WordNetLemmatizer()

    def __init__(self, value):
        super().__init__(value)

    def get_weight_ebm(self, parser):
        """Checks and cleans the word. Then returns its weight in the parser's vector for the evaluate_ebm."""
        return parser.inverted_terms.loc[self.id, parser.current_document]

    def get_weight_seq(self, parser):
        """Checks and cleans the word. Then returns its weight in the parser's vector for the evaluate_seq."""
        return parser.weights.loc[self.id, parser.current_document]

    def check(self):
        """Checks if the word has numbers or punctuation in it."""
        if any(ch.isdigit() for ch in self.id) or any(ch in punctuation for ch in self.id):
            raise InvalidQueryException("Invalid word literal.")

    def clean(self):
        """Uses stemmer and lemmatizer to get a cleaned word just like in the matrix of weights."""
        return self.snowball_stemmer.stem(
            self.wordnet_lemmatizer.lemmatize(*get_wordnet_pos(
                self.speller(self.id))))


class OpeningBracketToken(WeightToken):
    """Represents an opening bracket token. Get_weight method starts the recursion."""

    def __init__(self):
        super().__init__("(")

    def get_weight_ebm(self, parser):
        """Returns the value of the expression inside the parentheses for the evaluate_ebm."""
        parser.current_token = next(parser.tokenizer)
        return parser.evaluate()

    get_weight_seq = get_weight_ebm


class NotToken(WeightToken):
    """Represents an operator "NOT" token."""
    def __init__(self):
        super().__init__("!")

    def get_weight_ebm(self, parser):
        """Returns the negated value of the expression after the operator for the evaluate_ebm."""
        parser.current_token = next(parser.tokenizer)
        return 1.0 - parser.current_token.get_weight_ebm(parser)

    def get_weight_seq(self, parser):
        """Returns the negated value of the expression after the operator for the evaluate_seq."""
        parser.current_token = next(parser.tokenizer)
        return 1.0 - parser.current_token.get_weight_seq(parser)


class AndToken(OperatorToken):
    """Represents an operator "AND" token."""
    def __init__(self):
        super().__init__("&")

    def evaluate_operator(self, operands):
        """Returns the value of the conjunction of operands."""
        return 1.0 - math.sqrt(sum([(1.0 - op) ** 2 for op in operands]) / len(operands))


class OrToken(OperatorToken):
    """Represents an operator "OR" token."""
    def __init__(self):
        super().__init__("|")

    def evaluate_operator(self, operands):
        """Returns the value of the disjunction of operands."""
        return math.sqrt(sum([op ** 2 for op in operands]) / len(operands))


class ClosingBracketToken:
    """Represents a closing bracket token. Acts as the EndToken to return from the recursion."""
    id = ")"


class EndToken:
    """Represents an end of expression token."""
    id = "\0"
