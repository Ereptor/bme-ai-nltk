import os.path
import nltk
import numpy as NP
from scipy import linalg as LA

#tputil = text processor utilites

def foo():
  print('bar')
  
def add_to_database(filename):
  if not os.path.isfile(filename):
    print("Error: Input file not found.")
    return
    
  database = open('database.dat', 'a')
  importfile = open(filename, 'r')
  
  database.write(importfile.read())
  database.write('\t\t\t')
  
  importfile.close()
  database.close()

  
def compile():
  if not os.path.isfile('database.dat'):
    print("Error: No database found.")
    return
  
  
  database = open('database.dat', 'r')
  text = open('database.dat', 'r').read()
  tokenized_text = nltk.word_tokenize(text)
  fdist = nltk.FreqDist(tokenized_text)
  
  knowledgebase = open('knowledgebase.dat', 'w')
  for pairs in fdist.most_common(70):
    knowledgebase.write(str(pairs[0]) + '\t' + str(pairs[1]) 
    + '\n')
    

  
def purge():
  os.remove('database.dat')
  os.remove('knowledgebase.dat')
  
  
def split_database():
  database = open('database.dat', 'r')
  datatext = database.read()
  
  parted = str.split(datatext, '\t\t\t')
  
  return parted
  
def most_common(text, number):
  tokenized_text = nltk.word_tokenize(text)
  
  return nltk.FreqDist(tokenized_text).most_common(number)
  
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

# exact copy from https://github.com/alexland/kPCA/blob/master/PCA.py
# good for now, until we don't figure out what it does.
def pca(matrix, num_eigenvalues=None, EV=0, LDA=0):
    D = NP.array(matrix)
    if not (LDA & EV):
      D, EV = NP.hsplit(D, [-1])
      
    # D -= D.mean(axis=0)
    R = NP.corrcoef(D, rowvar=False)
    m, n = R.shape
    if num_eigenvalues:
      num_eigenvalues = (m - num_eigenvalues, m-1)
    eva, evc = LA.eigh(R, eigvals=num_eigenvalues)
    NP.ascontiguousarray(evc)  
    NP.ascontiguousarray(eva)
    idx = NP.argsort(eva)[::-1]
    evc = evc[:,idx]
    eva = eva[idx]
    return eva.tolist()
