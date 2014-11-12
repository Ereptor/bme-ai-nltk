import os.path
import nltk
import json
import numpy as NP
from scipy import linalg as LA

#tputil = text processor utilites

# the separator character in database.dat file
DATABASE_SEPARATOR = '\t\t\t'
KNOWLEDGEBASE_FILE = 'knowledgebase.dat'
DATABASE_FILE = 'database.dat'

# method to remove the file without raisin an error
def remove_file(filepath):
  try:
    os.remove(filepath)
  except OSError:
    pass


# adds a file to the database.dat file
def add_to_database(filename):
  if not os.path.isfile(filename):
    print("Error: Input file not found.")
    return
    
  database = open(DATABASE_FILE, 'a')
  importfile = open(filename, 'r')
  
  database.write(importfile.read())
  database.write(DATABASE_SEPARATOR)
  
  importfile.close()
  database.close()
  

# compiles a single text and adds it to the knowledge base
def compile_text(text, knowledgebase):
  fingerprint = writing_fingerprint(text)
  fingerprint_str = json.dumps(fingerprint)
  knowledgebase.write(fingerprint_str+'\n')


# compiles the database.dat file and adds it to the knowledge base  
def compile_database():
  if not os.path.isfile(DATABASE_FILE):
    print("Error: No database found.")
    return
  
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'a')
  database = open(DATABASE_FILE, 'r')
  rawtext = database.read()
  texts = rawtext.split(DATABASE_SEPARATOR)
  
  for text in texts:
    compile_text(text, knowledgebase)
    
  knowledgebase.close()
  database.close()


# takes all the text files in the books folder and compiles them into knowledge base

## I cleaned up the code a little, should be more portable and
## easier to understand
def compile_books():
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'a')
  books_path = os.path.join(os.getcwd(), "books")
  
  for file in os.listdir(books_path): 
    book = open(file,'r')
    text = book.read()
    book.close()
    compile_text(text, knowledgebase)
  
  knowledgebase.close()

  
def purge():
  remove_file(DATABASE_FILE)
  remove_file(KNOWLEDGEBASE_FILE)

  
# it takes a normal string and creates a text identifying
def writing_fingerprint(text):
  tokenized_text = nltk.word_tokenize(text)
  #create a 5000*50 matrix, which represents the text
  matrix = text_matrix(tokenized_text)
  result = pca(matrix)
  return result


def text_matrix(tokenized_text):
  WORD_CHUNKS = 5000 # the number of chunks the text should be cut up
  WORDS = 50 # the length of a single chunk
  common_words = nltk.FreqDist(tokenized_text).most_common(WORDS) # the common words
  all_words = len(tokenized_text) # the number of all words
  words_per_chunk = all_words // WORD_CHUNKS # divided by the length of a single chunk, should give us the number of words in a chunk
  remainder = all_words % WORD_CHUNKS # however we still have some extra words
  matrix = [] # the result matrix
  word_index = 0 # a helping variable
  for index in range(WORD_CHUNKS): # iterate from 0 to WORD_CHUNKS
    end_index = word_index + words_per_chunk # calculate the end index
    if index < remainder: # the first 'remainder' chunks will have 1 extra word
      end_index+=1
    
    text_chunk = tokenized_text[word_index:end_index] # get the text chunk
    word_index = end_index
    fdist = nltk.FreqDist(text_chunk) # get the word distribution
    chunk_word_count = []
    for word in common_words: # for all common words
      chunk_word_count.append(fdist[word[0]]) # get the number of times the word was used in the chunk
    
    matrix.append(chunk_word_count) # append the chunk's row to the matrix

  return matrix

##PCA will be here