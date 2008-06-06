from itertools import *

f = open("leitner/models.py")

(f1,f2,f3) = tee(f,3)
for l1,l2,l3 in zip(islice(f1,0,None,3),islice(f2,1,None,3),islice(f3,2,None,3)):
    print l1 + l2 + l3
    print "--"


