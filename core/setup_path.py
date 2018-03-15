import sys
import os
pth_lst = os.getcwd().split('/')
del pth_lst[-1]
pth = '/'.join(pth_lst)
# add path to other sources
sys.path.insert(0, pth)
