import os
from os import listdir
import pandas as pd
import numpy as np
from scipy.io import loadmat
import pickle
import gzip
from dataclasses import dataclass
from typing import Union
from multiprocessing import Process, Manager
import json


@dataclass
class FileNameMapping:
    split: str
    index_mapping: list
    delimiter: Union[str, None] = None


@dataclass
class SingleMapping:
    is_from_to: bool
    index_1: int
    index_2: Union[int, None]
    name: str
    join_type: Union[str, None] = None


class MultipleFileReader:

    def __init__(self) -> None:
        super().__init__()
        self.file_reader = FileReader()

    def get_files_of_dir(self, path: str):
        files = listdir(path)
        file_names = []
        for file in files:
            file_name = f"{path}\\{file}"
            if os.path.isdir(file_name):
                [file_names.append(item) for item in self.get_files_of_dir(file_name)]
            else:
                file_names.append(file_name)
        return file_names

    @staticmethod
    def split_setups(i, ds, num_threads):
        interval = int(len(ds) / num_threads)
        return ds[interval * i:interval * (1 + i)]

    def multi_thread_compute(self, files, mapping, num_threads=10):
        manager = Manager()
        setup_list = manager.list()

        processes = []
        for thread_index in range(num_threads):
            sample_list = self.split_setups(thread_index, files, num_threads)
            args = (sample_list, mapping, setup_list)
            p = Process(target=self.read_file_from_list, args=args)
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
        return list(setup_list)

    def read_file_from_list(self, files: list, mapping: FileNameMapping, df_list):
        len_files = len(files)
        for i, file in enumerate(files):
            self.read_one_file(file, mapping, df_list)
            if i % int(len_files*0.1) == 0:
                print(f"[{i}/{len_files}]")

    def read_one_file(self, file: str, mapping: FileNameMapping, df_list):
        _, file_name = os.path.split(file)
        categoricals = self.file_reader.get_categorical_var_from_name(".".join(file_name.split(".")[:-1]), mapping)
        t_df = self.file_reader.read_file(file, delimiter=mapping.delimiter)
        for k, val in categoricals.items():
            t_df[k] = val
        df_list.append(t_df)

    def read_files_from_dir(self, path: str, mapping: FileNameMapping, multi_processing=False):
        files = self.get_files_of_dir(path)
        if len(files) > 100:
            indices = np.random.choice(len(files), 100, replace=False)
            files = np.array(files)
            files = files[indices]
        if multi_processing:
            df_list = self.multi_thread_compute(files, mapping, num_threads=20)
        else:
            df_list = []
            self.read_file_from_list(files, mapping, df_list)
        print("Concat")
        df = pd.concat(df_list, axis=0)
        return df


class FileReader:

    def get_files_of_dir(self, path: str, files: list):
        file_names = []
        for file in files:
            file_name = f"{path}\\{file}"
            # print(file_name)
            if os.path.isdir(file):
                file_names.append(self.get_files_of_dir(file_name, listdir(file_name)))
            else:
                file_names.append(file_name)
        return file_names

    @staticmethod
    def check_delimiter(line1, line2):
        delimiter = ","
        if len(line1.split(";")) > 2 and len(line1.split(";")) == len(line2.split(";")):
            delimiter = ";"
        elif len(line1.split(",")) > 2 and len(line1.split(",")) == len(line2.split(",")):
            delimiter = ","
        elif len(line1.split(" ")) > 2 and len(line1.split(" ")) == len(line2.split(" ")):
            delimiter = " "
        return delimiter

    def read_csv(self, file: str, delimiter: Union[str, None] = None):
        if delimiter is None:
            with open(file, "r", encoding="utf8") as t_file:
                first_line, second_line = "", ""
                for i, line in enumerate(t_file):
                    if i == 0:
                        first_line = line
                    elif i == 1:
                        second_line = line
                    else:
                        break
            delimiter = self.check_delimiter(first_line, second_line)
        return pd.read_csv(file, delimiter=delimiter, low_memory=False)

    @staticmethod
    def read_excel_file(file):
        return pd.read_excel(file)

    @staticmethod
    def read_mat_file(file):
        mat = loadmat(file)
        keys = mat.keys()
        keys = [key for key in keys if key[:2] != "__"]
        ds_mat = [mat[key] for key in keys]
        print(keys)
        for item in ds_mat:
            print(item.shape)
        return pd.DataFrame(np.hstack(ds_mat))

    @staticmethod
    def read_ziped_pickle_file(file):
        with gzip.open(file, 'rb') as f:
            return pickle.load(f)

    def read_file(self, path: str, file_name: Union[str, None] = None, delimiter: Union[str, None] = None):
        file = path
        if file_name is not None:
            file += f"\\{file_name}"
        file_ending_split = file.split(".")
        # assert len(file_ending_split) == 2, f"Another point in path {file}"
        file_ending = file_ending_split[-1]
        # print(f"Path: {path} File ending:{file_ending}")
        ds = pd.DataFrame()
        if file_ending == "csv":
            ds = self.read_csv(file, delimiter=delimiter)
        elif file_ending == "xlsx":
            ds = self.read_excel_file(file)
        elif file_ending == "mat":
            ds = self.read_mat_file(file)
        elif file_ending == "pgz":
            ds = self.read_ziped_pickle_file(file)
        # elif file_ending in ["txt", "text"]:
        #     ds.append(read_csv(file))
        else:
            print(f"Not supported {file_ending=} -- {file}")
        return ds
    
    @staticmethod
    def get_categorical_var_from_name(name: str, file_mapping: FileNameMapping) -> dict:
        split_name = name.split(file_mapping.split)
        categorical_dict = {}
        for index_mapping in file_mapping.index_mapping:
            if index_mapping.is_from_to:
                if index_mapping.join_type == "str":
                    categorical_dict[index_mapping.name] = file_mapping.split.join(split_name[index_mapping.index_1:index_mapping.index_2 + 1])
                else:
                    print(f"Error: Not supported join type: {index_mapping.join_type}")

            else:
                categorical_dict[index_mapping.name] = split_name[index_mapping.index_1]
        return categorical_dict


