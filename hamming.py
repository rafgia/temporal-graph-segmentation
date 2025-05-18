def hamming(timestamp2edges,timestamp2id,piecewise):
  #create a dict where the key is the pair of edges and the value is the count
  hamming_consensus_vectors = []
  for piece in piecewise:
    hamming = []
    non_temporal_edges = []
    edges_in_piece = {}
    for snap in piece:
      edges = timestamp2edges[timestamp2id[snap]][0] #take the edge in the selected timestamp passing through id in timestamp2edges
      if edges not in non_temporal_edges:
        non_temporal_edges.append(edges)
        edges_in_piece[(edges)] = 1
      else:
        edges_in_piece[edges] += 1 #count the occurence of edge
    for key,value in edges_in_piece.items():
      if value > (len(timestamp2edges)/2): #the condition is that we take the edge only if the value is greater than half the len of the snap
        hamming.append(key)
    hamming_consensus_vectors.append(hamming)
  return hamming_consensus_vectors