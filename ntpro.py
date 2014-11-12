#!/usr/bin/python3

#ntpro = NLTK text processor

import sys
import tputil
import tpcalc

def help():
  print('\nUsage: ' + sys.argv[0] + ' (option)'
  + '\n\nOptions:'
  + '\n \t -h \t\t\t --- Show this help dialog'
  + '\n \t add [filename]\t\t --- Add to database'
  + '\n \t compile-database \t\t --- Process the database'
  + '\n \t compile-texts \t\t --- Compile text files in \'texts\' folder'
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
    if sys.argv[1] == 'compile-texts':
      tputil.compile_texts()
    elif sys.argv[1] == 'compile-database':
      tputil.compile_database()
    elif sys.argv[1] == 'purge':
      tputil.purge()
  else:
    help()