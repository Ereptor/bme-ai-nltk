#tpcalc = text processor calculations

import os.path
import sys
import tputil



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
    print('[ERROR]: No knowledgebase present, please' + '  compile first.')
    sys.exit(tputil.NO_KNOWLEDGEBASE)
  elif not os.path.isfile(filename):
    print('[ERROR]: File not found')
    sys.exit(tputil.FILE_NOT_FOUND)
  
  knowledgebase = tputil.get_knowledgebase()
  
  new_point = tputil.get_file_frequency(filename, knowledgebase[tputil.KNOWLEDGEBASE_KEY_WORDS]) # new, because this should be the one loaded from the file
  
  goodpoints = knowledgebase[tputil.KNOWLEDGEBASE_KEY_FREQS]
  center = tputil.center_point(goodpoints)
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