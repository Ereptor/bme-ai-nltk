import os.path
import nltk

def foo():
  print('bar')
  
def add_to_database(filename):
  database = open('database.dat', 'a')
  importfile = open(filename, 'r')
  
  database.write('\t')
  database.write(importfile.read())
    

def compare(filename):
  foo()
  
def compile():
  text = open('database.dat', 'r').read()
  tokenized_text = nltk.word_tokenize(text)
  fdist = nltk.FreqDist(tokenized_text)
  
  knowledgebase = open('knowledgebase.dat', 'w')
  for pairs in fdist.most_common(70):
    knowledgebase.write(str(pairs[0]) + '\t' + str(pairs[1]) 
    + '\n')