#tputil = text processor utilites

import os
import nltk
import numpy
import sys

from matplotlib.mlab import PCA
import matplotlib.pyplot as pyplot
import matplotlib
from mpl_toolkits.mplot3d import axes3d

# configurable constants in 
DATABASE_SEPARATOR = '\t\t\t'
KNOWLEDGEBASE_FILE = 'knowledgebase.dat'
DATABASE_FILE = 'database.dat'
FINGERPRINT_FOLDER = 'fingerprint'
MOST_COMMON_NUMBER = 50

# error numbers
FILE_NOT_FOUND = 11
NO_TEXTS = 12
NO_DATABASE = 13
NO_KNOWLEDGEBASE = 14

# method to remove the file without raising an error
def remove_file(filepath):
  try:
    os.remove(filepath)
  except OSError:
    pass


# adds a file to the database.dat file
def add_to_database(filename):
  if not os.path.isfile(filename):
    print("[ERROR]: Input file not found.")
    sys.exit(FILE_NOT_FOUND) # Finish with file not found error
    
  database = open(DATABASE_FILE, 'a')
  importfile = open(filename, 'r')
  
  database.write(importfile.read())
  database.write(DATABASE_SEPARATOR)
  
  print('File successfully added to database.')
  
  importfile.close()
  database.close()


# adds the text files in ./texts folder to the database
def add_texts():
  text_folder = os.path.join(str(os.getcwd()), FINGERPRINT_FOLDER)
  database = open(DATABASE_FILE, 'a')
  
  iterator = 0
  for text_name in os.listdir(text_folder):
    iterator += 1
    text = open(os.path.join(text_folder, text_name))
    
    
    if(os.path.getsize(DATABASE_FILE) > 0):
      #write separator if there was text before
      database.write(DATABASE_SEPARATOR)  
    database.write(text.read())
    
    text.close()
    
    # won't be seen unless excessive amount of files are added, but it doesn't hurt
    print('%d text added to database file.'%(iterator), end='\r')

  
  if(iterator != 0):  
    print('Text(s) successfully added to database file.')
    database.close()  
  else:
    print('[ERROR]: There are no files in texts folder.')
    database.close()
    sys.exit(NO_TEXTS)
  
  

# compiles the database.dat file and adds it to the knowledge base  
def compile_database():
  if not os.path.isfile(DATABASE_FILE):
    print("[ERROR]: No database found. Please run compile-database first.")
    sys.exit(NO_DATABASE) # Finish with database error
  
  # remove previous knowledgebase to avoid duplicates
  remove_file(KNOWLEDGEBASE_FILE)
  
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'a')
  database = open(DATABASE_FILE, 'r')
  rawtext = database.read()
  texts = rawtext.split(DATABASE_SEPARATOR)
  
  # write the most common words in all the texts as a header for knowledgebase
  keys = most_common(rawtext, MOST_COMMON_NUMBER)
  keywords = numpy.empty(MOST_COMMON_NUMBER, dtype=object)
  
  for i in range(0,MOST_COMMON_NUMBER):
    keywords[i] = keys[i][0]
    knowledgebase.write(str(keywords[i]) + '\t')
  knowledgebase.write('\n')
  
  
  iterator = 0
  for text in texts:
    # length counts punctuation, but its amount
    # should be about the same in all texts
    length = len(text)
      
    iterator += 1
    for keyword in keywords:
      count = get_count(text,keyword)
      
      frequency = 100*count/length # frequency is a percentage
      knowledgebase.write(str(frequency) + '\t')

    knowledgebase.write('\n')
    print('%d text(s) processed.'%iterator, end='\r')

  print('%d text(s) successfully processed.'%(iterator))
  
  knowledgebase.close()  
  database.close()

# returns the number of occurences of [word] in [text]
def get_count(text, word):
  word_tokenizer = nltk.RegexpTokenizer(r'\w\w+') # throws away one letter words
  
  tokens = word_tokenizer.tokenize(text.lower())
  freq = nltk.FreqDist(tokens)
  
  return freq[word]

#this filters the punctuation!
# returns the [number] most common words in [text]
def most_common(text, number):
  word_tokenizer = nltk.RegexpTokenizer(r'\w\w+') # again, no one letter words allowed
  
  tokens = word_tokenizer.tokenize(text.lower())
  freq = nltk.FreqDist(tokens)
  
  return freq.most_common(number)


