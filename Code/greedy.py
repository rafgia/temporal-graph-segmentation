from load import load_graph
from penalties import _edges_in_time_interval, segment_penalty_given_validedges, segment_penalty
from datetime import datetime
from auxiliary import compute_a_auxiliary_structure


def topdown_greedy_segmentation(a_aux,timestamp2edges,nsegments):
  ntimestamps = len(timestamp2edges)
  first_segment = (0,ntimestamps-1)
  segment2penalty = {first_segment:segment_penalty(a_aux,timestamp2edges,first_segment[0],first_segment[1])}
  segment2bestsplit = {}
  segments_to_be_split = {first_segment}
  current_time = []
  for i in range(2,nsegments+1):

    #computing the best split for the 2 segments generated in the previous iteration
    for current_segment in segments_to_be_split:
      #compute the best split for current_segment
      if (len(current_segment))>1:
        max_gain_cs = float('-inf')
        cst1, cst2 = current_segment[0], current_segment[1]
        current_segment_penalty = segment2penalty[current_segment]

        valid_edges1 = set()
        valid_edges2 = _edges_in_time_interval(timestamp2edges,cst1,cst2)
        for k in range(cst1,cst2):
          #compute valid edge sets for the current split (based on which penalties are computed)
          for edge in timestamp2edges[k]:
            valid_edges1.add(edge)
            #it means that 'edge' is not present in time interval [k+1,cst2]
            if a_aux[k][edge] == a_aux[cst2][edge]: 
              valid_edges2.remove(edge)

          penalty1 = segment_penalty_given_validedges(a_aux,valid_edges1,cst1,k)
          penalty2 = segment_penalty_given_validedges(a_aux,valid_edges2,k+1,cst2)
          current_split_penalty =  penalty1 + penalty2
          current_gain = current_segment_penalty - current_split_penalty
          if current_gain > max_gain_cs:
            max_gain_cs = current_gain
            split = k
            penalty_best_split_1 = penalty1
            penalty_best_split_2 = penalty2

        #storing the best split for current_segment
        segment2bestsplit[current_segment] = (max_gain_cs,split,penalty_best_split_1,penalty_best_split_2)


    #looking for the best split overall
    max_gain_overall = float('-inf')
    best_segment_to_be_split_overall = None
    for segment in segment2bestsplit.keys():
      (max_gain_cs,split,_,_) = segment2bestsplit[segment]
      if max_gain_cs > max_gain_overall:
        max_gain_overall = max_gain_cs
        best_segment_to_be_split_overall = segment

    #performing the best split overall
    (_,best_split,penalty_best_split_1,penalty_best_split_2) = segment2bestsplit[best_segment_to_be_split_overall]
    newsegment1 = (best_segment_to_be_split_overall[0],best_split)
    newsegment2 = (best_split+1,best_segment_to_be_split_overall[1])
    segment2penalty.pop(best_segment_to_be_split_overall)
    segment2penalty[newsegment1] = penalty_best_split_1
    segment2penalty[newsegment2] = penalty_best_split_2
    segment2bestsplit.pop(best_segment_to_be_split_overall)
    segments_to_be_split = {newsegment1,newsegment2}
    #print the time required for the calculation of best split
    now = datetime.now()
    current_time.append(now.strftime("%M:%S.%f"))


  output_segments = sorted(list(segment2penalty.keys()))
  overall_penalty = sum(segment2penalty.values())
  return output_segments, overall_penalty, segment2penalty, current_time


if __name__ == '__main__':
  start = datetime.now()    
  nodes,node2id,timestamps,timestamp2id,edges,edge2id,timestamp2edges,snapshots, temporal_dict, new_temporal_dict = load_graph("graph_path.csv/txt", True,',')
  a_aux = compute_a_auxiliary_structure(len(edges),len(timestamps),timestamp2edges)
  nsegments = 6001
  segments, overall_penalty, segment2penalty, current_time = topdown_greedy_segmentation(a_aux,timestamp2edges,nsegments)
  print("Timestamps: ", len(timestamps), "Nodes: ",len(nodes)," Edges: ",len(edges))
  print("penalty", overall_penalty)
  end = datetime.now()
  print ("Time: ", (end-start))