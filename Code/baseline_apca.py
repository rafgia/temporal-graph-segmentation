# adaptation of APCA to temporal graphs

from datetime import datetime
from load import load_graph
from penalties import segment_penalty
from auxiliary import compute_a_auxiliary_structure
import matplotlib.pyplot as plt

def extract_edges(snapshot):
    """
    Extract the set of undirected edges from a snapshot adjacency structure.
    """
    edge_set = set()
    for u in snapshot:
        for v in snapshot[u]:
            edge_set.add((min(u, v), max(u, v)))
    return edge_set

def compute_hamming_distances(snapshots):
    """
    Compute Hamming distances between consecutive graph snapshots.
    The Hamming distance is defined as the number of edges that differ between two consecutive snapshots.
    """
    distances = []
    for i in range(1, len(snapshots)):
        edges_prev = extract_edges(snapshots[i - 1])
        edges_curr = extract_edges(snapshots[i])
        hamming_distance = len(edges_prev.symmetric_difference(edges_curr))
        distances.append((i, hamming_distance))
    return distances

def estimate_threshold(snapshots, alpha=1.5):
    """
    Estimate an adaptive threshold for detecting segment boundaries in temporal graph snapshots.
    The threshold is computed as:
        mean(Hamming distances) + alpha * std(Hamming distances)
    """
    distances = compute_hamming_distances(snapshots)
    values = [d for _, d in distances]
    mean_val = sum(values) / len(values)
    std_val = (sum((x - mean_val) ** 2 for x in values) / len(values)) ** 0.5
    return mean_val + alpha * std_val

def segment_snapshots_adaptive(snapshots, threshold):
    """
    Segment temporal snapshots into groups based on an adaptive threshold.
    A new segment is created whenever the Hamming distance between two consecutive snapshots exceeds the given threshold.
    """
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
    