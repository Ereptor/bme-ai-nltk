#!/usr/bin/python3
import sys
import tputil


def help():
  print('Unknown command. Usage: ' + sys.argv[0]
   + '\n \t -h \t\t\t --- Show this help dialog'
   + '\n \t add [filename]\t\t --- Add to database'
   + '\n \t compile \t\t --- Process the database'
   + '\n \t compare [filename] \t --- DO magic tricks')

  

# main function
if __name__ == '__main__':
  if len(sys.argv) > 2 :
    if sys.argv[1] == 'add':
      tputil.add_to_database(sys.argv[2])
    if sys.argv[1] == 'compare':
      tputil.compare(sys.argv[2])
  elif sys.argv[1] == 'compile':
    tputil.compile()
  else:
    help()