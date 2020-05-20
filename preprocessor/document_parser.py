import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller
from nltk.corpus import wordnet
from string import punctuation


def load_nltk():
    """Loads main nltk packages for further use."""
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("stopwords")
    nltk.download('averaged_perceptron_tagger')


class DocumentParser:
    """Parses a single document creating a vector of word occurrences in it."""

    speller = Speller(lang="en")
    snowball_stemmer = SnowballStemmer("english")
    wordnet_lemmatizer = WordNetLemmatizer()

    def __init__(self, document_name):
        self.text = None
        with open(document_name, 'r', encoding="utf-8", errors="replace") as file:
            self.text = file.read().replace('\n', ' ')
            print("File", document_name, "successfully loaded.")
        self.words = [w for w in nltk.word_tokenize(self.text)]

    def correct_spelling(self):
        """Corrects the spelling of the word if needed."""
        self.words = [self.speller(w) for w in self.words]
        return self

    def to_lower(self):
        """Converts words from the list to the lower case."""
        self.words = [w.lower() for w in self.words]
        return self

    def remove_numbers(self):
        """Returns the list of words without the ones that contain numbers."""
        self.words = [w for w in self.words if not any(ch.isdigit() for ch in w)]
        return self

    def remove_punctuation(self):
        """Cleans the list of words from the ones that contain punctuation."""
        self.words = [w for w in self.words if not any(ch in punctuation for ch in w)]
        return self

    def remove_stopwords(self):
        """Removes all the stop words like "is", "the", "a", etc. """
        self.words = [w for w in self.words if w not in stopwords.words('english')]
        return self

    def lemmatize(self):
        """Lemmatizes the given words."""
        self.words = [self.wordnet_lemmatizer.lemmatize(*get_wordnet_pos(word)) for word in self.words]
        return self

    def stem(self):
        """Stems the given words."""
        self.words = [self.snowball_stemmer.stem(word) for word in self.words]
        return self

    def start(self):
        """Parses the text into the list of stemmed and lemmatized words."""
        self.to_lower() \
            .remove_numbers() \
            .remove_punctuation() \
            .correct_spelling() \
            .remove_stopwords() \
            .lemmatize() \
            .stem()
        return {word: self.words.count(word) for word in self.words}


def get_wordnet_pos(word):
    """Maps POS tag to first character lemmatize() accepts."""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return word, tag_dict.get(tag, wordnet.NOUN)
