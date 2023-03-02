import argparse
import json
import os
import numpy as np
from pipeline.compute_stats import compute_stats_one_ds
from file_reader import FileReader
from pipeline.cleaner import CleanDF
from pipeline.mp_dist import compute_mpdist_window, compute_mpdist
from pipeline.utils import get_cleaned_file

def main():
    parser = argparse.ArgumentParser(description='Compute Stat. Measurements for Time Series')
    parser.add_argument('--config-file', type=str, help='File path to config files, which defines the complete dataset',
                        required=True)
    parser.add_argument('--compute-mpdist', type=bool, default=True,
                        help='triggers the computation of mpdist between the defined datasets')
    parser.add_argument('--create-cleaned-version', type=bool, default=False,
                        help='cleans the dataset and writes an new file')
    parser.add_argument('--compute-stats', type=bool, default=False, help='triggers the computation ADF, AC, and PRV')

    args = parser.parse_args()
    config_file = args.config_file

    with open(config_file, "r") as json_file:
        mapping_info = json.load(json_file)
    print(mapping_info)

    root_dir = os.getcwd()

    if args.create_cleaned_version:
        file_reader = FileReader()
        cleaner = CleanDF()
        for i, (key, ds_item) in enumerate(mapping_info.items()):
            file_name = f"{root_dir}/data/{key}/{ds_item['__file__']}"
            forecast_value = ds_item['Forecasting Values'][0]
            df_i = file_reader.read_file(file_name)
            sort = ds_item["sort"]
            df_i = cleaner.clean_one_df(df_i)
            if sort != "":
                df_i = df_i.sort_values(by=[sort, "date"])
                df_i["t"] = np.arange(len(df_i))
            cleaned_file_name = get_cleaned_file(file_name)
            df_i.to_csv(cleaned_file_name)
            np_arr = df_i[forecast_value].values
            np_filename = "/".join(file_name.split("/")[:-1])
            np.save(f"{np_filename}/np_array", np_arr)

    if args.compute_stats:
        for i, (key, ds_item) in enumerate(mapping_info.items()):
            compute_stats_one_ds(id=i, file_name=f"{root_dir}/data/{key}/{ds_item['__file__']}",
                                 forecast_values=ds_item["Forecasting Values"][0], out_dir="data/",
                                 sort=ds_item["sort"] != "")

    if args.compute_mpdist:
        data_list = []
        mp_window_dict = {}
        for i, (key, ds_item) in enumerate(mapping_info.items()):
            file_name = f"{root_dir}/data/{key}/{ds_item['__file__']}"
            np_filename = "/".join(file_name.split("/")[:-1])
            data = np.load(f"{np_filename}/np_array.npy")
            mp_window = compute_mpdist_window(np_filename, data, True)
            mp_window_dict[i] = mp_window
            # only use a max window of 1M because of performance problems.
            data_list.append(data[:1_000_000])
        compute_mpdist(mp_window_dict, data_list)



if __name__ == '__main__':
    main()
