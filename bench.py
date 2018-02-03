#!/usr/bin/env python2

import subprocess
import time

executable = "./projects/proj1/benchmark"
functions = ["quicksort_array", "quicksort_list", "mergesort_array", "mergesort_list"]
nums = range(0, 25000, 100)

def main():
  with open('reports/proj1/runs.csv', 'w') as f:
    for fn in functions:
      print "Testing %s" % fn
      for num in nums:
        start = time.time()
        subprocess.call([executable, fn, str(num)])
        end = time.time()
        f.write("%s, %d, %f\n" % (fn, num, (end - start) * 1000))

if __name__ == '__main__':
    main()
        
      
