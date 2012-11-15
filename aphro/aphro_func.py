from numpy import *
def aphro2global_one(a2org_one, dattype, miss):
  if dattype == "MA":
    a2glob = ones([180,360], float32)*miss
    a2glob[90-15: 90+54+1, 60:149+1] = a2org_one
    return a2glob
