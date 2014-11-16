import os.path
import tputil
import numpy
from matplotlib.mlab import PCA

#tpcalc = text processor calculations

MAX_DIST_PRC = 85
AVG_DIST_PRC = 90

def compare(filename):
  if not os.path.isfile('knowledgebase.dat'):
    print('Error: No knowledgebase present, please'  
    + '  compile first.')
    return
    
#  if not os.path.isfile(filename):
#    print("Error: Input file not found.")
    #return
    
  # for now, until we write a better one
  text_count = tputil.get_text_count()
  knowledgematrix = numpy.empty((text_count, tputil.MOST_COMMON_NUMBER))
  
  for i in range(0,text_count):
    knowledgematrix[i] = tputil.get_text_frequency(i)
  
  result_pca = PCA(knowledgematrix) # this will be moved to tputil
  goodpoints = result_pca.Y[:5]
  center = tputil.center_point(goodpoints)
  new_point = result_pca.Y[5] # new, because this should be the one loaded from the file
  dist_average = 0
  dist_max = 0
  for point in goodpoints:
    dist = tputil.dist(center, point)
    dist_average += dist
    dist_max = max(dist_max, dist)
  
  dist_average /= len(goodpoints)
  
  dist_new = tputil.dist(center, new_point)
  
  dist_single_prc = (dist_max - dist_average) / (AVG_DIST_PRC-MAX_DIST_PRC)
  
  act_prc = max(100-(dist_new / dist_single_prc),0)
  print('The text is %f to be written by the same author'%act_prc)
  