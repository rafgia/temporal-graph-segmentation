def _edges_in_time_interval(timestamp2edges,t1,t2):
  edgeset = set()
  for t in range(t1,t2+1):
    edges_t = timestamp2edges[t]
    for edge in edges_t:
      edgeset.add(edge)
  return edgeset