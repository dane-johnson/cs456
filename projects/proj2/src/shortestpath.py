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
