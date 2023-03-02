import pandas as pd
import os
import json
from tsfresh import extract_features
from file_reader import FileReader
from utils import get_cleaned_file

TS_FRESH_SETTINGS = {
    "agg_autocorrelation": [
        {
            "f_agg": "mean",
            "maxlag": 40
        },
        {
            "f_agg": "median",
            "maxlag": 40
        },
        {
            "f_agg": "var",
            "maxlag": 40
        }
    ],
    "augmented_dickey_fuller": [
        {
            "attr": "teststat"
        },
        {
            "attr": "pvalue"
        },
        {
            "attr": "usedlag"
        }
    ],
    "percentage_of_reoccurring_values_to_all_values": None,
    "standard_deviation": None,
}

class FeatureExtractorTask:

    def __init__(self, id, data_key, out_dir, categoricals=None) -> None:
        super().__init__()
        self.id = id
        self.out_dir = out_dir + str(id)
        self.data_key = data_key
        self.categoricals = categoricals if categoricals != "" else None
        self.file_reader = FileReader()

    def run(self,filename, sort=False):
        """Define, what the task will actually do"""
        # 1. Read in the time series data from disk
        df = self.file_reader.read_file(filename)
        df = df.iloc[:1_000_000]
        df['id'] = 1
        print("--- start extract Feature ---")
        # 2. Extract the features.
        # Turn of multiprocessing - the parallelism comes with multiple luigi workers.

        sort = "t" if sort else "date"

        features = extract_features(
            timeseries_container=df,
            column_id='id',
            column_sort=sort,
            column_kind=self.categoricals,
            column_value=str(self.data_key),
            default_fc_parameters=TS_FRESH_SETTINGS
        )
        print(features)
        # 3. Store the data
        features.to_csv(self.out_dir)


def compute_stats_datasets(id_list):
    root_dir = os.getcwd()
    out_dir = root_dir + "/../tmp/"

    data_root = root_dir + "/../../time_series_datasets"

    mapping_info_name = "../input_conf.json"
    with open(mapping_info_name, "r") as json_file:
        mapping_info = json.load(json_file)

    datasets = {}
    for key, item_list in mapping_info.items():
        for item in item_list:
            item['folder'] = key
            datasets[int(item['id_paper'])] = item

    for id, dataset in datasets.items():
        if id in id_list or id_list is None:
            filename = f"{dataset['folder']}/{dataset['__file__']}"
            filename = get_cleaned_file(filename)
            filename = f"{data_root}/{filename}"
            if filename != "":
                forecast_values = dataset['Forecasting Values'][0]
                feature_extractor = FeatureExtractorTask(id=id, data_key=forecast_values, out_dir=out_dir)
                feature_extractor.run(filename, sort=dataset["Sort"] != "")


if __name__ == "__main__":
    compute_stats_datasets([49])
