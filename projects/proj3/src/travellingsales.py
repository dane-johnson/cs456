from math import sqrt
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
  configurations = permute(points)
  best = min(configurations, key=score)
  return best, proper_score(best)

def read_file(filename):
  """Reads in an input file into a list of points"""
  with open(filename, 'r') as fin:
    alllines = fin.read()
    points = []
    for line in alllines.split('\n'):
      x, y = map(int, line.split(' '))
      points.append((x, y))
  return points
