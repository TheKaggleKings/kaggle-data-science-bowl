import sys

import pandas as pd


def main(file_in, file_out):
    """
    Reads csv from `file_in` and outputs pickle to `file_out`.

    This cleaning script works on both test.csv and train.csv

    I think this makes data_optimizer_script.py redundant but it might be needed for less powerful computers

    :param file_in:
    :param file_out:
    :return:
    """
    test = pd.read_csv(file_in)

    test = clean_test(test)

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
    args = sys.argv[1:]
    main(*args)
