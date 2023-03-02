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

def load_data(folder="np_files"):
    array_dict = {}
    files = os.listdir(folder)

    for i, file in enumerate(files):
        paper_id = file.split(".")[-2]
        array_dict[(i, paper_id)] = np.load(f"{folder}/{file}")
    return array_dict


def compute_window_len(index, folder="np_files"):
    file = f"arr_{index}.npy"
    array = [np.load(f"{folder}/{file}")]
    print(array[0].shape)
    return single_thread_compute(array)

def main():
    data = load_data("../np_files")
    new_data = []
    for i, x_i in data.items():
        if len(x_i.shape) > 1:
            x_i = x_i.reshape(-1)
        new_data.append(x_i[:1_000_000])

    window_len_dict = {2: 192, 3: 2356, 4: 9830, 5: 1740, 10: 346, 11: 3788, 12: 794, 13: 308, 17: 36044, 18: 236,
                       19: 320, 20: 2150, 21: 244, 28: 12288, 29: 16, 30: 794, 39: 1690, 41: 6758, 49: 4916, 52: 230}


    dists = np.load("np_dists.npy")
    print(dists.shape)

    keys = data.keys()
    keys = {k:int(i.split("_")[1]) for k,i in keys}
    data = new_data

    for i, x_i in enumerate(data):
        for j, x_j in enumerate(data):
            print(x_i.shape, x_j.shape, window_len_dict[keys[i]])
            window_len = window_len_dict[keys[i]]
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

def compute_mpdist_window(id_list):
    for id in id_list:
        data = np.load(f"../np_files/arr_{id}.npy")
        mp_window = maximum_subsequence(data)
        print(id, mp_window)
        np.save(f"../np_files/arr_{id}_mp", mp_window)


if __name__ == '__main__':
    main()
