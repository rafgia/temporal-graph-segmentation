# Temporal graph segmentation

This repository contains the implementation of the algorithm described in the paper:  
**“Segmentation of temporal graphs”**  
available at: https://www.sciencedirect.com/science/article/abs/pii/S0020025525010667

## Citation

If you use this code, please cite:

```
@article{YOUR_CITATION_KEY,
  title={Temporal-Graph Segmentation via Adaptive Penalty and Change Detection},
  author={Giancotti, Raffaele and ...},
  journal={Information Sciences},
  year={2025},
  publisher={Elsevier}
}
```


## Features

- Extracts edges from graph snapshots (undirected).  
- Computes Hamming distances between consecutive snapshots (edge-set differences).  
- Estimates an adaptive threshold based on the mean and standard deviation of Hamming distances.  
- Segments the sequence of snapshots into contiguous intervals whenever the Hamming distance exceeds the threshold.  
- Builds an auxiliary cumulative-edge-presence structure to support segment penalty computation across intervals (via `compute_a_auxiliary_structure`).  

## Repository Structure

```
.
├── code/               # (or root) Python source files
│   ├── main.py         # entry point: loads data, segments snapshots, computes penalty
│   └── ...             # helpers: snapshot manipulation, threshold estimation, segmentation, auxiliary structure
├── tests/              # (optional) tests for correctness of functions  
├── LICENSE             # license file  
└── README.md           # this file  
```

## Usage

1. Prepare your temporal graph data, so you have:  
   - a list of snapshots (e.g. adjacency dictionaries) — each snapshot represents a graph at a given timestamp,  
   - a mapping from timestamps to edges (`timestamp2edges`) if you use the auxiliary-structure approach.  

2. From Python, call the sequence:  
   ```python
   threshold = estimate_threshold(snapshots, alpha=1.5)
   segments = segment_snapshots_adaptive(snapshots, threshold)
   a_aux = compute_a_auxiliary_structure(n_edges, n_timestamps, timestamp2edges)
   total_penalty = sum(segment_penalty(a_aux, timestamp2edges, seg[0], seg[-1]) 
                       for seg in segments)
   ```  

3. (Optional) Adjust the `alpha` parameter in `estimate_threshold` to make segmentation more or less sensitive to changes.  

## Functions Overview

- `extract_edges(snapshot)` — returns the set of undirected edges present in a snapshot.  
- `compute_hamming_distances(snapshots)` — computes Hamming-distance (edge difference) between consecutive snapshots.  
- `estimate_threshold(snapshots, alpha=1.5)` — uses mean + alpha * std of Hamming distances to compute a threshold.  
- `segment_snapshots_adaptive(snapshots, threshold)` — splits the sequence of snapshots into segments when change is large.  
- `compute_a_auxiliary_structure(nedges, ntimestamps, timestamp2edges)` — builds a data structure that tracks cumulative presence of each edge over time.  

## Requirements

- Python 3  
- (Optional) dependencies needed by your `load_graph` function and penalty computation — ensure data is loaded as expected.  
- (Optional) visualization libraries (e.g. matplotlib) if you want to plot or inspect the segmentation.  

## Example

```bash
python main.py path/to/temporal_graph_file.csv
```

This will:
- load the temporal graph,  
- estimate a threshold,  
- segment the snapshot sequence adaptively,  
- compute the total penalty,  
- output: estimated threshold, number of segments, total penalty, execution time.  

## Contributing

Feel free to fork this repo, fix bugs, add tests, or integrate further segmentation strategies.  
If you add new features, please also update this README accordingly.

## License

This project is licensed under the terms specified in the `LICENSE` file.  
