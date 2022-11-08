# Underlying modules for preprocessing of the data

## preprocessing.py

contains the class for preprocessing with two functions `fit` and `transform`.

## `fit(data)`

During fitting the preprocessor  

1. learns the value to replace missing `'avg_price', 'last_price', 'num_price_chg'`. Particularly, the missing values 
will be replaced by their corresponding average grouped by `'country'` and `'project_type'`. (**-123456789 in the data represents the missing values**)
2. learns onehotencoding of `'project_type'`. This is based on the assumption that `'project_categories'` DO NOT have shared `'project_type'`.
3. keeps only the columns used in clustering. The current setting uses `'country_latitude', 'country_longitude', 'nft_age', 'num_owners',
'avg_price', 'last_price', 'num_price_chg'` in addition to the onehotencoded `'project_type'`.
4. learns scaling the columns to `mean=0` and `std=1`

## `transform(data)`

Based on the data shown to the preprocessor in the `fit`, the preprocesser transforms the data to the proper format to be passed to the clustering model.

