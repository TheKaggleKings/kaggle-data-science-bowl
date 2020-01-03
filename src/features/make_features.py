import pandas as pd
import os
import sys
from src.constants import DIR


def main(file_in, file_out, add_labels=False):
    """
    Reads clean data from `file_in` and outputs some features in `file_out`.

    Adds labels from train_labels.csv if add_labels is True.

    :param file_in: Path to cleaned data
    :param file_out: Path to output file
    :param add_labels: If `True`, adds column with training labels
    :return:
    """
    df = pd.read_pickle(file_in)

    full = process_train(df, add_labels)

    full.to_pickle(file_out)


def process_train(df, add_labels):
    # Process stuff
    features = make_title_features(df)

    if add_labels:
        # Filter to only stuff which we have labels for
        file_in = os.path.join(DIR.ROOT, "data", "raw", "train_labels.csv")
        labels = pd.read_csv(file_in)
        subset = features.loc[labels.installation_id.unique()]
        full = subset.reset_index().merge(labels, on="installation_id")
    else:
        full = features

    return full


def make_title_features(df):
    df1 = df[["title", "installation_id"]].drop_duplicates()
    df1["temp"] = True
    features = df1.pivot(
        columns="title", values="temp", index="installation_id"
    ).fillna(False)

    features.columns = features.columns.astype(str)

    return features


if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)
