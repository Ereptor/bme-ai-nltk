Knowledgebase.dat:

Contains the processed data in 'word \t occurence' formatted 'tuples'.



Database.dat:

Contains all the known text in plain text format, without labeling or knowing their author. The different texts are separated by  a '\t\t\t' mark (hopefully no one would use this exact string of tabulators in a real text).



ntpro.py (NLTK text processor):

The main program. For the sake of being easily readable it basically only contains function calls, none of the program's logic is realised here beside the user interface.



tputil.py (text processor utilities):

A standard assistant library that helps with the basic user interactions and provides tools for the scientific calculations in tpcalc.py.

add_to_database(filename) - attempts to add the text found at 'filename' to the database (database.dat). Returns with an error message if the input file doesn't exist at the given path.

compile() - compiles the known data into a knowledgebase (knowledgebase.dat). It returns with an error message if there is no known database present.

purge() - deletes the data- and knowledgebase at its standard location.

split_database() - separates the merged texts and returns them in an array. First index = 0.

most_common((string)text,(int)number) - returns the [number] most common words in [text]. The returned values are stored in {word, occurence} formatted tuples.


tpcalc.py

Contains the all the scientific algorithm related functions (at the time of writing it's only the compare function).