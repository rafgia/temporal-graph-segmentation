import pytest
from Code.edges_in_interval import _edges_in_time_interval
from Code.find_split import find_split, split_piecewise
from Code.hamming import hamming
from Code.penalties import segment_penalty, segment_penalty_given_validedges
from Code.auxiliary import compute_a_auxiliary_structure

def test_edges_in_time_interval():
    timestamp2edges = [
        [0, 1],
        [1, 2],
        [2, 3],
        [0]
    ]
    assert _edges_in_time_interval(timestamp2edges, 1, 2) == {1, 2, 3}
    assert _edges_in_time_interval(timestamp2edges, 0, 3) == {0, 1, 2, 3}

def test_find_split():
    timestamps = list(range(10))
    assert find_split(timestamps, 3) == 4  # 10/3 = 3 + remainder 1 >= 0.5 -> split=4
    assert find_split(timestamps, 5) == 2  # 10/5 = 2, remainder 0 -> split=2

def test_split_piecewise():
    timestamps = list(range(10))
    split = 3
    expected = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [9]
    ]
    assert split_piecewise(timestamps, split) == expected

def test_hamming():
    timestamp2edges = {
        0: [[0,1]],
        1: [[1,2]],
        2: [[0,1]],
        3: [[2,3]]
    }
    timestamp2id = {i:i for i in range(4)}
    piecewise = [[0,1],[2,3]]
    # Each edge occurs only once; half of 4 = 2, so none pass threshold
    assert hamming(timestamp2edges, timestamp2id, piecewise) == [[], []]

def test_segment_penalty_given_validedges():
    a_aux = [
        [1,0,0],
        [2,1,0],
        [3,1,1]
    ]
    valid_edges = [0,1]
    t1, t2 = 1,2
    # interval_size = 2
    # e=0: a2-a1=3-2=1 -> min(1,1)=1
    # e=1: a2-a1=1-1=0 -> min(0,2-0)=0
    assert segment_penalty_given_validedges(a_aux, valid_edges, t1, t2) == 1

def test_segment_penalty():
    timestamp2edges = [
        [0,1],
        [1,2],
        [2,3],
        [0]
    ]
    a_aux = compute_a_auxiliary_structure(4,4,timestamp2edges)
    t1, t2 = 1,2
    expected = segment_penalty_given_validedges(a_aux, _edges_in_time_interval(timestamp2edges, t1, t2), t1, t2)
    assert segment_penalty(a_aux, timestamp2edges, t1, t2) == expected
