#!/usr/local/bin/python3

import os, sys
import pandas as pd
import numpy as np

if __name__ == "__main__":
    
    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    train_path = os.path.join(data_path, "train.csv")
    test_path = os.path.join(data_path, "test.csv")

    # Reads data and overviews
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    print(len(train), len(test))
    df = pd.concat([train, test])
    count = df.groupby("labels").count()
    print(count, count / len(df))
    
