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
  cost = [{}]
  path = [{}]
  for p in rest:
    ## Initialize all 2 sets to be the distance to the source
    cost[0][frozenset([source, p])] = dist_sqrd(source, p)
    path[0][frozenset([source, p])] = [source, p]

  for i in xrange(len(points) - 3): ## Do this for all but the first and last 2 connections
    cost.append({})
    path.append({})
    for v in rest:
      for s in cost[i].keys(): ## For each i - 1 set
        min_cost = float('inf')
        best_path = []
        if v in s:
          continue ## Skip if this point is already in the set
        for u in s:
          ## Find the shortest connection to add v into the set, not from the source
          if u != source and cost[i][s] + dist_sqrd(u, v) < min_cost:
            min_cost = cost[i][s] + dist_sqrd(u, v)
            best_path = path[i][s] + [v]
        if (not s | frozenset([v]) in cost[i + 1]) or min_cost < cost[i + 1][s | frozenset([v])]:
          cost[i + 1][s | frozenset([v])] = min_cost
          path[i + 1][s | frozenset([v])] = best_path

  ## For the last connection, also consider return cost
  min_cost = float('inf')
  best_path = []
  for v in rest:
    for s in cost[-1].keys():
      if v in s:
        continue ## Only select connections with v absent
      for u in s:
        ## Find the shortest connection to add v to the set, not from the source,
        ## and connect v back to the source
        if u != source and cost[-1][s] + dist_sqrd(u, v) + dist_sqrd(v, source) < min_cost:
          min_cost = cost[-1][s] + dist_sqrd(u, v) + dist_sqrd(v, source) < min_cost
          best_path = path[-1][s] + [v]
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
