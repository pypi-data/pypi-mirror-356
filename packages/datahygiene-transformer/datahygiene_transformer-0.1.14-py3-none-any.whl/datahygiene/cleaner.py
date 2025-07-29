import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import yaml
import json

class DataHygieneTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, numeric_cols=None, cat_cols=None, fillna=True, drop_constant=True,
                 drop_high_cardinality=None, validate_schema=True, verbose=True, encode='onehot'):
        self.numeric_cols = numeric_cols
        self.cat_cols = cat_cols
        self.fillna = fillna
        self.drop_constant = drop_constant
        self.drop_high_cardinality = drop_high_cardinality
        self.validate_schema = validate_schema
        self.verbose = verbose
        self.encode = encode

        self.constant_cols_ = []
        self.high_card_cols_ = []
        self.fill_medians_ = {}
        self.all_categories_ = {}
        self.ordinal_maps_ = {}
        self.fitted_columns_ = []

    def fit(self, X, y=None):
        X = X.copy()

        if self.numeric_cols is None:
            self.numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
        if self.cat_cols is None:
            self.cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

        for col in self.numeric_cols:
            if self.fillna:
                self.fill_medians_[col] = X[col].median()

        for col in self.cat_cols:
            X[col] = X[col].astype("category")
            if self.fillna:
                X[col] = X[col].cat.add_categories('Unknown')
                X[col] = X[col].fillna('Unknown')
            cats = sorted([str(v) for v in X[col].dropna().unique()])
            self.all_categories_[col] = cats
            if self.encode == 'ordinal':
                self.ordinal_maps_[col] = {cat: idx for idx, cat in enumerate(cats)}

        if self.drop_constant:
            self.constant_cols_ = [col for col in X.columns if X[col].nunique(dropna=False) <= 1]

        if self.drop_high_cardinality:
            self.high_card_cols_ = [col for col in self.cat_cols if X[col].nunique() > self.drop_high_cardinality]

        self.fitted_columns_ = X.columns.tolist()
        return self

    def transform(self, X):
        X = X.copy()

        # Add missingness indicators
        for col in self.numeric_cols:
            X[f"{col}_missing"] = X[col].isna().astype(int)

        # Fill numeric columns
        for col in self.numeric_cols:
            if self.fillna:
                X[col] = X[col].fillna(self.fill_medians_.get(col, 0))
            X[col] = X[col].astype(float)

        # Handle categorical columns
        for col in self.cat_cols:
            X[col] = X[col].astype("category")
            if self.fillna:
                if 'Unknown' not in X[col].cat.categories:
                    X[col] = X[col].cat.add_categories('Unknown')
                X[col] = X[col].fillna('Unknown')
            if col in self.all_categories_:
                X[col] = X[col].cat.set_categories(self.all_categories_[col])

        # Drop constant columns
        if self.drop_constant:
            X.drop(columns=self.constant_cols_, inplace=True, errors='ignore')

        # Frequency encode high-cardinality columns
        if self.drop_high_cardinality:
            for col in self.high_card_cols_:
                freq_map = X[col].value_counts().to_dict()
                X[col] = X[col].map(freq_map).fillna(0)

        # Encode categoricals
        if self.encode == 'ordinal':
            for col in self.cat_cols:
                if col in X.columns:
                    mapped = X[col].map(self.ordinal_maps_.get(col, {}))
                    # Convert to object if categorical
                    if pd.api.types.is_categorical_dtype(mapped):
                        # Step 1: convert categorical to integer codes (int dtype, with -1 for NaN)
                        codes = mapped.cat.codes

                        # Step 2: replace -1 (missing) with np.nan so we can fillna safely
                        codes = codes.replace(-1, np.nan)

                        # Step 3: fillna with -1 (or any sentinel you want)
                        codes = codes.fillna(-1).astype(int)

                        # Ensure -1 is a valid category
                        if -1 not in mapped.cat.categories:
                            mapped = mapped.cat.add_categories([-1])

                        mapped = codes  # assign back
                    else:
                        mapped = mapped.fillna(-1)

                    X[col] = mapped

        elif self.encode == 'onehot':
            X = pd.get_dummies(X, columns=self.cat_cols, dummy_na=False)

        # Schema validation
        if self.validate_schema:
            missing_cols = set(self.fitted_columns_) - set(X.columns)
            if missing_cols:
                raise ValueError(f"Missing expected columns: {missing_cols}")

        if self.verbose:
            print(f"[DataHygieneTransformer] Dropped constant columns: {self.constant_cols_}")
            print(f"[DataHygieneTransformer] Frequency-encoded high-cardinality columns: {self.high_card_cols_}")
            print(f"[DataHygieneTransformer] Final columns: {X.columns.tolist()}")

        return X
