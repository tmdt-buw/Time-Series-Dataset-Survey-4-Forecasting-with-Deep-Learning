from typing import Dict, List
from matrixprofile.algorithms import mpdist
from matrixprofile.algorithms import maximum_subsequence
import numpy as np
import os
from multiprocessing import Process, Manager


def split_list(i, ds, num_threads):
    interval = int(len(ds) / num_threads)
    return ds[interval * i:interval*(1+i)]


def compute_max_window(i, x, ret_dict):
    mp_window = maximum_subsequence(x)
    ret_dict[i] = mp_window
    print(f"done {i}")
    return mp_window

def multi_thread_compute(setups):
    manager = Manager()
    setup_dict = manager.dict()
    processes = []
    for thread_index, setup in enumerate(setups):
        args = (thread_index, setup, setup_dict)
        p = Process(target=compute_max_window, args=args)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    return dict(setup_dict)

def single_thread_compute(setups):
    manager = Manager()
    setup_dict = manager.dict()
    for thread_index, setup in enumerate(setups):
        compute_max_window(thread_index, setup, setup_dict)

    return dict(setup_dict)

def compute_mpdist_window(file_name: str, data: np.array):
    mp_window = maximum_subsequence(data)
    print(f"{file_name} mpdist window: {mp_window}")
    np.save(f"{file_name}_mp.npy", mp_window)
    return mp_window

def compute_mpdist(window_len_dict: Dict[str, int], data: List[np.array], dist_file_name="dists.npy"):
    if os.path.isfile(dist_file_name):
        dists = np.load(dist_file_name)
        assert dists.shape == (len(data), len(data)), "loaded data has wrong shape"
    else:
        dists = np.zeros([len(data), len(data)])

    for i, x_i in enumerate(data):
        for j, x_j in enumerate(data):
            print(x_i.shape, x_j.shape, window_len_dict[i])
            window_len = window_len_dict[i]
            if len(x_j) < window_len:
                window_len = len(x_j) - 1
                print("new window", window_len, len(x_i), len(x_j))
            if len(x_i) < window_len:
                window_len = len(x_i) - 1
                print("new window", window_len, len(x_i), len(x_j))
            if dists[i][j] == 0.0 and i >= 18:
                result_x_ij = mpdist(x_i, x_j, w=window_len, n_jobs=8)
                print(f"dist {result_x_ij}")
                dists[i][j] = result_x_ij
                np.save("np_dists_new", dists)
                print(f"{i} - {j} done")
            else:
                print(f"skiped: {i} - {j}")

