#!/usr/local/bin/python3

import os, sys
import pandas as pd
from simpletransformers.classification import MultiLabelClassificationModel

def run_experiment(model_name, pretrain_name):

    # Specifies models.
    args = {"train_batch_size": 8,
            "eval_batch_size": 8,
            "num_train_epochs": 3,
            "learning_rate": 1e-5,
            "warmup_ratio": 0.1,
            "warmup_steps": 100,
            "reprocess_input_data": True,
            "overwrite_output_dir": True}
    model = MultiLabelClassificationModel(model_name, pretrain_name, num_labels=2, args=args)

    # Train models.
    model.train_model(train_df)
    
    # Predicts labels.
    for split, df in zip(["train", "test", "predict"], [train_df, test_df, predict_df]):
        if split in {"train", "test"} or [split, model_name] == ["predict", "roberta"]:
            _, predictions = model.predict(df["text"])
            df["predictions"] = [list(p) for p in predictions]
            df.to_csv(os.path.join(data_path, split + "_" + model_name + "_pred.csv"), index=False)

if __name__ == "__main__":

    # Gets path.
    sys_path = sys.path[0].split("src")[0]
    data_path = os.path.join(sys_path, "data")
    train_path = os.path.join(data_path, "train.csv")
    test_path = os.path.join(data_path, "test.csv")
    predict_path = os.path.join(data_path, "predict.csv")

    # Reads data.
    train_df = pd.read_csv(train_path)
    train_df["labels"] = train_df["labels"].apply(lambda l: eval(l))
    test_df = pd.read_csv(test_path)
    predict_df = pd.read_csv(predict_path)

    # Runs experiments.
    model_names = ["xlnet", "bert", "roberta"]
    pretrain_names = ["xlnet-base-cased", "bert-base-cased", "roberta-base"]
    for model_name, pretrain_name in zip(model_names, pretrain_names):
        run_experiment(model_name, pretrain_name)
