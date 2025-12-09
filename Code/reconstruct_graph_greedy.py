import numpy as np

def generate_compressed_graph_greedy(temporal_dictionary, Rec_all, edge_dictionary):

  #gets the list of each snapshot
  snap_segment = list(temporal_dictionary.values()) 
  compressed_graph = []
  for segments in Rec_all:
    segments = list(segments) 
    #we now calculate the hamming consensus vector for each segment
    hamming = []
    #if there is only one snapshot the compressed graph takes exactly this snapshot
    if len(snap_segment[segments[0]:segments[1]+1]) == 1: 
      for i in (snap_segment[segments[0]:segments[1]+1]):
        for j in i:
          hamming.append((j))
    else:
      hamming_vectors = []
      for segment in snap_segment[segments[0]:segments[1]+1]:
        #for each value in segment append 1 if the edge is in the segment, 0 otherwise
        hamming_distance = [] 
        for edge in edge_dictionary:
          if list(edge) in segment:
            hamming_distance.append(1)
          else:
            hamming_distance.append(0)
        hamming_vectors.append(hamming_distance)
      transpose_hamming = np.transpose(hamming_vectors)
      #hamming consensus centroid
      hamming_single_vector = [] 
      for row in transpose_hamming:
        count1 = np.count_nonzero(row == 1)
        count0 = np.count_nonzero(row == 0)
        if count1 < count0:
          hamming_single_vector.append(0)
        else:
          hamming_single_vector.append(1)
      #it takes the edge corresponding to the edge that has the same index of 1 value in hamming single vector (the hamming consensus centroid)
      hamming_value = [] 
      for edge in range(0,len(hamming_single_vector)-1):
        if hamming_single_vector[edge] == 1:
          hamming_value.append(list(edge_dictionary[edge]))
      for i in hamming_value:
        hamming.append(i)
    compressed_graph.append(hamming)
  return compressed_graph
