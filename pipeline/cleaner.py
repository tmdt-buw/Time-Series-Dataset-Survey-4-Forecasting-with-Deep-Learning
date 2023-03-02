import pandas as pd
import swifter
from datetime import datetime
import re
import numpy as np


class CleanDF:

    @staticmethod
    def check_if_float_str(floatnum):
        regex = '[+-]?[0-9]+\.[0-9]+'
        return re.fullmatch(regex, floatnum)

    @staticmethod
    def check_correct_time_format(x):
        try:
            datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

    @staticmethod
    def drop_unamed_columns(df):
        for column in df.columns:
            if column.split(" ")[0] == "unnamed:":
                df = df.drop(columns=[column])
            elif column == "(inverter)":
                df = df.drop(columns=[column])
        return df

    @staticmethod
    def try_parsing_date(text):
        for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%m/%d/%Y', "%m/%d/%y", '%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M'):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                pass
        raise ValueError(f'no valid date format found -> {text}')

    @staticmethod
    def try_parsing_datetime(text):
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H', '%m/%d/%y %H:%M', '%d/%m/%y %H:%M'):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                pass
        raise ValueError(f'no valid date format found -> {text}')

    @staticmethod
    def create_date_from_columns(df, columns):
        if columns == ["year"]:
            y = np.array(df['year'] - 1970, dtype='<M8[Y]')
            df.loc[:, 'date'] = pd.to_datetime(y)
        elif columns == ["year", "month"]:
            y = np.array(df['year'] - 1970, dtype='<M8[Y]')
            m = np.array(df['month'] - 1, dtype='<m8[M]')
            df.loc[:, 'date'] = pd.to_datetime(y+m)
        else:
            df.loc[:, 'date'] = pd.to_datetime(df[columns])
        return df

    @staticmethod
    def set_categoricals_to_int(df, key):
        keys = list(df[key].unique())
        df.loc[:, f"{key}_n"] = 0
        for i, cat in enumerate(keys):
            df.loc[cat == df[key], f"{key}_n"] = i
        df = df.drop(columns=key)
        df = df.rename(columns={f"{key}_n": key})
        return df


    def convert_date_time(self, df, col_name):
        df.loc[:, col_name] = df[col_name].swifter.apply(lambda x: str(self.try_parsing_datetime(str(x))))
        if not df[col_name].dtype == '<M8[ns]':
            df.loc[:, col_name] = pd.to_datetime(df[col_name])
        df = df.rename(columns={col_name: 'date'})
        return df

    def convert_and_remove_date(self, df):
        date_names = ['year', 'month', 'day', 'hour', 'minutes']
        str_date_columns = [name for name in date_names if name in df.columns]
        if "date" in df.columns and "time" in df.columns:
            df.loc[:, 'date'] = df.loc[:, 'date'].swifter.apply(lambda x: str(self.try_parsing_date(str(x)).date()))
            df.loc[:, 'time'] = df.loc[:, 'time'].swifter.apply(lambda x: str(x).replace(".", ":"))
            df.loc[:, 'date'] = pd.to_datetime(df['date'] + ' ' + df['time'])
            df = df.drop(columns=['time'])
        elif "date" in df.columns:
            # check if date date or datetime
            if len(str_date_columns) > 0 and str_date_columns[0] == 'hour':
                df.loc[:, 'date'] = df['date'] + ' ' + (df['hour'] - 1).astype(str) + ':00:00'
                df.loc[:, 'date'] = df['date'].swifter.apply(lambda x: str(self.try_parsing_datetime(str(x))))
            else:
                df.loc[:, 'date'] = df['date'].swifter.apply(lambda x: str(self.try_parsing_date(str(x)).date()))
            if not df['date'].dtype == '<M8[ns]':
                df.loc[:, 'date'] = pd.to_datetime(df['date'])
        elif "time" in df.columns:
            df = self.convert_date_time(df, "time")
        elif "localtime" in df.columns:
            df = self.convert_date_time(df, "localtime")
        elif "datetime" in df.columns:
            df = self.convert_date_time(df, "datetime")
        elif "timestamp" in df.columns:
            df = self.convert_date_time(df, "timestamp")
        else:
            df = self.create_date_from_columns(df, str_date_columns)
            df = df.drop(str_date_columns, axis=1)
        return df

    @staticmethod
    def set_id(df, id_column_name="No"):
        df = df.rename(columns={id_column_name: 'id'})
        return df

    def remove_and_convert_types(self, df):
        types = dict(df.dtypes)
        for key, val in types.items():
            if val == "str":
                df[key] = df[key].astype("category")
                print(df.head())
                df = self.set_categoricals_to_int(df, key)
                print(df.head())
            elif val == "object":
                first_value = df[key].iloc[0]
                if type(first_value) == str and self.check_if_float_str(first_value):
                    df = df.astype({key: 'float64'})
                elif type(first_value) == str:
                    # print(f"Remove value: {first_value}")
                    df[key] = df[key].astype("category")
                    print(df.head())
                    df = self.set_categoricals_to_int(df, key)
                    print(df.head())
                else:
                    df = df.astype({key: 'float64'})
        return df

    def clean_one_df(self, df):
        print("--- start cleaning ---")
        df.columns = df.columns.str.strip().str.lower()
        df = self.drop_unamed_columns(df)
        df = df.dropna()
        df = df.reset_index(drop=True)
        df = self.convert_and_remove_date(df)
        df = self.remove_and_convert_types(df)
        df['id'] = 1
        return df.dropna()