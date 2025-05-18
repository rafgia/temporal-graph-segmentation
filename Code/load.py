from collections import defaultdict
from datetime import datetime

def load_graph(file,header,sep):
  with open(file) as f:
    start = 1 if header else 0
    nodes = set()
    timestamps = set()
    temporal_edges = list()
    for line in f.readlines()[start:]:
      tokens = line.split(sep)
      node1 = min(int(tokens[0]),int(tokens[1]))
      node2 = max(int(tokens[0]),int(tokens[1]))
      timestamp = float(tokens[2])
      nodes.add(node1)
      nodes.add(node2)
      timestamps.add(timestamp)
      temporal_edges.append((node1,node2,timestamp))

    #array mapping nodeIDs (array indices) to actual nodes (array values)
    nodes = sorted(list(nodes))
    #dictionary mapping actual nodes to nodeIDs
    node2id = {}
    for i in range(len(nodes)):
      node2id[nodes[i]] = i

    #array mapping timestampIDs (array indices) to actual timestamps (array values)
    timestamps = sorted(list(timestamps))
    #dictionary mapping actual timestamps to timestampIDs
    timestamp2id = {}
    for i in range(len(timestamps)):
      timestamp2id[timestamps[i]] = i

    #all (unique) non-temporal edges in the graph
    #'edges' is an #array mapping edgeIDs (array indices) to actual edges (array values)
    edges = set()
    for e in temporal_edges:
      nontemporal_e = (node2id[e[0]],node2id[e[1]])
      edges.add(nontemporal_e)
    edges = sorted(list(edges))

    #dictionary mapping actual (non-temporal) edges to edgeIDs
    edge2id = {}
    for i in range(len(edges)):
      edge2id[edges[i]] = i

    #set of edges in every timestamp
    #for both timestamps and edges their corresponding IDs are considered here
    timestamp2edges = {} 
    for e in temporal_edges:
      edge = (node2id[e[0]],node2id[e[1]])
      timestampID = timestamp2id[e[2]]
      if timestampID not in timestamp2edges: 
        timestamp2edges[timestampID] = set()
      timestamp2edges[timestampID].add(edge2id[edge])

    #array of all temporal snapshots of the temporal graph
    #every cell of the array is a snapshot
    #every snapshot is a dictionary whose keys are nodes and values are the neighbors of that node in that snapshot
    #for both timestamps and nodes their corresponding IDs are considered here
    #information is duplicated: for any (u,v) edge both v is stored as a neighbor of u and u is stored as a neighbor of v
    snapshots = [None]*len(timestamps)
    for e in temporal_edges:
      nodeID1 = node2id[e[0]]
      nodeID2 = node2id[e[1]]
      timestampID = timestamp2id[e[2]]
      if not snapshots[timestampID]:
        snapshots[timestampID] = defaultdict(set)
      snapshots[timestampID][nodeID1].add(nodeID2)
      snapshots[timestampID][nodeID2].add(nodeID1)

    temporal_dict = {}
    for e in temporal_edges:
      if e[2] not in temporal_dict:
        temporal_dict[e[2]] = []
      temporal_dict[e[2]].append((e[0],e[1]))
    
    new_temporal_dict = {} #to rescale the timestamps
    new_id = 0
    for i in temporal_dict:
      new_temporal_dict[new_id] = temporal_dict[i]
      new_id += 1


    return nodes,node2id,timestamps,timestamp2id,edges,edge2id,timestamp2edges,snapshots, temporal_dict, new_temporal_dict