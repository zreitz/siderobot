#!/usr/bin/env python3
import argparse 
import os

import tensorflow as tf 
import tensorflow_text


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, required=True,
        help="Journal article abstract.")
    parser.add_argument(
        "-m", "--model_dir", type=str, required=True,
        help="Path to model dir.")
    return parser.parse_args()


def inference(model, query: str) -> float:
    return tf.sigmoid(model(tf.constant([query]), training=False)).numpy()[0][0]


def main() -> None:
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
    args = cli()
    model = tf.saved_model.load(args.model_dir)
    print(inference(model, args.input))
    exit(0)


if __name__ == "__main__":
    main()
