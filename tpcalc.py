import os.path
import tputil

#tpcalc = text processor calculations

def compare(filename):
  if not os.path.isfile('knowledgebase.dat'):
    print('Error: No knowledgebase present, please'  
    + '  compile first.')
    return
    
  if not os.path.isfile('database.dat'):
    print('Error: No database found.')
    return
    
  if not os.path.isfile(filename):
    print("Error: Input file not found.")
    #return
    
    
  knowledgebase = open('knowledgebase.dat', 'r')
  
  texts = tputil.split_database()
  
  
  for line in knowledgebase:
    data = str.split(line, '\t')
    word = data[0]
    occurence = int(data[1])
    
    '''
    Your job is basically implementing the comparison.
    'knowledgebase' contains the 70 most common words in
    all the texts. Currently it also contains random
    garbage like punctuation and such, but I'll
    tune it, don't worry about that.
    
    word = the 'words' in the knowledgebase
    occurance = the number of times it was in the text
    
    As far as I know this algorithm doesn't require
    labels and it doesn't need to know who wrote what,
    so texts that have the same author automatically 
    gravitate towards each other.
    
    the tputil.split_database() function returns all
    the previously added texts in an array. The last
    object is an empty(ish) string, I'll clean it up once
    I got some sleep. Feel free to use it as it is now, its
    interface won't change.
    '''
    
    
    
  knowledgebase.close()