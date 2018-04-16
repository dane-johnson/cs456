#!/usr/bin/env python2
import random
from travellingsales import brute_force_ts, branch_and_bound_ts, dynamic_programming_ts, mst_approx_ts

N_MAX = 15

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
    function, scores = tests[test]
    _, score = function(graph)
    scores.append(score)

with open('runs.csv', 'w') as fout:
  for test in tests:
    function, scores = tests[test]
    for i in xrange(2, N_MAX + 1):
      fout.write('%s,%d,%f\n' % (test, i, scores[i-2]))
