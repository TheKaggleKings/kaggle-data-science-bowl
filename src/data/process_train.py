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
    # Comment

    file_out = os.path.join(DIR.ROOT, "data", "processed", "features.pkl")
    df.to_pickle(file_out)


if __name__ == "__main__":
    main()
