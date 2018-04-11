import sys
from math import sqrt
from copy import deepcopy

from shortestpath import MinPriorityHeap

def dist_sqrd(p1, p2):
  """Calculate distance between two points squared"""
  x1, y1 = p1
  x2, y2 = p2
  return (y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1)

def dist(p1, p2):
  """Calculate distance between two points"""
  return sqrt(dist_sqrd(p1, p2))

def score(configuration):
  """Quickly score a configuration"""
  total = dist_sqrd(configuration[-1], configuration[0])
  for p1, p2 in zip(configuration[:-1], configuration[1:]):
    total += dist_sqrd(p1, p2)
  return total

def proper_score(configuration):
  """Find the distance travelled in a configuration"""
  total = dist(configuration[-1], configuration[0])
  for p1, p2 in zip(configuration[:-1], configuration[1:]):
    total += dist(p1, p2)
  return total

def permute(points):
  """Try all points in every order"""
  if len(points) == 1:
    return [points]
  configurations = []
  for i, point in enumerate(points):
    for permutation in permute(points[:i] + points[i+1:]):
      configurations.append([point] + permutation)
  return configurations

def brute_force_ts(points):
  """Slow, try-everything approach"""
  ## Doesn't matter where we start, pick any point
  src = points[0]
  configurations = map(lambda x: [src] + x, permute(points[1:]))
  best = min(configurations, key=score)
  return best, proper_score(best)

def lower_bound(placed, remaining):
  """Calculates the lower bound of the current state by taking established path, and
  guessing the shortest path on remaining edges"""
  ## Calculate the cost of the connections in the placed vertices
  ## (x2 because it will be averaged later)
  cost = 0
  for u, v in zip(placed[:-1], placed[1:]):
    cost += dist_sqrd(u, v) * 2

  ## Add in the best case for all remaining edges
  for u in remaining:
    smallest = float('inf')
    next_smallest = float('inf')
    for v in remaining + placed:
      if u == v:
        ## Don't connect to self
        continue
      val = dist_sqrd(u, v)
      if val < smallest:
        next_smallest = smallest
        smallest = val
      elif cost < next_smallest:
        next_smallest = val
    cost += smallest + next_smallest
  ## Add in the cost of returning to the source
  if len(remaining) == 0:
    cost += dist_sqrd(placed[0], placed[-1]) * 2
  else:
    cost += min(map(lambda x: dist_sqrd(placed[0], x), remaining))
  return cost / 2

def calc_next_states(state):
  next_states = []
  for i, p in enumerate(state['remaining']):
    s = {
      'placed': state['placed'] + [p],
      'remaining': state['remaining'][:i] + state['remaining'][i+1:],
      'lower_bound': lower_bound(state['placed'] + [p], state['remaining'][:i] + state['remaining'][i+1:])
    }
    next_states.append(s)
  return next_states

def expand_path(placed, remaining, cheapest):
  children = []
  print placed, remaining, lower_bound(placed, remaining)
  for i, p in enumerate(remaining):
    print placed + [p], remaining[:i] + remaining[i+1:], lower_bound(placed + [p], remaining[:i] + remaining[i+1:])
    child = {
      'placed': placed + [p],
      'remaining': remaining[:i] + remaining[i+1:],
      'lower_bound': lower_bound(placed + [p], remaining[:i] + remaining[i+1:])
    }
    children.append(child)
  children.sort(key=lambda x: x['lower_bound'])
  best = None
  for child in children:
    print cheapest, child['lower_bound']
    if child['lower_bound'] < cheapest:
      path, cost = expand_path(child['placed'], child['remaining'], cheapest)
      if cost < cheapest:
        cheapest = cost
        best = path
  return best, cheapest

def branch_and_bound_ts(points):
  """More enlightened approach, only search promising trees"""
  ## Doesn't matter where we start, pick any point
  placed = points[:1]
  remaining = points[1:]
  path, _ = expand_path(placed, remaining, float('inf'))
  return path, proper_score(path)

def dynamic_programming_ts(points):
  """Solves TSP with dynamic programming. Takes a lot of space"""
  ## Pick a source. It doesn't matter which
  source = points[0]
  rest = points[1:]
  cost = {}
  path = {}

  for i in rest:
    ## Create all length 2 subsets
    key = (frozenset([source, i]), i)
    cost[key] = dist_sqrd(source, i)
    path[key] = [source, i]

  for size in xrange(3, len(points) + 1):
    ## Loop through n - 2 more times to create all subsets of n size
    subsets = filter(lambda x: len(x) == size - 1, map(lambda x: x[0], cost.keys()))
    for S in subsets:
      for i in rest:
        if i in S:
          ## This doesn't generate a new subset
          continue
        min_cost = float('inf')
        for j in rest:
          if not j in S or j == i or j == source:
            ## These cases are not allowed
            continue
          if cost[(S, j)] + dist_sqrd(i, j) < min_cost:
            min_cost = cost[(S, j)] + dist_sqrd(i, j)
            best_path = path[(S, j)] + [i]
        key = (S | frozenset([i]), i)
        cost[key] = min_cost
        path[key] = best_path

  min_cost = float('inf')
  for S, i in filter(lambda x: len(x[0]) == len(points), cost.keys()):
    ## Look through all the n length sets, find the shortest path to close the loop
    key = (S, i)
    if cost[key] + dist_sqrd(source, i) < min_cost:
      min_cost = cost[key] + dist_sqrd(source, i)
      best_path = path[key]
  return best_path, proper_score(best_path)

def mst_approx_ts(points):
  """Quickly approximates a TSP, sacrificing precision for time."""
  dist = {}
  for p in points:
    dist[p] = float('inf')
  dist[points[0]] = 0
  queue = MinPriorityHeap()
  for p in points:
    queue.insert(p, dist[p])

  path = []
  while len(queue) > 0:
    u = queue.extract_min()
    path.append(u)
    for v in points:
      if v in set(path):
        ## Ignore this edge, out of the list
        continue
      cost = dist_sqrd(u, v)
      if cost < dist[v]:
        dist[v] = cost
        queue.decrease_key(queue.get_index(v), cost)
        
  return path, proper_score(path)

def read_file(filename):
  """Reads in an input file into a list of points"""
  with open(filename, 'r') as fin:
    alllines = fin.read()
    points = []
    for line in alllines.split('\n'):
      if line == '':
        break
      x, y = map(int, line.split(' '))
      points.append((x, y))
  return points

def print_solution(path, score):
  printed_path = ""
  for p in path:
    printed_path += "%s -> " % (p,)
  printed_path += "%s" % (path[0],)
  print "Path: %s" % printed_path
  print "Cost: %f" % score

def usage():
  print "Usage: %s inputfile" % sys.argv[0]
  exit(1)

def main(algo):
  if len(sys.argv) != 2:
    usage()
  points = read_file(sys.argv[1])
  solution = algo(points)
  print_solution(*solution)
