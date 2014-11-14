#!/usr/bin/python3

#ntpro = NLTK text processor

import sys
import tputil
import tpcalc

def help():
  print('\nUsage: ' + sys.argv[0] + ' (option)'
  + '\n\nOptions:'
  + '\n \t help \t\t\t --- Show this help dialog'
  + '\n'
  + '\n \t add [filename]\t\t --- Add to database'
  + '\n \t add-texts \t\t --- Add text files to database in \'texts\' folder'
  + '\n \t compile-database \t --- Process the database'
  + '\n \t plot \t\t\t --- Show graph representing the distribution of datapoints.'
  + '\n \t compare [filename] \t --- Do magic tricks'
  + '\n \t purge \t\t\t --- Delete data- and knowledgebase'
  + '\n')

  

# main function
if __name__ == '__main__':
  if len(sys.argv) > 2 :
    if sys.argv[1] == 'add':
      tputil.add_to_database(sys.argv[2])
    elif sys.argv[1] == 'compare':
      tpcalc.compare(sys.argv[2])
    else:
      help()
  elif len(sys.argv) == 2:
    if sys.argv[1] == 'add-texts':
      tputil.add_texts()
    elif sys.argv[1] == 'compile-database':
      tputil.compile_database()
    elif sys.argv[1] == 'purge':
      tputil.purge()
    elif sys.argv[1] == 'plot':
      tputil.plotPCA()
    elif sys.argv[1] == 'full-setup':
      tputil.purge()
      tputil.add_texts()
      tputil.compile_database()
  else:
    help()