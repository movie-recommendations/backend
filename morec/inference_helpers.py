import re
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class StringToList(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.input_features_ = X.columns
        return self

    def transform(self, X, y=None):
        return X.map(self.string_to_list)

    def string_to_list(self, x):
        if pd.isna(x):
            return x
        else:
            return [int(n) for n in re.split(',\s*|\s+', x)]

    def get_feature_names(self, input_features=None):
        return self.input_features_


class AddOne(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X + 1