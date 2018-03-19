import os
import shortestpath

densedir = './graphs/sample-graphs/dense-graphs/'
sparsedir = './graphs/sample-graphs/sparse-graphs/'
algorithms = [(shortestpath.floyd_warshall, "Floyd-Warshall"), (shortestpath.johnson_min_heap, "Johnson-Min-Heap")]

def main():
  sparse_files = os.listdir(sparsedir)
  dense_files = os.listdir(densedir)
  with open("trials.csv", "w") as fout:
    fout.write("FILE,ALGO,TIME\n")
    for fileset, dirname in [(sparse_files, sparsedir), (dense_files, densedir)]:
      for filename in fileset:
        graph = shortestpath.parse(shortestpath.readfile(dirname + filename))
        for algorithm, algoname in algorithms:
          _, time = shortestpath.find_average_time(graph, algorithm)
          fout.write("%s,%s,%f\n" % (filename, algoname, time))

if __name__ == "__main__":
  main()
