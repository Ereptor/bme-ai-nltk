#tputil = text processor utilites

import os
import nltk
import numpy
import sys
import json

import matplotlib.pyplot as pyplot
import matplotlib
from mpl_toolkits.mplot3d import axes3d
from nltk.corpus import stopwords

# configurable constants in 
DATABASE_SEPARATOR = '\t\t\t'
KNOWLEDGEBASE_FILE = 'knowledgebase.dat'
DATABASE_FILE = 'database.dat'
FINGERPRINT_FOLDER = 'fingerprint'
MOST_COMMON_NUMBER = 50

KNOWLEDGEBASE_KEY_WORDS = 'keywords'
KNOWLEDGEBASE_KEY_FREQS = 'freqs'
KNOWLEDGEBASE_KEY_STOPMODE = 'stopmode'
KNOWLEDGEBASE_KEY_SMLANGUAGE = 'stopmodeLanguage'

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
def add_to_database(filename, database=None):
  if not os.path.isfile(filename):
    print("[ERROR]: Input file not found.")
    sys.exit(FILE_NOT_FOUND) # Finish with file not found error
  
  close_database = False
  if database is None:
    close_database = True
    database = open(DATABASE_FILE, 'a',encoding='utf-8')
  
  importfile = open(filename, 'r',encoding='utf-8')
  
  database.write(importfile.read())
  database.write(DATABASE_SEPARATOR)
  
  importfile.close()
  
  if close_database:
    database.close()
    
  print('\''+os.path.basename(filename)+'\' successfully added to database.')



# adds the text files in ./texts folder to the database
def add_texts():
  text_folder = os.path.join(str(os.getcwd()), FINGERPRINT_FOLDER)
  database = open(DATABASE_FILE, 'a',encoding='utf-8')
  
  iterator = 0
  for text_name in os.listdir(text_folder):
    iterator += 1
    add_to_database(os.path.join(text_folder, text_name), database)
    
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
def compile_database(stop_mode = False, sm_language = 'english'):
  if not os.path.isfile(DATABASE_FILE):
    print("[ERROR]: No database found. Please run compile-database first.")
    sys.exit(NO_DATABASE) # Finish with database error
  
  database = open(DATABASE_FILE, 'r',encoding='utf-8')
  rawtext = database.read()
  database.close()
  
  texts = rawtext.split(DATABASE_SEPARATOR)  
  freq = freqdist_text(rawtext, stop_mode, sm_language)
  
  # the dict, which will store our knowledge about the author
  knowledgebase = {}
  
  # collect the most common words
  keys = freq.most_common(MOST_COMMON_NUMBER)
  keywords = numpy.empty(MOST_COMMON_NUMBER, dtype=object)
  
  for i in range(0,MOST_COMMON_NUMBER):
    keywords[i] = keys[i][0]
  
  knowledgebase[KNOWLEDGEBASE_KEY_WORDS] = keywords.tolist()
  knowledgebase[KNOWLEDGEBASE_KEY_STOPMODE] = stop_mode
  if stop_mode:
    knowledgebase[KNOWLEDGEBASE_KEY_SMLANGUAGE] = sm_language
  
  knowledge_freqs = []
  
  iterator = 0
  for text in texts:
    # length counts punctuation, but its amount
    # should be about the same in all texts
    length = len(text)
    
    if length > 0:
      iterator += 1
      frequency = get_text_frequency(text, knowledgebase)
      
      knowledge_freqs.append(frequency.tolist())
      print('%d text(s) processed.'%iterator, end='\r')
  
  knowledgebase[KNOWLEDGEBASE_KEY_FREQS] = knowledge_freqs

  # remove previous knowledgebase to avoid duplicates
  knowledgebase_file = open(KNOWLEDGEBASE_FILE, 'w',encoding='utf-8')
  
  json.dump(knowledgebase, knowledgebase_file)
  
  knowledgebase_file.close()
  
  print('%d text(s) successfully processed.'%(iterator))
  
def get_knowledgebase():
  if not os.path.isfile(KNOWLEDGEBASE_FILE):
    print("[ERROR]: No database found. Please run compile-database first.")
    sys.exit(NO_KNOWLEDGEBASE) # Finish with knowledge error
    
  knowledgebase_file = open(KNOWLEDGEBASE_FILE, 'r',encoding='utf-8')
  knowledgebase = json.load(knowledgebase_file)
  knowledgebase_file.close()
  
  freqs = knowledgebase[KNOWLEDGEBASE_KEY_FREQS];
  knowledgebase[KNOWLEDGEBASE_KEY_FREQS] = numpy.array(freqs)
  
  return knowledgebase
  
def freqdist_text(text, stop_mode, language):
  word_tokenizer = nltk.RegexpTokenizer(r'\w\w+') # throws away one letter words
  
  tokens = word_tokenizer.tokenize(text)
  
  if(stop_mode):
    stop = stopwords.words(language)
    filtered_tokens = [w for w in tokens if w not in stop]
    tokens = filtered_tokens
  
  freq = nltk.FreqDist(tokens)
  
  return freq


def purge():
  remove_file(DATABASE_FILE)
  remove_file(KNOWLEDGEBASE_FILE)
  
  print('Files successfully deleted.')



# returns the frequency of keywords in text
def get_text_frequency(text, knowledgebase):
  keywords = knowledgebase[KNOWLEDGEBASE_KEY_WORDS]
  stop_mode = knowledgebase[KNOWLEDGEBASE_KEY_STOPMODE]
  sm_language = knowledgebase.get(KNOWLEDGEBASE_KEY_SMLANGUAGE) # None if value doesn't exists
  length = len(text) # this is the length of the whole text
  if length > 0:
    frequency = numpy.empty(MOST_COMMON_NUMBER)
    freq = freqdist_text(text, stop_mode, sm_language) # this shortens the text!
    for i in range(0,MOST_COMMON_NUMBER):
      frequency[i] = 100*freq[keywords[i]]/length
  
  return frequency



# opens a file and returns it's word frequency
def get_file_frequency(filepath, knowledgebase):
  input_file = open(filepath,encoding='utf-8')
  input_frequency = get_text_frequency(input_file.read(), knowledgebase)
  input_file.close()
  return input_frequency


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
  knowledgebase = get_knowledgebase()
  
  matrix = knowledgebase[KNOWLEDGEBASE_KEY_FREQS];
  
  figure = pyplot.figure()
  ax = figure.add_subplot(111, projection = '3d')
  
  input_frequency = get_file_frequency(filename, knowledgebase)
  
  #data = PCA_result(matrix)
  #data[0] = data[1] # amateur solution, but the first PCA result is *always* off
  
  ax.set_xlabel(str('Most common word percentage\n' + knowledgebase[KNOWLEDGEBASE_KEY_WORDS][0]))
  ax.set_ylabel('Second most common word percentage\n'+ knowledgebase[KNOWLEDGEBASE_KEY_WORDS][1])
  ax.set_zlabel('Third most common word percentage\n'+ knowledgebase[KNOWLEDGEBASE_KEY_WORDS][2])
  
  ax.plot(matrix[:,0], matrix[:,1], matrix[:,2], 'o', c='b')
  ax.plot([input_frequency[0]], [input_frequency[1]], [input_frequency[2]], 'o', c='r') #ax.plot expects an array, not a single item
  
  ax.view_init(45,-45)

  pyplot.show()
 