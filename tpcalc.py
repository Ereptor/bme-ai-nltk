import os.path

def compare(filename):
  if not os.path.isfile('knowledgebase.dat'):
    print('Error: No knowledgebase present, please compile'
    + ' first.')
    
    return
  
  knowledgebase = open('knowledgebase.dat', 'r')
  
  for line in knowledgebase:
    data = str.split(line, '\t')
    word = data[0]
    occurance = int(data[1])
    
    print(word + ' - ' + str(occurance))
    '''
    Your job is implementing the comparison 
    knowledgebase contains the 70 most common words in all the texts
    word is obviously the words in the knowledgebase
    and occurance is the number of times it was in the text
    
    
    '''
    
  
  knowledgebase.close()