def purge():
  remove_file(DATABASE_FILE)
  remove_file(KNOWLEDGEBASE_FILE)
  
  print('Files successfully deleted.')


# Returns the array representing the [index]th text in the knowledgebase
# indexing starts with 0
def get_text_frequency(row):
  if not os.path.isfile(KNOWLEDGEBASE_FILE):
    sys.exit(NO_KNOWLEDGEBASE)
    
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'r')
  
  # range[0-row) skips, first row is not frequency related
  for i in range(0,row+1):
    knowledgebase.readline()
    
  frequency = knowledgebase.readline().split('\t')
  frequency.pop() # last element is empty (tab without number following it)
  
  knowledgebase.close()
  
  return frequency

# naming is confusing, it's supposed to be used
# for the text that's to be compared to our knowledgebase
def get_frequency(text):
  if not os.path.isfile(KNOWLEDGEBASE_FILE):
    print('[ERROR]: Knowledgebase not found. Please compile database first.')
    sys.exit(NO_KNOWLEDGEBASE)
    
  knowledgebase = open(KNOWLEDGEBASE_FILE)
  
  keywords = knowledgebase.read().split('\t')
  knowledgebase.close()
  
  frequency = numpy.empty(MOST_COMMON_NUMBER)
  length = len(text)
  for i in range(0,MOST_COMMON_NUMBER):
    frequency[i] = 100*get_count(text, keywords[i])/length
  
  
  return frequency
  


# Returns the number of texts used for reference in the knowledgebase
def get_text_count():
  if not os.path.isfile(KNOWLEDGEBASE_FILE):
    sys.exit(NO_KNOWLEDGEBASE)
  
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'r')
  
  iterator = -1 # yet again, first line in knowledgebase is not text data
  while knowledgebase.readline():
    iterator += 1
  
  knowledgebase.close()
  
  return iterator


# Returns the index of the keyword in the knowledgebase
# If the word is not part of the 50 most common words it returns -1
# Note: not used in live code, left in to provide the interface
def get_word_index(word):
  if not os.path.isfile(KNOWLEDGEBASE_FILE):
    sys.exit(NO_KNOWLEDGEBASE)
  
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'r')
  keywords = knowledgebase.readline().split('\t')
  
  index = -1
  
  for i in range(0,MOST_COMMON_NUMBER):
    if(keywords[i] == word):
      index = i
      break

  knowledgebase.close()
  
  return index    

# input is a numpy matrix
# determines the 'center' of array of vectors
def center_point(points):
  center = points[0]
  
  for point in points[1:]:
    center += point
  center /= len(points)
  
  return center

# returns the distance between two n-dimensional vectors
def dist(point_a, point_b):
  vect = point_a - point_b
  dist = numpy.linalg.norm(vect)

  return dist
  
# Legacy code
def PCA_result(data):
  shape = data.shape
  
  if len(shape) > 1 and shape[0] < shape[1]:
    pca_data = (PCA(data.transpose()).Y).transpose()
  else:
    pca_data = PCA(data).Y
  
  return pca_data


# Switched back to original (truncated) vectors from
# PCA, oddly enough it seems to be more accurate
def plot(filename):
    # There was a try/except block here, but the possible error message is
    # more informative than a generic error text
    matrix = numpy.empty((get_text_count() + 1,MOST_COMMON_NUMBER))
    matrix2 = numpy.empty((2,MOST_COMMON_NUMBER)) #ax.plot requires at least two rows
    
    figure = pyplot.figure()
    ax = figure.add_subplot(111, projection = '3d')
    
    input_frequency = get_frequency(open(filename).read())
    
    for i in range(0, get_text_count()):
      matrix[i] = get_text_frequency(i)
    
    matrix[get_text_count()] = input_frequency
    #data = PCA_result(matrix)
    #data[0] = data[1] # amateur solution, but the first PCA result is *always* off
    
    for i in range(0,2):
      matrix2[i] = matrix[get_text_count()]
    
    ax.set_xlabel('Most common word percentage')
    ax.set_ylabel('Second most common word percentage')
    ax.set_zlabel('Third most common word percentage')
    
    ax.plot(matrix[:,0], matrix[:,1], matrix[:,2], 'o', c='b')
    ax.plot(matrix2[:,0], matrix2[:,1], matrix2[:,2], 'o', c='r')
    
    ax.view_init(45,-45)
  
    pyplot.show()
 