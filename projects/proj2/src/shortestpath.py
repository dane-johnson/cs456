import os
import sys
import time
import copy
import math
from collections import OrderedDict

INFINITY = float('inf')
JOHNSON_KEY = "JOHNSON_KEY"

def ileft(i):
  return i * 2 + 1
def iright(i):
  return i * 2 + 2
def iparent(i):
  return (i - 1) / 2

def dll_iterator(dll):
  """Generates an iterator to loop over a doubly linked list"""
  curr = dll
  if curr == None:
    return
  mylist = [curr]
  curr = curr.right
  while curr != dll:
    mylist.append(curr)
    curr = curr.right
  return mylist

def D(n):
  """D(n) = floor(lg(n))"""
  return int(math.floor(math.log(n)/math.log(2))) + 1
  

class Node:
  def __init__(self, val, key):
    self.key = key
    self.val = val
    self.right = self
    self.left = self
    self.parent = None
    self.child = None
    
  def __repr__(self):
    return str(self.__dict__)
  
class MinPriorityHeap:
  def __init__(self):
    self.heap = []

  def __len__(self):
    return len(self.heap)
  def heap_swap(self, i, j):
    "Swaps two values of the heap"
    temp = self.heap[i]
    self.heap[i] = self.heap[j]
    self.heap[j] = temp

  def heapify(self, i):
    "Restores the heap property to the heap"
    smallest = i
    if ileft(i) < len(self.heap) and self.heap[ileft(i)].key < self.heap[smallest].key:
      smallest = ileft(i)
    if iright(i) < len(self.heap) and self.heap[iright(i)].key < self.heap[smallest].key:
      smallest = iright(i)
    if smallest != i:
      self.heap_swap(i, smallest)
      self.heapify(smallest)

  def extract_min(self):
    "Removes the minimum value of the heap"
    my_min = self.heap[0]
    self.heap[0] = self.heap[-1]
    self.heap.pop()
    self.heapify(0)
    return my_min.val

  def decrease_key(self, i, key):
    "Decreases the priority of the element at i"
    if key > self.heap[i].key:
      raise Exception("New key is larger than current key")
    self.heap[i].key = key
    while i > 0 and self.heap[iparent(i)].key > self.heap[i].key:
      self.heap_swap(i, iparent(i))
      i = iparent(i)

  def get_index(self, x):
    for i, node in enumerate(self.heap):
      if node.val == x:
        return i

  def insert(self, x, key):
    self.heap.append(Node(x, INFINITY))
    self.decrease_key(len(self.heap) - 1, key)

class FibonacciHeap:
  def __init__(self):
    self.n = 0
    self.min = None

  def __len__(self):
    return self.n

  def insert(self, x, key):
    node = Node(x, key)
    node.degree = 0
    node.parent = None
    node.child = None
    node.mark = False
    if self.min == None:
      node.left = node
      node.right = node
      self.min = node
    else:
      node.right = self.min.right
      self.min.right.left = node
      node.left = self.min
      self.min.right = node
      if node.key < self.min.key:
        self.min = node
    self.n += 1

  def find_min(self):
    return self.min.val

  def extract_min(self):
    my_min = self.min
    if my_min:
      ## Move all children of min to the root list
      if my_min.child:
        for child in dll_iterator(my_min.child):
          child.right = self.min.right
          self.min.right.left = child
          child.left = self.min
          self.min.right = child
          child.parent = None
      ## remove the min from the root list
      self.min.right.left = self.min.left
      self.min.left.right = self.min.right
      if my_min == my_min.right:
        self.min = None
      else:
        self.min = my_min.right
        self.consolidate()
      self.n -= 1
    return my_min.val

  def consolidate(self):
    """Recombine the heaps"""
    A = [None] * (D(self.n) + 1)
    if self.min:
      for node in dll_iterator(self.min):
        x = node
        d = x.degree
        while A[d]:
          y = A[d]
          if x.key > y.key:
            temp = x
            x = y
            y = temp
          self.heap_link(y, x)
          A[d] = None
          d += 1
        A[d] = x
      self.min = None
      for i in xrange(D(self.n) + 1):
        if A[i]:
          if self.min == None:
            ## Create the root list
            self.min = A[i]
            self.min.right = self.min
            self.min.left = self.min
          else:
            ## add to root list
            self.min.right.left = A[i]
            A[i].right = self.min.right
            self.min.right = A[i]
            A[i].left = self.min
            if A[i].key < self.min.key:
              self.min = A[i]

  def heap_link(self, y, x):
    ## Remove y from root list
    y.left.right = y.right
    y.right.left = y.left 
    y.right = y
    ## Make y a child of x
    if x.child:
      x.child.right.left = y
      y.right = x.child.right
      x.child.right = y
      y.left = x.child
    else:
      y.right = y
      y.left = y
      x.child = y
    x.degree += 1
    y.parent = x
    y.mark = False

  def decrease_key(self, x, k):
    if k > x.key:
      raise Exception("New key is larger than current key")
    else:
      x.key = k
      y = x.parent
      if y and x.key < y.key:
        self.cut(x, y)
        self.cascading_cut(y)
      if x.key < self.min.key:
        self.min = x

  def cut(self, x, y):
    ## Remove x from y's list and decrement y.degree
    x.right.left = x.left
    x.left.right = x.right
    if y.child == x and x != x.right:
      y.child = x.right
    elif y.child == x:
      y.child = None
    y.degree -= 1

    ## Add x to the min root list
    x.right = self.min.right
    self.min.right.left = x
    x.left = self.min
    self.min.right = x
    if x.key < self.min.key:
      self.min = x
      
    x.parent = None
    x.mark = False

  def cascading_cut(self, y):
    z = y.parent
    if z:
      if not y.mark:
        y.mark = True
      else:
        self.cut(y, z)
        self.cascading_cut(z)

  def get_index(self, val):
    queue = [self.min]
    while len(queue) > 0:
      curr = queue.pop()
      for node in dll_iterator(curr):
        if node.val == val:
          return node
        if node.child:
          queue.insert(0, node.child)

