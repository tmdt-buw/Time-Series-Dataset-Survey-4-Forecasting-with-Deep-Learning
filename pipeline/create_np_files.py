import os
import numpy as np
import json
from file_reader import FileReader
from utils import get_cleaned_file


def convert_to_np_file(id_list=None):
    file_reader = FileReader()
    root_dir = os.getcwd()

    mapping_info_name = "../input_conf.json"

    with open(mapping_info_name, "r") as json_file:
        mapping_info = json.load(json_file)

    datasets = {}

    for key, item_list in mapping_info.items():
        for item in item_list:
            item['folder'] = key
            datasets[int(item['id_paper'])] = item


    data_root = root_dir + "/../../time_series_datasets"

    if id_list is None:
        id_list = list(datasets.keys())

    for id in id_list:
        dataset = datasets[id]
        file_name = f"{dataset['folder']}/{dataset['__file__']}"
        file_name = get_cleaned_file(file_name)
        df_i = file_reader.read_file(f"{data_root}/{file_name}")
        forecast_value = dataset['Forecasting Values'][0]
        np_arr = df_i[forecast_value].values
        np.save(f"../np_files/arr_{id}", np_arr)



def main():
    # df_c1 = read_cluster([2,3,4,5,10,11,12,13,17,18,19,20,21,25,26,27,31,33], cleaned_version=True)
    id_list = [49]
    convert_to_np_file(id_list)

if __name__ == '__main__':
    main()
