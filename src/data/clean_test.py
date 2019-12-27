import os

import pandas as pd
from src.constants import DIR


def main():
    file_in = os.path.join(DIR.ROOT, "data", "raw", "test.csv")
    test = pd.read_csv(file_in)

    test = clean_test(test)

    file_out = os.path.join(DIR.ROOT, "data", "processed", "test.pkl")
    test.to_pickle(file_out)


def clean_test(df):
    df = set_dtypes(df)

    df = df.sort_values("timestamp")

    return df


def set_dtypes(df):
    df = df.astype(
        {
            "world": "category",
            "type": "category",
            "title": "category",
            "event_code": "category",
            "installation_id": "category",
            "game_session": "category",
            "event_id": "category",
        }
    )
    df.loc[:, "game_time"] = pd.to_numeric(df.game_time, downcast="integer")
    df.loc[:, "event_count"] = pd.to_numeric(df.event_count, downcast="integer")

    return df


if __name__ == "__main__":
    main()