def check_if_already_there(path):
    file = "\\".join(path.split("\\")[-3:-1])
    file_exists = os.path.exists(file + "_0_cleaned.csv")
    return file_exists


def read_files(mapping_info, root_dir: str="", multi_file_mapping: dict=None, multi_processing: bool=True,
               pipeline: bool=False):
    ds_dict = {}
    m_file_reader = MultipleFileReader()
    file_reader = FileReader()
    for i, (folder_key, items) in enumerate(mapping_info.items()):
        if folder_key not in ["id_44"]:
        # if True:
            item_list = []
            for single_item in items:
                path = f"{root_dir}\\{folder_key}\\{single_item['__file__']}"
                if pipeline:
                    if single_item['__file__'] != "" and single_item['Forecasting Values'] != [""] and not check_if_already_there(path):
                        try:
                            if multi_file_mapping is not None and folder_key in multi_file_mapping.keys():
                                item_list.append(m_file_reader.read_files_from_dir(path, multi_file_mapping[folder_key], multi_processing=multi_processing))
                            else:
                                item_list.append(file_reader.read_file(path=path))
                        except FileNotFoundError:
                            print(f"FileNotFoundError: \\{folder_key}\\{single_item['__file__']}")
                else:
                    if single_item['__file__'] != "":
                        try:
                            if multi_file_mapping is not None and folder_key in multi_file_mapping.keys():
                                item_list.append(m_file_reader.read_files_from_dir(path, multi_file_mapping[folder_key],
                                                                                   multi_processing=multi_processing))
                            else:
                                item_list.append(file_reader.read_file(path=path))
                        except FileNotFoundError:
                            print(f"FileNotFoundError: \\{folder_key}\\{single_item['__file__']}")

            ds_dict[folder_key] = item_list
    return ds_dict


if __name__ == '__main__':
    root_dir = os.getcwd()
    data_root = root_dir + "\\..\\time_series_datasets"
    mapping_info_name = "input_conf.json"

    with open(mapping_info_name, "r") as json_file:
        mapping_info = json.load(json_file)

    multi_file_mapping = {
        'id_33': FileNameMapping("_", [
            SingleMapping(False, 1, None, 'latitude', None),
            SingleMapping(False, 2, None, 'longitude', None),
            SingleMapping(False, 3, None, 'year', None),
            SingleMapping(True, 4, 5, 'type', 'str'),
            SingleMapping(True, 6, 7, 'interval', 'str')
        ], delimiter=","),
        'id_34': FileNameMapping("_", [
            SingleMapping(False, 1, None, 'event', None),
        ]),
        'id_37': FileNameMapping("_", [
            SingleMapping(False, 0, None, 'date', None),
        ]),
    }

    ds_dict = read_files(mapping_info, root_dir=data_root, multi_file_mapping=multi_file_mapping,
                         multi_processing=False, pipeline=True)

    print(ds_dict)