#################### BELLMAN-FORD ####################

def bellman_ford(graph, source):
  """Performs the bellman-ford SSSP algorithm"""
  distance = {}
  predecessor = {}
  edges = []
  
  for src in graph:
    distance[src] = INFINITY
    predecessor[src] = None
    for dest in graph[src]:
      edges.append((src, dest, graph[src][dest]))
  distance[source] = 0

  for i in xrange(len(graph) - 1):
    for src, dest, w in edges:
      if distance[src] + w < distance[dest]:
        distance[dest] = distance[src] + w
        predecessor[dest] = src

  for src, dest, w in edges:
    if distance[src] + w < distance[dest]:
      raise Exception("Graph contains a negative weight cycle")

  return distance, predecessor

#################### DIJKSTRA ####################

def dijkstra(graph, source, unvisited):
  """Dijkstra's algorithm using a passed in data structure for unvisited"""
  distance = OrderedDict()
  
  for src in graph:
    unvisited.insert(src, INFINITY)
    distance[src] = INFINITY
    
  distance[source] = 0
  unvisited.decrease_key(unvisited.get_index(source), 0)
  
  while len(unvisited) > 0:
    src = unvisited.extract_min()
    for dest in graph[src]:
      if distance[dest] > distance[src] + graph[src][dest]:
        distance[dest] = distance[src] + graph[src][dest]
        unvisited.decrease_key(unvisited.get_index(dest), distance[dest])

  return distance.values()

def dijkstra_min_heap(graph, source):
  """Dijkstra's algorith implemented with a Min Priority Heap"""
  unvisited = MinPriorityHeap()
  return dijkstra(graph, source, unvisited)

def dijkstra_fibonacci(graph, source):
  """Dijkstra's algorithm implemented with a Fibonacci Heap"""
  unvisited = FibonacciHeap()
  return dijkstra(graph, source, unvisited)

#################### JOHNSON ####################

def johnson(graph, dijkstra):
  """Runs Johnson's algorithm on a graph. Must be given an implementation of Dijkstra's algorithm"""
  my_graph = copy.deepcopy(graph)
  new_node = {}
  for node in my_graph:
    new_node[node] = 0
  my_graph[JOHNSON_KEY] = new_node

  ## This will throw an exception if there are negative weight cycles
  distance, predecessor = bellman_ford(my_graph, JOHNSON_KEY)
  for src in my_graph:
    for dest in my_graph:
      if dest in my_graph[src]:
        my_graph[src][dest] += (distance[src] - distance[dest])
  del my_graph[JOHNSON_KEY]

  adj_matrix = []
  for src in my_graph:
    prime = dijkstra(my_graph, src)
    for j, dest in enumerate(my_graph):
      prime[j] += (distance[dest] - distance[src])
    adj_matrix.append(prime)
    
    ## Make infinities -1 to match sample output      
  retval = copy.deepcopy(adj_matrix)
  for i, row in enumerate(retval):
    for j, val in enumerate(row):
      if val >= INFINITY:
        retval[i][j] = -1
  return retval

