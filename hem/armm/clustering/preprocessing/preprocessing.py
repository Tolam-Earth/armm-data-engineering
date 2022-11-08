import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler

MISSING_VALUE = -123456789


class Preprocessor:
    def __init__(self):
        self.mean_based_on_categorical = None
        self.OneHotEncoder = OneHotEncoder(
            handle_unknown='ignore', sparse=False)
        self.StandardScaler = StandardScaler()
        self.columns_with_missing_allowed = ['avg_price',
                                             'last_price',
                                             'num_price_chg',
                                             ]
        self.attributes_pool = None
        self.attributes_for_clustering = [
            'latitude',
            'longitude',
            'nft_age',
            'num_owners',
            'avg_price',
            'last_price',
            'num_price_chg',
        ]
        self.categories_for_clustering = ['project_type']
        self.columns_group_by = ['country',
                                 'project_type',
                                 ]

    def _fill_missing_with_groupby_mean(self, table: pd.DataFrame, table_groupby_mean: pd.DataFrame) -> pd.DataFrame:
        if MISSING_VALUE in table[self.columns_with_missing_allowed].values or table[self.columns_with_missing_allowed].isnull(
        ).values.any():
            table_with_na = table.mask(table == MISSING_VALUE, np.nan)
            temp = table_with_na[self.columns_group_by].merge(table_groupby_mean, on=self.columns_group_by, how='left')
            table[self.columns_with_missing_allowed] = table_with_na[self.columns_with_missing_allowed].fillna(
                temp[self.columns_with_missing_allowed])
        return table

    def fit(self, data_raw: pd.DataFrame, y=None, **keywords):
        data = data_raw.reset_index(drop=True, inplace=False)
        # calculating mean of the column based on the country and project type to be used for filling missing
        data[self.columns_with_missing_allowed] = data[self.columns_with_missing_allowed].mask(data == MISSING_VALUE,
                                                                                               np.nan)
        self.mean_based_on_categorical = data.groupby(by=self.columns_group_by, as_index=False
                                                      )[self.columns_with_missing_allowed].mean()
        data = self._fill_missing_with_groupby_mean(table=data, table_groupby_mean=self.mean_based_on_categorical)
        # onehot encoding the categorical variable
        temp = self.OneHotEncoder.fit_transform(data[self.categories_for_clustering])
        temp = pd.DataFrame(
            temp, columns=self.OneHotEncoder.get_feature_names_out())
        data = data[self.attributes_for_clustering]
        data = pd.concat([data, temp], ignore_index=False, axis=1)
        self.attributes_pool = data.columns.values.tolist()
        self.StandardScaler.fit(data)
        return self

    def transform(self, data_raw: pd.DataFrame, y=None, **keywords):
        data = data_raw.reset_index(drop=True, inplace=False)
        data = self._fill_missing_with_groupby_mean(table=data, table_groupby_mean=self.mean_based_on_categorical)

        temp = self.OneHotEncoder.transform(data[self.categories_for_clustering])
        temp = pd.DataFrame(
            temp, columns=self.OneHotEncoder.get_feature_names_out())
        data = data[self.attributes_for_clustering]
        data = pd.concat([data, temp], ignore_index=False, axis=1)
        data = pd.DataFrame(self.StandardScaler.transform(data), columns=self.attributes_pool)
        return data
