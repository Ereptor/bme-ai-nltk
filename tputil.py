import os.path
import nltk

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
  
  