from tsfresh import extract_features
from file_reader import FileReader
from pipeline.utils import get_cleaned_file

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


def compute_stats_one_ds(id: int, file_name: str, forecast_values: str, out_dir: str, sort: bool):
    filename = get_cleaned_file(file_name)
    feature_extractor = FeatureExtractorTask(id=id, data_key=forecast_values, out_dir=out_dir)
    feature_extractor.run(filename, sort=sort)
