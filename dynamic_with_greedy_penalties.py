from datetime import datetime
import numpy as np
from auxiliary import compute_a_auxiliary_structure
from load import load_graph
from penalties import segment_penalty
from unique_snapshots import dict_to_csv

def tgagg(timestamps_edges,timestamp_id,auxiliary_vector,k):
  #inverted_dict = {value: key for key, value in timestamp2id.items()} #aggiunto per invertire chiave(che ora è timestamp) con valore(che ora è id)
  Time = timestamp_id
  P = [[0 for j in range(k)] for i in range(len(timestamp_id.values()))] #penalty matrix
  R = [[0 for j in range(k)] for i in range(len(timestamp_id.values()))] #reconstruction matrix
  for i in range(len(Time.values())):
    p = [0 for s in range(i,-1,-1)]
    for s in range(i,-1,-1):
        p[s] = segment_penalty(auxiliary_vector,timestamps_edges,s,i)
    P[i][0] = p[0]
    R[i][0] = 0
    #if i%1000 == 0:
      #now = datetime.now()
      #current_time = now.strftime("%H:%M:%S")
      #print("Current Time =", current_time, "for ", i, " snapshots")
    for j in range(1,min(i+1,k)): #populating the penalty matrix P and the reconstruction matrix R
      if i == 0:
        min_value = P[0][j-1]
      else:
        min_value = P[0][j-1]+p[1]
      min_index = 0
      for s in range(1,i):
        min_s_value = P[s][j-1]+p[s+1]
        if min_s_value < min_value:
          min_value = min_s_value
          min_index = s
      P[i][j] = min_value
      R[i][j] = min_index
  return P,R

def reconstruct_graph(reconstruct, times):
  Rec_all = [] #reconstructing the solution
  for t in range(len(times)-1,-1,-1):
    Recon_t = []
    ub = t
    for j in range(k-1,-1,-1):
      lb = reconstruct[ub][j]
      if lb > 0:
        Tj = (lb+1,ub)
      else:
        Tj = (lb,ub)
      Recon_t.append(Tj)
      ub = lb
    Rec_all.append(Recon_t)
  return Rec_all

def generate_compressed_graph(temporal_dictionary, Rec_all, edge_dictionary):

  snap_segment = list(temporal_dictionary.values()) #gets the list of each snapshot
  compressed_graph = []
  for segments in reversed(Rec_all[0]):
    segments = list(segments) #gets the segments of optimal segmentation, as reported in Rec_all
    #we now calculate the hamming consensus vector for each segment
    hamming = []
    if len(snap_segment[segments[0]:segments[1]+1]) == 1: #if there is only one snapshot the compressed graph takes exactly this snapshot
      for i in (snap_segment[segments[0]:segments[1]+1]):
        for j in i:
          hamming.append((j))
    else:
      hamming_vectors = []
      for segment in snap_segment[segments[0]:segments[1]+1]:
        hamming_distance = [] #for each value in segment append 1 if the edge is in the segment, 0 otherwise
        for edge in edge_dictionary:
          if list(edge) in segment:
            hamming_distance.append(1)
          else:
            hamming_distance.append(0)
        hamming_vectors.append(hamming_distance)
      transpose_hamming = np.transpose(hamming_vectors)
      hamming_single_vector = [] #hamming consensus centroid
      for row in transpose_hamming:
        count1 = np.count_nonzero(row == 1)
        count0 = np.count_nonzero(row == 0)
        if count1 < count0:
          hamming_single_vector.append(0)
        else:
          hamming_single_vector.append(1)
      hamming_value = [] #it takes the edge corresponding to the edge that has the same index of 1 value in hamming single vector (the hamming consensus centroid)
      for edge in range(0,len(hamming_single_vector)-1):
        if hamming_single_vector[edge] == 1:
          hamming_value.append(list(edge_dictionary[edge]))
      for i in hamming_value:
        hamming.append(i)
    compressed_graph.append(hamming)
  return compressed_graph

if __name__ == '__main__':
  start = datetime.now()   
  nodes,node2id,timestamps,timestamp2id,edges,edge2id,timestamp2edges,snapshots,temporal_dict, new_temporal_dict = load_graph("C:/Users/Utente/Desktop/Temporal-SIR-GN-main/Experiments_with_datasets/temp_brazilAir.txt", True,',')
  a_aux = compute_a_auxiliary_structure(len(edges),len(timestamps),timestamp2edges)
  k = 2
  penalty,reconstruct = tgagg(timestamp2edges,timestamp2id,a_aux, k)
  #new_graph = reconstruct_graph(reconstruct, timestamps)
  #generated_graph = generate_compressed_graph(new_temporal_dict,new_graph,edges)
  print("Timestamps: ", len(timestamps), "Nodes: ",len(nodes)," Edges: ",len(edges))
  print("penalty", penalty[-1])
  #print("penalty", new_graph)
  end = datetime.now()
  print ("Time: ", (end-start))
  #dict_to_csv(generated_graph,"compressed_brazilAir.csv")
  
 
