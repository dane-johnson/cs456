#!/usr/bin/env python2
import random
import time
from travellingsales import brute_force_ts, branch_and_bound_ts, dynamic_programming_ts, mst_approx_ts

N_MAX = 10

tests = {
  "BruteForce": (brute_force_ts, []),
  "BranchAndBound": (branch_and_bound_ts, []),
  "DynamicProgramming": (dynamic_programming_ts, []),
  "MSTApproximation": (mst_approx_ts, [])
}

random.seed(0)

for i in xrange(2, N_MAX + 1):
  graph = []
  for j in xrange(i):
    graph.append((random.randrange(50), random.randrange(50)))
  for test in tests:
    function, times = tests[test]
    t1 = time.time()
    function(graph)
    t2 = time.time
    times.append(t2 - t1)

with open('runs.csv', 'w') as fout:
  fout.write("ALGOS,N,TIME")
  for test in tests:
    function, times = tests[test]
    for i in xrange(2, N_MAX + 1):
      fout.write('%s,%d,%f\n' % (test, i, times[i-2]))
