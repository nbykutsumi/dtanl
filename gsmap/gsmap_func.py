from numpy import *

def gsmap2global_one(a2org_one, miss):
  a2glob = ones([180,360], float32)*miss
  a2glob[30:149+1,:] = a2org_one
  return a2glob

