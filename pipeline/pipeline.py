from compute_stats import compute_stats_datasets
from cleaner import CleanDF
from file_reader import FileReader, read_files
import os
import json
from utils import get_cleaned_file
from tqdm import tqdm
import numpy as np


if __name__ == '__main__':
    id_list = [49]
    # id_list = None
    file_reader = FileReader()
    root_dir = os.getcwd()
    cleaner = CleanDF()

    mapping_info_name = "../input_conf.json"

    with open(mapping_info_name, "r") as json_file:
        mapping_info = json.load(json_file)

    datasets = {}

    for key, item_list in mapping_info.items():
        for item in item_list:
            if item['__file__'] != "" and item["Forecasting Values"] != [""]:
                item['folder'] = key
                datasets[int(item['id_paper'])] = item

    data_root = root_dir + "/../../time_series_datasets"

    if id_list is None:
        id_list = list(datasets.keys())

    for id in tqdm(id_list):
        dataset = datasets[id]
        file_name = f"{dataset['folder']}/{dataset['__file__']}"
        df_i = file_reader.read_file(f"{data_root}/{file_name}")
        sort = dataset["Sort"]
        df_i = cleaner.clean_one_df(df_i)
        if sort != "":
            df_i = df_i.sort_values(by=[sort, "date"])
            df_i["t"] = np.arange(len(df_i))
        cleaned_file_name = get_cleaned_file(file_name)
        df_i.to_csv(f"{data_root}/{cleaned_file_name}")



