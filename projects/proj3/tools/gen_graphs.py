#!/usr/bin/env python2

import sys
import random
import string
from travellingsales import brute_force_ts

def main():
  if len(sys.argv) > 2:
    usage()
  if len(sys.argv) == 1:
    ngraphs = 1
  else:
    ngraphs = int(sys.argv[1])

  random.seed()
  for i in xrange(ngraphs):
    nverticies = random.randrange(4, 10)
    points = []
    for j in xrange(nverticies):
      points.append((random.randrange(30), random.randrange(30)))
    _, solution = brute_force_ts(points)
    with open("graphs/samples/%s.graph" % string.ascii_uppercase[i], 'w') as fout:
      for point in points:
        x, y = point
        fout.write("%d %d\n" % (x, y))
    with open("graphs/solutions/%s.solution" % string.ascii_uppercase[i], 'w') as fout:
      fout.write("%f" % solution)


def usage():
  print "Usage: %s [ngraphs]" % sys.argv[0]
  exit(1)

if __name__ == "__main__":
  main()
