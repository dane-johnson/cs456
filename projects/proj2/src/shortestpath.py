import sys
INFINITY = sys.maxint

def ileft(i):
  return i * 2 + 1
def iright(i):
  return i * 2 + 2
def iparent(i):
  return (i - 1) / 2

class Node:
  def __init__(self, val, key):
    self.key = key
    self.val = val
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
    node.child = None
    node.mark = False
    if self.min == None:
      node.left = node
      node.right = node
      self.min = node
    else:
      self.min.right.left = node
      self.min.right = node
      if node.key < self.min.key:
        self.min = node
    self.n += 1

  def find_min(self):
    return self.min.val

## Merge list procedure
## min1.right.left = min2.left
## min2.left.right = min1.right
## min1.right = min2
## min2.left = min1
def fib_heap_union(heap1, heap2):
  new_heap = FibonacciHeap()
  if heap1.min = None:
    new_heap.min = heap2.min
  elif heap2.min = None:
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