def johnson_min_heap(graph):
  """Runs Johnson's algorithm, using Min Heap implementation of Dijkstra's algorithm"""
  return johnson(graph, dijkstra_min_heap)

def johnson_fibonacci_heap(graph):
  """Runs Johnson's algorithm, using MinHeap implementation of Dijkstra's algotrihm"""
  return johnson(graph, dijkstra_fibonacci)

#################### FLOYD-WARSHALL ####################

def floyd_warshall(graph):
  n = len(graph)
  W = make_adj_matrix(graph)
  
  D = [0] * (n + 1)
  P = [0] * (n + 1)
  for i in xrange(n + 1):
    D[i] = [0] * n
    P[i] = [0] * n
    for j in xrange(n):
      D[i][j] = [0] * n
      P[i][j] = [0] * n

  D[0] = copy.deepcopy(W)
  for i, v in enumerate(D[0]):
    for j, w in enumerate(D[0][i]):
      if D[0][i][j] == 0 or D[0][i][j] == INFINITY:
        P[0][i][j] = None
      else:
        P[0][i][j] = i

  for h in xrange(1, n + 1):
    for i in xrange(n):
      for j in xrange(n):
        D[h][i][j] = min(D[h-1][i][j], D[h-1][i][h-1] + D[h-1][h-1][j])
        if D[h][i][j] > D[h-1][i][h-1] + D[h-1][h-1][j]:
          P[h][i][j] = P[h][h-1][j]
          
  ## Make infinities -1 to match sample output      
  retval = copy.deepcopy(D[n])
  for i, row in enumerate(retval):
    for j, val in enumerate(row):
      if val >= INFINITY:
        retval[i][j] = -1
  return retval

def make_adj_matrix(graph):
  adj_matrix = [0] * len(graph)
  for i, start in enumerate(graph):
    adj_matrix[i] = [0] * len(graph)
    for j, dest in enumerate(graph):
      if dest == start:
        adj_matrix[i][j] = 0
      elif dest in graph[start]:
        adj_matrix[i][j] = graph[start][dest]
      else:
        adj_matrix[i][j] = INFINITY
  return adj_matrix

def find_average_time(graph, fn, n=10):
  """Runs the given algorithm n times and returns the output and average time"""
  times = []
  for i in xrange(n):
    t1 = time.time()
    out = fn(graph)
    t2 = time.time()
    times.append(t2 - t1)
  avg = sum(times) / n
  return out, avg

def write_adj_list(fout, adj_list):
  for row in adj_list:
    for val in row:
      fout.write("%d " % val)
    fout.write("\n")

def main():
  if len(sys.argv) != 2:
    usage()
  else:
    alllines = readfile(sys.argv[1])
    graph = parse(alllines)
    fw_out, fw_time = find_average_time(graph, floyd_warshall)
    jmh_out, jmh_time = find_average_time(graph, johnson_min_heap)
    fh_out, fh_time = find_average_time(graph, johnson_fibonacci_heap)
    with open(os.path.splitext(os.path.basename(sys.argv[1]))[0] + "Out" + os.path.splitext(sys.argv[1])[1], "w") as fout:
      fout.write("Floyd-Warshall time: %f seconds\n" % fw_time)
      fout.write("Johnson Min-Priority-Heap time: %f seconds\n" % jmh_time)
      fout.write("Johnson Fibonacci-Heap time: %f seconds\n" % fh_time)
      fout.write("--------------------FLOYD-WARSHALL--------------------\n")
      write_adj_list(fout, fw_out)
      fout.write("--------------------JOHNSON-MIN-PRIORITY-HEAP--------------------\n")
      write_adj_list(fout, jmh_out)
      fout.write("--------------------JOHNSON-FIBONACCI-HEAP--------------------\n")
      write_adj_list(fout, fh_out)

def usage():
  print "Usage: %s filename" % sys.argv[0]
  quit()

def readfile(filename):
  with open(filename, "r") as fin:
    alllines = fin.read()
  return alllines

def parse(alllines):
  graph = OrderedDict()
  for line in alllines.splitlines():
    nums = line.split(" ")
    key = nums[0]
    graph[key] = OrderedDict()
    for vw in nums[1:]:
      v, w = vw.split(":")
      graph[key][v] = int(w)
  return graph

if __name__ == "__main__":
  main()

