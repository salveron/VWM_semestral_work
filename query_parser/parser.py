import re

import pandas as pd
from query_parser.tokens import *
from utils import InvalidTokenException, weights_holder, inverted_terms_holder, InvalidQueryException


class QueryParser:
    """Parses a query accepted from the user and then recursively evaluates it."""

    token_pattern = re.compile("\s*(?:((?!and|or|not)\w+)|(and|or|not|[()]))")

    def __init__(self, query, sequential=False):
        self.sequential = sequential

        self.query = query.lower()
        self.add_parentheses()

        self.groups = re.findall(self.token_pattern, self.query)
        self.words = self.get_words()

        self.inverted_terms = None
        self.weights = None
        if not self.sequential:
            self.inverted_terms = pd.DataFrame([inverted for inverted in inverted_terms_holder
                                                if inverted.name in self.words]).fillna(0.0)
        else:
            self.weights = weights_holder

        self.tokenizer = None
        self.current_document = None
        self.current_token = None

    def get_words(self):
        return [group[0] for group in self.groups if group[0]]

    def tokenize(self):
        """Generates tokens from the matches of regular expression."""

        bracket_stack = []
        w_counter = 0
        for word, operator in self.groups:
            if word:
                yield WordToken(self.words[w_counter])
                w_counter += 1
            elif operator == "not":
                yield NotToken()
            elif operator == "and":
                yield AndToken()
            elif operator == "or":
                yield OrToken()
            elif operator == "(":
                bracket_stack.append("(")
                yield OpeningBracketToken()
            elif operator == ")":
                if len(bracket_stack) > 0:
                    bracket_stack.pop()
                else:
                    raise InvalidQueryException("Wrong parentheses. Try again.")
                yield ClosingBracketToken()
            else:
                raise InvalidTokenException("Invalid operator. Try again.")

        if len(bracket_stack) > 0:
            raise InvalidQueryException("Wrong parentheses. Try again.")
        yield EndToken()

    def add_parentheses(self):
        """Adds missing parentheses to the query so that it evaluates right."""
        pattern = re.compile("(?<!\()(?:not\s+)?(?:\b\w+\b|\(.+?\))(?:\s+and\s+(?:not\s+)?(?:\b\w+\b|\(.+?\)))+(?!\))")
        self.query = re.sub(pattern, lambda x: "(" + x.group(0) + ")", self.query)

    def evaluate(self):
        """Evaluates the expression finding the relevance of the given vector of weights for the given query.

        Recursively calls itself when the OpeningBracketToken is found to evaluate the expression inside. This function
        also uses the generator defined by the tokenize method. That generator is created in the constructor."""
        try:
            left_operand = self.current_token

            if not self.sequential:
                res = left_operand.get_weight_ebm(self)
            else:
                res = left_operand.get_weight_seq(self)

            self.current_token = next(self.tokenizer)
            while self.current_token.id not in [EndToken.id, ClosingBracketToken.id]:
                operator = self.current_token
                self.current_token = next(self.tokenizer)

                if not self.sequential:
                    next_value = self.current_token.get_weight_ebm(self)
                else:
                    next_value = self.current_token.get_weight_seq(self)

                next_token = next(self.tokenizer)
                values = [res]
                while next_token.id == operator.id:
                    values.append(next_value)
                    next_token = next(self.tokenizer)

                    if not self.sequential:
                        next_value = next_token.get_weight_ebm(self)
                    else:
                        next_value = next_token.get_weight_seq(self)

                    self.current_token = next_token
                    next_token = next(self.tokenizer)
                values.append(next_value)
                self.current_token = next_token
                res = operator.evaluate_operator(values)
            return res

        except AttributeError as ae:
            raise InvalidQueryException(f"Wrong query \"{self.query}\". Try again.") from ae

    def start(self):
        result = []
        matrix = self.inverted_terms if not self.sequential else self.weights
        for doc_name in matrix.columns:
            self.current_document = doc_name
            self.tokenizer = self.tokenize()
            self.current_token = next(self.tokenizer)
            result.append((doc_name, round(self.evaluate() * 100, 2)))
        return [res for res in result if res[1] > 0]
