import sys
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
    A = [None] * 10 ##XXX: Replace 10 with correct calculation
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
      for i in xrange(self.n + 1):
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

fh = FibonacciHeap()
fh.insert(1, 1)
fh.insert(2, 2)
fh.insert(3, 3)
fh.insert(4, 4)
print fh.extract_min()
print fh.extract_min()
print fh.extract_min()
print fh.extract_min()
