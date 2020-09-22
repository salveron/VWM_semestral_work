# BI-VWM Semestral work

This project is the **BI-VWM** semestral task for **FIT CTU in Prague**. The task specification can be found 
at the **FIT CTU Courses** website for the **BI-VWM** subject.

In brief, this application implements the **Extended Boolean Model (EBM)** for information retrieval. It uses
the **bbc** collection of articles of different topics to create the matrix of the proper size to make
the differences in efficiency between the **EBM** and the **Sequential search** be clearly seen.

Authored by **Nikita Mortuzaiev** and **Roman Zhuravskyi**.

## Packages

 - **preprocessor** - parses the collection of documents and prepares a weight matrix and the inverted list
 for every word in every document.
 
 - **query_parser** - parses the queries from the user input and computes result using the Extended Boolean model formulas
 or sequentially.
 
 - **gui** - the graphical web interface (Django).
 
 - **bbc** - the collection of documents to be used for searching in. The topics of texts are: **business**, 
 **entertainment**, **politics**, **sport** and **tech**.
 
 ## Installation
 
 To install required libraries run this code:
 
 `pip install -r requirements.txt`
 
 Required third-party libraries are these: **numpy**, **pandas**, **nltk** and **django**.
 
 ## Usage
 
 Execute this:
 
 `python3 main.py`
 
 to run the application that uses already parsed dataset saved in the file **"dataset.csv"**, or this:
 
 `python3 main.py --new`
 
 to start the application that creates the dataset and stores it to the file **"dataset.csv"**
 before running the web server. 
 
 **WARNING: CREATING A NEW "dataset.csv" FILE COSTS A LOT OF TIME** (there are more than 2,000 files to filter, lemmatize
 and stem).
 
 ## Contributing
 
 Feel free to improve the code to get better results.
