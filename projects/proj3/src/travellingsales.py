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
  """Calculates the lower bound of the current state by
  multiplying the cheapest edge by the number of
  edges needed to complete the circuit"""
  if len(remaining) <= 1:
    return score(placed + remaining)
  shortest = dist_sqrd(remaining[0], remaining[1])
  for i, u in enumerate(remaining):
    for v in remaining[:i] + remaining[i+1:]:
      if dist_sqrd(u, v) < shortest:
        shortest = dist_sqrd(u, v)
        
  distance = 0
  for u in placed[:-1]:
    for v in placed[1:]:
      distance += dist_sqrd(u, v)
      
  return distance + shortest * (len(remaining) + 1)

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

def branch_and_bound_ts(points):
  """More enlightened approach, only search promising trees"""
  ## Doesn't matter where we start, pick any point
  state = {
    "placed": points[:1],
    "remaining": points[1:],
    "lower_bound": lower_bound(points[:1], points[1:])
  }
  solution = None
  queue = MinPriorityHeap()
  queue.insert(state, state['lower_bound'])
  while len(queue) != 0:
    curr = queue.extract_min()
    if len(curr['remaining']) == 1:
      ## We have found a solution
      candidates = calc_next_states(curr)
      if solution:
        candidates.append(solution)
      solution = min(candidates, key=lambda x: x['lower_bound'])
      queue.prune(solution['lower_bound'])
    else:
      ## Calculate the next states and add them to the queue
      next_states = calc_next_states(curr)
      for state in next_states:
        queue.insert(state, state['lower_bound'])
  return solution['placed'], proper_score(solution['placed'])

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
