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

    file_out = os.path.join(DIR.ROOT, "data", "processed", "features.pkl")
    features.to_pickle(file_out)


def make_title_features(df):
    df1 = df[["title", "installation_id"]].drop_duplicates()
    df1["temp"] = True
    features = df1.pivot(
        columns="title", values="temp", index="installation_id"
    ).fillna(False)

    return features


if __name__ == "__main__":
    main()
