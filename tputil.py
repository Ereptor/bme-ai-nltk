#tputil = text processor utilites

import os
import nltk
import numpy

from matplotlib.mlab import PCA
import matplotlib.pyplot as pyplot
import matplotlib
from mpl_toolkits.mplot3d import axes3d

# the separator character in database.dat file
DATABASE_SEPARATOR = '\t\t\t'
KNOWLEDGEBASE_FILE = 'knowledgebase.dat'
DATABASE_FILE = 'database.dat'
MOST_COMMON_NUMBER = 50

# method to remove the file without raisin an error
def remove_file(filepath):
  try:
    os.remove(filepath)
  except OSError:
    pass


# adds a file to the database.dat file
def add_to_database(filename):
  if not os.path.isfile(filename):
    print("[ERROR]: Input file not found.")
    return # Finish with error
    
  database = open(DATABASE_FILE, 'a')
  importfile = open(filename, 'r')
  
  database.write(importfile.read())
  database.write(DATABASE_SEPARATOR)
  
  print('File successfully added to database.')
  
  importfile.close()
  database.close()


# adds the text files in ./texts folder to the database
def add_texts():
  text_folder = os.path.join(str(os.getcwd()),'texts')
  database = open(DATABASE_FILE, 'a')
  
  iterator = 1
  for text_name in os.listdir(text_folder):
    text = open(os.path.join(text_folder, text_name))
    
    database.write(text.read())
    database.write(DATABASE_SEPARATOR)
    
    text.close()
    print('%d text added to database file.'%(iterator), end='\r')
    iterator += 1
    
  print('Text(s) successfully added to database file.')  
  database.close()
  
  

# compiles the database.dat file and adds it to the knowledge base  
def compile_database():
  if not os.path.isfile(DATABASE_FILE):
    print("[ERROR]: No database found. Please run compile-database first.")
    return # Finish with error
  
  # remove previous knowledgebase to avoid duplicates
  remove_file(KNOWLEDGEBASE_FILE)
  
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'a')
  database = open(DATABASE_FILE, 'r')
  rawtext = database.read()
  texts = rawtext.split(DATABASE_SEPARATOR)
  texts.pop() #remove last empty text
  
  #Write the most common words in all the texts as a header for knowledgebase
  keys = most_common(rawtext, MOST_COMMON_NUMBER)
  keywords = numpy.empty(MOST_COMMON_NUMBER, dtype=object)
  
  for key in keys:
    knowledgebase.write(str(key[0]) + '\t')  
  knowledgebase.write('\n')
  

  for iterator in range(0,MOST_COMMON_NUMBER):
    keywords[iterator] = keys[iterator][0]
    

  iterator = 1
  for text in texts:
    length = len(text)
    
    for keyword in keywords:
      count = get_count(text,keyword)
      
      frequency = 100*count/length
      knowledgebase.write(str(frequency) + '\t')

    knowledgebase.write('\n')
    print('%d text processed.'%iterator, end='\r')
    iterator += 1
    
  print('%d text successfully processed.'%(iterator-1))
  
  knowledgebase.close()
  database.close()

# returns the number of occurences of [word] in [text]
def get_count(text, word):
  word_tokenizer = nltk.RegexpTokenizer(r'\w\w+') #throws away one letter words
  
  tokens = word_tokenizer.tokenize(text.lower())
  freq = nltk.FreqDist(tokens)
  
  return freq[word]

# input is a numpy matrix
def center_point(points):
  center = points[0]
  for point in points[1:]:
    center += point
  center /= len(points)
  return center
  

#this filters the punctuation!
# returns the [number] most common words in [text]
def most_common(text, number):
  word_tokenizer = nltk.RegexpTokenizer(r'\w\w+') #again, no one letter words allowed
  
  tokens = word_tokenizer.tokenize(text.lower())
  freq = nltk.FreqDist(tokens)
  
  return freq.most_common(number)


def purge():
  remove_file(DATABASE_FILE)
  remove_file(KNOWLEDGEBASE_FILE)
  
  print('Files successfully deleted.')


# Returns the array representing the [index]th text in the knowledgebase
def get_text_frequency(row):
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'r')
  
  for i in range(0,row+1):
    knowledgebase.readline()
    
  frequency = knowledgebase.readline().split('\t')
  frequency.pop()
  
  knowledgebase.close()
  return frequency


# Returns the number of texts used for reference in the knowledgebase
def get_text_count():
  iterator = -1
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'r')
  
  while knowledgebase.readline():
    iterator += 1
  
  knowledgebase.close()
  return iterator


# Returns the index of the keyword in the knowledgebase
# If the word is not part of the 50 most common words it returns -1
def get_word_index(word):
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'r')
  keywords = knowledgebase.readline().split('\t')
  
  index = -1
  
  for i in range(0,MOST_COMMON_NUMBER):
    if(keywords[i] == word):
      index = i
      break

  knowledgebase.close()
  return index    


# PCA to transform the 50 columns into 3
# It means that after the transformation every text is represented in
# a 3D space, not in 50 dimension
def PCA3D(data):
  result = PCA(data)
  result_array = numpy.empty((result.numrows, 3))

  iterator = 0  
  for item in result.Y:
    result_array[iterator] = [item[0],item[1],item[2]]
    iterator += 1
   
  return result_array
  

# SECOND MATRIX IS FOR DEBUGGING! TODO: remove matrix2
# Other than that it's a simple function plotting the graph
def plotPCA():
  try:
    knowledgematrix = numpy.empty((get_text_count(), MOST_COMMON_NUMBER))
  
    for i in range(0,get_text_count()):
      knowledgematrix[i] = get_text_frequency(i)
  
    matrix = PCA3D(knowledgematrix)
  
    figure = pyplot.figure()
    ax = figure.add_subplot(111, projection = '3d')
    
    matrix2 = numpy.empty((70,3))
    for i in range(0,70):
      matrix2[i] = matrix[5]
      
    center = center_point(matrix[:5])
    
    ax.plot(matrix[:,0], matrix[:,1], matrix[:,2], 'o', c='b')
    ax.plot(matrix2[:,0], matrix2[:,1], matrix2[:,2], 'o', c='r')
    ax.plot([center[0]], [center[1]], [center[2]], 'o', c='g')
    
    ax.view_init(45,-45)
  
    pyplot.show()
  except Exception as exc:
    print('[ERROR]: Not enough datapoints for analysis, please add more reference texts.',exc)