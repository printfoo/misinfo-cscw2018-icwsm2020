#!/usr/local/bin/python3

import os, sys
import pandas as pd

if __name__ == "__main__":

    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    measure_path = os.path.join(data_path, "predict_roberta_pred.csv")
    clean_path = os.path.join(data_path, "measurement.csv")
    fc_path =  os.path.join(sys_path, "resources", "factcheck.csv")

    # Reads raw data and saves plot data.
    thresholds = {"belief": 0.45105067, "disbelief": 0.43621385}
    df = pd.read_csv(measure_path, dtype="str")
    df["predictions"] = df["predictions"].apply(lambda p: eval(p))
    df["belief"] = df["predictions"].apply(lambda p: p[0] > thresholds["belief"])
    df["disbelief"] = df["predictions"].apply(lambda p: p[1] > thresholds["disbelief"])
    fc = pd.read_csv(fc_path, dtype="str")
    fc = fc.dropna(subset={"ruling_val"})
    fc["verdict"] = fc["ruling_val"].apply(lambda r: -1 if float(r) < 0 else (0 if float(r) < 2 else 1))
    df = df.merge(fc, left_on="id", right_on="social_id")
    df["delta"] = df.apply(lambda r: (float(r["time"]) - float(r["ruling_time"])) / (24 * 60 * 60), axis=1)
    df["before_fc"] = df.apply(lambda r: r["delta"] < 0, axis=1)
    df["count"] = 1
    for label in ["belief", "disbelief"]:
    
        # Measurement
        plot_path = os.path.join(data_path, label + "_measurement_plot.csv")
        tdf = df.groupby(["verdict", "before_fc", label]).count()
        print(tdf[["count"]])
        tdf[["count"]].to_csv(plot_path)
        
        # Platform
        plot_path = os.path.join(data_path, label + "_platform_plot.csv")
        tdf = df.groupby(["site", "before_fc", label]).count()
        print(tdf[["count"]])
        tdf[["count"]].to_csv(plot_path)
        
        # Factcheck
        plot_path = os.path.join(data_path, label + "_factcheck_plot.csv")
        print(tdf)
        df[["social_id", "verdict", "delta", "before_fc", label]].to_csv(plot_path, index=False)
