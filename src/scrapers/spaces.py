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
from dotenv import load_dotenv
from pandarallel import pandarallel
from typing import Iterable, List
from huggingface_hub.hf_api import SpaceInfo

load_dotenv()
pandarallel.initialize(
    progress_bar = True,
    nb_workers = 32
)


def collect_spaces(spaces: Iterable[SpaceInfo]) -> List[dict]:
    """
        Collects spaces data

        Parameters:
            spaces (Iterable[ModelInfo]): Spaces iterable
        Returns:
            (List[dict]): List of dictionaries containing data for each space
    """
    data = []
    for _ in spaces:
        data.append({
            'name': _.id,
            'likes': _.likes,
        })
    return data



def collect_space_info(row: pd.Series) -> pd.Series:
    """
        Collect extra information about each space

        Parameters:
            row (pd.Series): Single DataFrame row
        Returns:
            (pd.Series): Modified row
    """
    import os
    import huggingface_hub
    TOKEN = os.getenv("HUGGING_FACE_TOKEN")

    _ = huggingface_hub.space_info(
        repo_id = row['name'],
        token = TOKEN,
    )
    row['author'] = _.author
    row['last_modified'] = _.author
    # models (may not be available)
    try:
        row['models'] = _.models
    except:
        row['models'] = None

    return row


if __name__ == '__main__':

    # Retrieve Models from HuggingFace
    spaces = huggingface_hub.list_spaces()

    data = collect_spaces(spaces)   # Collect spaces list
    df = pd.DataFrame(data = data)  # Convert to DataFrame
    df.to_csv('data/spaces.csv', index=False)

    # Collect extra information for spaces
    # NOTE: Using pandarallel would run the function on all cores, and is likely to simulate a small DDOS attack
    #       on HuggingFace API servers, and thus may not be a good solution. However, it's x64 faster than normal (:
    df = df.parallel_apply(collect_space_info, axis=1)
    # df = df.apply(collect_space_info, axis=1)

    df.to_csv('data/spaces_extra.csv', index=False)