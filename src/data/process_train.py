import pandas as pd
import os
from src.constants import DIR


def main():
    """
    Takes the cleaned data from data/clean and feature engineers some stuff to be documented later :)

    :return:
    """

    file_in = os.path.join(
        DIR.ROOT, "data", "processed", "memory_optimized_data.pkl"
    )

    df = pd.read_pickle(file_in)

    # Process stuff
    features = make_title_features(df)

    # Filter to only stuff which we have labels for
    file_in = os.path.join(DIR.ROOT, "data", "raw", "train_labels.csv")
    labels = pd.read_csv(file_in)
    subset = features.loc[labels.installation_id.unique()]

    full = subset.reset_index().merge(labels, on="installation_id")

    file_out = os.path.join(DIR.ROOT, "data", "processed", "features.pkl")
    full.to_pickle(file_out)


def make_title_features(df):
    df1 = df[["title", "installation_id"]].drop_duplicates()
    df1["temp"] = True
    features = df1.pivot(
        columns="title", values="temp", index="installation_id"
    ).fillna(False)

    features.columns = features.columns.astype(str)

    return features


if __name__ == "__main__":
    main()
