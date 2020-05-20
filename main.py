import os
import sys

from preprocessor.collection_parser import CollectionParser, load_nltk


if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "--new":
        load_nltk()
        parser = CollectionParser(new_table=True)
        parser.create_table()
        parser.save_table()
    elif len(sys.argv) != 1:
        print("Usage: python main.py [--new]")
        exit()
    else:
        load_nltk()

    os.system("python3 manage.py runserver")
