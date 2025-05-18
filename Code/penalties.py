def _edges_in_time_interval(timestamp2edges,t1,t2):
  edgeset = set()
  for t in range(t1,t2+1):
    edges_t = timestamp2edges[t]
    for edge in edges_t:
      edgeset.add(edge)
  return edgeset

#Equation (6) in the draft
def segment_penalty_given_validedges(a_aux,valid_edges,t1,t2):
  interval_size = t2-t1+1
  penalty = 0
  for e in valid_edges:
    a1 = 0 if t1 == 0 else a_aux[t1-1][e]
    a2 = a_aux[t2][e]
    penalty = penalty + min(a2-a1, interval_size-(a2-a1))

  return penalty

def segment_penalty(a_aux,timestamp2edges,t1,t2):
  edges_t1t2 = _edges_in_time_interval(timestamp2edges,t1,t2)
  return segment_penalty_given_validedges(a_aux,edges_t1t2,t1,t2)
