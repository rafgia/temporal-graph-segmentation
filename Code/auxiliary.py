def compute_a_auxiliary_structure(nedges,ntimestamps,timestamp2edges):
  """
  Compute an auxiliary structure that tracks, for each timestamp, 
  how many times each edge has appeared up to that point.
  """
  prev = [0]*nedges
  a_aux = []
  for t in range(ntimestamps):
    for e in timestamp2edges[t]:
      prev[e] = prev[e] + 1
    a_aux.append(prev)
    prev = prev.copy()

  return a_aux
