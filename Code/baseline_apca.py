# adaptation of APCA to temporal graphs

from datetime import datetime
from load import load_graph
from penalties import segment_penalty
from auxiliary import compute_a_auxiliary_structure
import matplotlib.pyplot as plt



def extract_edges(snapshot):
    edge_set = set()
    for u in snapshot:
        for v in snapshot[u]:
            edge_set.add((min(u, v), max(u, v)))
    return edge_set

def compute_hamming_distances(snapshots):
    distances = []
    for i in range(1, len(snapshots)):
        edges_prev = extract_edges(snapshots[i - 1])
        edges_curr = extract_edges(snapshots[i])
        hamming_distance = len(edges_prev.symmetric_difference(edges_curr))
        distances.append((i, hamming_distance))
    return distances

def segment_snapshots_fixed_k(snapshots, k):
    distances = compute_hamming_distances(snapshots)

    sorted_distances = sorted(distances, key=lambda x: x[1], reverse=True)
    cut_indices = sorted([i for i, _ in sorted_distances[:k - 1]])

    segments = []
    prev_cut = 0
    for cut in cut_indices:
        segments.append(list(range(prev_cut, cut)))
        prev_cut = cut
    segments.append(list(range(prev_cut, len(snapshots)))) 

    threshold = min([d for i, d in sorted_distances[:k - 1]]) + 1

    return segments, threshold

if __name__ == '__main__':
    from datetime import datetime

    start = datetime.now()
    nodes, node2id, timestamps, timestamp2id, edges, edge2id, timestamp2edges, snapshots, temporal_edges, new_temporal_dict = load_graph(
        "C:/Users/Utente/Desktop/Temporal-SIR-GN-main/Experiments_with_datasets/ia-workplace-contacts.csv", True, ',')
    k = 5327
    segments, threshold_used = segment_snapshots_fixed_k(snapshots, k)
    a_aux = compute_a_auxiliary_structure(len(edges),len(timestamps),timestamp2edges)
    from penalties import segment_penalty 
    sum_penalties = 0
    for i in range(0,len(segments)):
        sum_penalties += segment_penalty(a_aux,timestamp2edges, segments[i][0], segments[i][-1])
    end = datetime.now()
    print(f"Threshold selected: {threshold_used}")
    print(f"Time: {end-start}")
    #for i, segment in enumerate(segments):
        #print(f"Segment {i + 1}: Snapshot indices {segment}")
    print(f"Penalties: {sum_penalties}")
