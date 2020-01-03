import pandas as pd
import os
import sys
from src.constants import DIR


def main(file_in, file_out):
    """
    Takes the cleaned data from data/clean and feature engineers some stuff to be documented later :)

    :return:
    """
    df = pd.read_pickle(file_in)

    full = process_train(df)

    full.to_pickle(file_out)


def process_train(df):
    # Process stuff
    features = make_title_features(df)

    # Filter to only stuff which we have labels for
    file_in = os.path.join(DIR.ROOT, "data", "raw", "train_labels.csv")
    labels = pd.read_csv(file_in)
    subset = features.loc[labels.installation_id.unique()]

    full = subset.reset_index().merge(labels, on="installation_id")

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
