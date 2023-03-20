#!/usr/bin/env python3
import typing as ty 
import argparse 
import os

import tensorflow as tf 
import tensorflow_text


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, required=True,
        help="Input txt file with abstract per line.")
    parser.add_argument(
        "-m", "--model_dir", type=str, required=True,
        help="Path to model dir.")
    return parser.parse_args()


def inference(model, queries: ty.List[str]) -> ty.List[float]:
    return tf.sigmoid(model(tf.constant(queries), training=False)).numpy()[0]


def main() -> None:
    args = cli()

    queries = []
    with open(args.input, "r") as fo:
        for line in fo:
            queries.append(line.strip())

    model = tf.saved_model.load(args.model_dir)
    print(inference(model, queries))
    
    exit(0)


if __name__ == "__main__":
    main()
