import os
import sys
import copy
import math
from collections import OrderedDict

INFINITY = sys.maxint

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
  return math.floor(math.log(n)/math.log(2))
  

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
      smallest = ileft(i)
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

  def insert(self, x, key):
    self.heap.append(Node(x, INFINITY))
    self.decrease_key(len(self.heap) - 1, key)

class FibonacciHeap:
  def __init__(self):
    self.n = 0
    self.min = None

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
      node.left = self.min.right
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
    y.mark = False

def fib_heap_union(heap1, heap2):
  new_heap = FibonacciHeap()
  if heap1.min == None:
    new_heap.min = heap2.min
  elif heap2.min == None:
    new_heap.min = heap1.min
  else:
    heap1.min.right.left = heap2.min.left
    heap2.min.left.right = heap1.min.right
    heap1.min.right = heap2.min
    heap2.min.left = heap1.min
    if heap1.min.key < heap2.min.key:
      new_heap.min = heap1.min
    else:
      new_heap.min = heap2.min
  new_heap.n = heap1.n + heap2.n

#################### JOHNSON ####################



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

def main():
  if len(sys.argv) != 2:
    usage()
  else:
    with open(sys.argv[1], "r") as fin:
      alllines = fin.read()
    graph = parse(alllines)
    apsp = floyd_warshall(graph)
    with open(os.path.basename(sys.argv[1]) + "Out.txt", "w") as fout:
      for row in apsp:
        for val in row:
          fout.write("%d " % val)
        fout.write("\n")

def usage():
  print "Usage: %s filename" % sys.argv[0]
  quit()

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
