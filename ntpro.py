#!/usr/bin/python3

#ntpro = NLTK text processor

import sys
import tputil
import tpcalc
import numpy

def help():
  print('\nUsage: ' + sys.argv[0] + ' (option)'
  + '\n\n[Options]:'
  + '\n \t help \t\t\t\t\t --- Show this help dialog'
  + '\n'
  + '\n \t add [filename]\t\t\t\t --- Add to database'
  + '\n \t add-fingerprint \t\t\t --- Add fingerprint from folder'
  + '\n \t compile-database {[-sm] [language]}  \t --- Process the database, -sm: stopwords mode on'
  + '\n \t compare [filename] \t\t\t --- Analyse stylistic resemblence'
  + '\n \t plot [filename]\t\t\t --- Show graph'
  + '\n \t purge \t\t\t\t\t --- Delete data- and knowledgebase'
  + '\n \t full-setup \t\t\t\t --- purge->add-fingerprint->compile-database'
  + '\n'
  + '\nDefault language with -sm flag: english. Other options: see nltk documentation for stopword languages.')

  

# main function
if __name__ == '__main__':
  
  if len(sys.argv) == 4 :
    if sys.argv[1] == 'compile-database' and sys.argv[2] == '-sm':
      tputil.compile_database(True, sys.argv[3])
  elif len(sys.argv) == 3 :
    if sys.argv[1] == 'add':
      tputil.add_to_database(sys.argv[2])
    elif sys.argv[1] == 'compare':
      tpcalc.compare(sys.argv[2])
    elif sys.argv[1] == 'plot':
      tputil.plot(sys.argv[2])
    elif sys.argv[1] == 'compile-database' and sys.argv[2] == '-sm':
      tputil.compile_database(True)
    else:
      help()
  elif len(sys.argv) == 2:
    if sys.argv[1] == 'add-fingerprint':
      tputil.add_texts()
    elif sys.argv[1] == 'compile-database':
      tputil.compile_database()
    elif sys.argv[1] == 'purge':
      tputil.purge()
    elif sys.argv[1] == 'full-setup':
      tputil.purge()
      tputil.add_texts()
      tputil.compile_database()
    else:
      help()
  else:
    help()