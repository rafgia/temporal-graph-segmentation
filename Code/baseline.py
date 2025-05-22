from datetime import datetime
from load import load_graph
from find_split import find_split, split_piecewise
from hamming import hamming
from penalties import segment_penalty
from auxiliary import compute_a_auxiliary_structure


if __name__ == '__main__':
  start = datetime.now()
  nodes,node2id,timestamps,timestamp2id,edges,edge2id,timestamp2edges,snapshots,temporal_edges, new_temporal_dict = load_graph("graph_path.txt/csv", True,',')
  a_aux = compute_a_auxiliary_structure(len(edges),len(timestamps),timestamp2edges)
  nsegments = 44
  split = find_split(timestamps,nsegments)
  piecewise = split_piecewise(timestamps,split)
  
  sum_penalties = 0
  for i in range(0,len(piecewise)):
    sum_penalties += segment_penalty(a_aux,timestamp2edges, timestamp2id[piecewise[i][0]], timestamp2id[piecewise[i][-1]])
  print(sum_penalties)
  #print (piecewise)
  end = datetime.now()
  #print ("Hamming consensus vector: ", hamming_consensus_vectors = hamming(timestamp2edges,timestamp2id,piecewise))
  print ("Time: ", (end - start))
  print(piecewise[0])
  
