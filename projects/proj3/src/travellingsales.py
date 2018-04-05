from math import sqrt

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

def bnb_ts(points):
  """More enlightened approach, only search promising trees"""
  ## Doesn't matter where we start, pick any point
  state = {
    "placed": points[:1]
    "remaining": points[1:]
    "lower_bound": lower_bound(points[:1], points[1:])
  }
  solution = None
  queue = MinPriorityHeap()
  queue.insert(state, state['lower_bound'])
  while len(queue) != 0:
    curr = queue.extract_min
    if len(curr['remaining']) == 1:
      ## We have found a solution
      candidates = calc_next_states(curr)
      if solution:
        candidates.append(solution)
      solution = min(candidates, lamda x: x['lower_bound'])
      queue.prune(x['lower_bound'])
    else:
      ## Calculate the next states and add them to the queue
      next_states = calc_next_states(curr)
      for state in next_states:
        queue.insert(state, state['lower_bound'])
  return solution

def read_file(filename):
  """Reads in an input file into a list of points"""
  with open(filename, 'r') as fin:
    alllines = fin.read()
    points = []
    for line in alllines.split('\n'):
      x, y = map(int, line.split(' '))
      points.append((x, y))
  return points
