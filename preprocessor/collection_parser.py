import os

import numpy as np
import pandas as pd

from preprocessor.document_parser import *


DATASET_PATH = "bbc"
CSV_FILE_NAME = "dataset.csv"
TOPICS_DICT = {"business": 510, "entertainment": 386, "politics": 417, "sport": 511, "tech": 401}


class CollectionParser:
    """Parses the collection of documents creating a main weights matrix for the extended boolean model."""

    def __init__(self, dataset_path=DATASET_PATH, new_table=False):
        self.document_names = []
        for topic, num_of_docs in TOPICS_DICT.items():
            self.document_names += [os.path.join(dataset_path, topic, "{:03d}".format(num)) + ".txt"
                                        for num in range(1, num_of_docs + 1)]

        self.table = pd.DataFrame()
        if not new_table:
            self.load_table()

    def create_table(self):
        """Creates the matrix of word occurrences, then computes tf matrix and idf vector for each document, then
        computes weights."""

        print("Creating the matrix of occurrences...")
        self.table = pd.DataFrame.from_dict({doc: DocumentParser(doc).start()
                                             for doc in self.document_names})

    def save_table(self, file_name=CSV_FILE_NAME):
        """Saves the matrix of weights to the .csv file for further processing with faster loading."""
        print("Saving the matrix of weights...")
        self.table.sort_index().to_csv(file_name)

    def load_table(self, file_name=CSV_FILE_NAME):
        """Loads the matrix of weights from the .csv file."""
        print("Loading the dataset...")
        self.table = pd.read_csv(file_name, index_col=0, engine="c", keep_default_na=False, na_values=[""]).fillna(0.0)

        print("Computing TF matrix...")
        tf_table = self.table.div(np.max(self.table, axis=1), axis="rows")
        assert not tf_table.isnull().all().all()

        print("Computing IDF vector...")
        idf_vector = np.log2(len(self.table.columns) / np.count_nonzero(self.table, axis=1))
        assert not np.isnan(idf_vector).all()

        print("Computing weights...")
        self.table = tf_table.mul(idf_vector / idf_vector.max(), axis="rows")
        assert not self.table.isnull().all().all()

    def start(self):
        return self.table
