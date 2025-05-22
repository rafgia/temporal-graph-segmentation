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

def estimate_threshold(snapshots, alpha=1.5):
    distances = compute_hamming_distances(snapshots)
    values = [d for _, d in distances]
    mean_val = sum(values) / len(values)
    std_val = (sum((x - mean_val) ** 2 for x in values) / len(values)) ** 0.5
    return mean_val + alpha * std_val

def segment_snapshots_adaptive(snapshots, threshold):
    segments = []
    current_segment = [0]

    for i in range(1, len(snapshots)):
        edges_prev = extract_edges(snapshots[i - 1])
        edges_curr = extract_edges(snapshots[i])
        hamming_distance = len(edges_prev.symmetric_difference(edges_curr))

        if hamming_distance > threshold:
            segments.append(current_segment)
            current_segment = [i]
        else:
            current_segment.append(i)

    segments.append(current_segment)
    return segments

if __name__ == '__main__':
    start = datetime.now()

    # Load graph
    nodes, node2id, timestamps, timestamp2id, edges, edge2id, timestamp2edges, snapshots, temporal_edges, new_temporal_dict = load_graph(
        "graph_path.csv/txt", 
        True, 
        ','
    )

    # Estimate threshold
    threshold = estimate_threshold(snapshots, alpha=1.5)

    # Segment based on estimated threshold
    segments = segment_snapshots_adaptive(snapshots, threshold)

    # Compute total penalty
    a_aux = compute_a_auxiliary_structure(len(edges), len(timestamps), timestamp2edges)
    sum_penalties = sum(
        segment_penalty(a_aux, timestamp2edges, segment[0], segment[-1]) for segment in segments
    )

    end = datetime.now()

    # Output
    print(f"Estimated threshold: {threshold:.2f}")
    print(f"Number of segments: {len(segments)}")
    print(f"Total penalty: {sum_penalties:.2f}")
    print(f"Execution time: {end - start}")