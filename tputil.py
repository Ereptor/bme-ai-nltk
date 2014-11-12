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
def compile_texts():
  knowledgebase = open(KNOWLEDGEBASE_FILE, 'a')
  texts_path = os.path.join(os.getcwd(),"texts")
  
  iterations = 0
  for file in os.listdir(books_path):
    iterations += 1
    current_text = open(os.path.join(texts_path,file),'r')
    text = current_text.read()
    current_text.close()
    compile_text(text)
    print(str(iterations) + ' text(s) processed.', end='\r')
  
  
  print('\nKnowledgebase successfully compiled.')
  knowledgebase.close()

  
def purge():
  remove_file(DATABASE_FILE)
  remove_file(KNOWLEDGEBASE_FILE)

## TODO: PCA, process texts in folder, etc.
## I should have some time tomorrow to get started on it