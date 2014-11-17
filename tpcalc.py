#tpcalc = text processor calculations

import os.path
import tputil
import numpy
from matplotlib.mlab import PCA



#MAX_DIST_PRC = 85
AVG_DIST_PRC = 85


## 
## Sorry in advance for my messing your function up,
## I used it as a kind of sketchboard while I was prettying
## my own code up.
##
## Also, since I removed the old implementation of the PCA algorithm
## it now calculates its estimates with the original values.
## It actually seems to be more on target, the non-Shakespearian texts score at
## around 50-60 percent, with Tartuffe having 52 instead of the old 60+ points.
##
## And on a final note, it now operates out of a file, not from the texts folder
## and is now independent of the number of sources. As far as I see
## functionality-wise it works as intended, it's the innards that are less than
## presentable.
##

def compare(filename):
  if not os.path.isfile('knowledgebase.dat'):
    print('[ERROR]: No knowledgebase present, please'  
    + '  compile first.')
    sys.exit(tputil.NO_KNOWLEDGEBASE)
  elif not os.path.isfile(filename):
    print('[ERROR]: File not found')
    sys.exit(tputil.FILE_NOT_FOUND)
    
  
#  if not os.path.isfile(filename):
#    print("Error: Input file not found.")
    #return
    
  # for now, until we write a better one
  text_count = tputil.get_text_count()
  knowledgematrix = numpy.empty((text_count, tputil.MOST_COMMON_NUMBER))
  
  inputtext = open(filename).read()
  
  
  for i in range(0,text_count):
    knowledgematrix[i] = tputil.get_text_frequency(i)
  
  #goodpoints = tputil.PCA_result(knowledgematrix) # this will be moved to tputil
  goodpoints = knowledgematrix[:4]
  center = tputil.center_point(goodpoints)
  new_point = tputil.get_frequency(inputtext) # new, because this should be the one loaded from the file
  #new_point = knowledgematrix[0]
  dist_average = 0
#  dist_max = 0
  for point in goodpoints:
    dist = tputil.dist(center, point)
    dist_average += dist
#    dist_max = max(dist_max, dist)
  
  dist_average /= len(goodpoints)
  
  dist_new = tputil.dist(center, new_point)
  
  dist_single_prc = (dist_average) / (100-AVG_DIST_PRC)
  
  act_prc = min(max(100-(dist_new / dist_single_prc),0),100)
  print(r'Estimated stylistic similarity to author is %.2f percent.'%act_prc)