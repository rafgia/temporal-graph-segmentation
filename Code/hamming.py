def hamming(timestamp2edges, timestamp2id, piecewise):
    """
    Compute Hamming consensus vectors for piecewise aggregated snapshots.

    For each piece (list of timestamps):
    - Count how many times each edge appears in the piece.
    - Only include edges that appear more than half of the snapshots in the piece.
    
    Returns a list of lists of edges for each piece.
    """
    hamming_consensus_vectors = []

    for piece in piecewise:
        edges_in_piece = {}  # dict to count edge occurrences
        for snap in piece:
            # Get edges in the snapshot
            edges_list = timestamp2edges[timestamp2id[snap]][0]
            # Convert to tuple to use as dict key
            edges_key = tuple(edges_list)
            # Count occurrence
            if edges_key not in edges_in_piece:
                edges_in_piece[edges_key] = 1
            else:
                edges_in_piece[edges_key] += 1
        # Build consensus vector: only edges appearing more than half of the piece
        hamming_piece = []
        for key, value in edges_in_piece.items():
            if value > len(piece) / 2:
                hamming_piece.append(list(key))
        hamming_consensus_vectors.append(hamming_piece)
    return hamming_consensus_vectors
