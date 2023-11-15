##########################################################
#
# Copyright (C) 2023-PRESENT: Keivan Ipchi Hagh
#
# Email:            keivanipchihagh@gmail.com
# GitHub:           https://github.com/keivanipchihagh
#
##########################################################

import pandas as pd
import huggingface_hub
from typing import Iterable, List
from argparse import ArgumentParser
from huggingface_hub.hf_api import ModelInfo

# Constants
TAGS = ['text-classification', 'text-generation']


def load_args() -> dict:
    """
        CMD Arguments

        Returns:
            (dict): Dictionary of CMD arguments
    """
    parser = ArgumentParser(description='')
    parser.add_argument('--sort',   type=str,   default='likes',  help="Sorting Strategy")
    parser.add_argument('--count',  type=int,   default=20,       help="Number of models to retrieve per tag")
    return parser.parse_args()



def collect_data(models: Iterable[ModelInfo], tag: str) -> List[dict]:
    """
        Collects model data

        Parameters:
            models (Iterable[ModelInfo]): Models iterable
            tag (str): Tag for the models
        Returns:
            (List[dict]): List of dictionaries containing data for each model
    """
    data = []
    for _ in models:
        data.append({
            'name': _.id,
            'author': _.author,
            'last_modified': _.last_modified,
            'downloads': _.downloads,
            'likes': _.likes,
            'pipeline_tag': _.pipeline_tag,
            'tag': tag,
        })
    return data


if __name__ == '__main__':
    args = load_args()      # Load CMD Arguments

    data = []
    for tag in TAGS:
        # Retrieve Models from HuggingFace
        models = huggingface_hub.list_models(
            filter = tag,
            sort = args.sort,   # Sort strategy
            direction = -1,     # Sort Desending
            limit = args.count, # Top n
            full = True,        # Also fetch most model data
        )

        # Collect data
        _ = collect_data(models, tag)
        data.extend(_)

    # Save as .csv
    pd.DataFrame(
        data = data
    ).to_csv('data/models.csv', index=False)
