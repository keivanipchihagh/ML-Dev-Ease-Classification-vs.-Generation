##########################################################
#
# Copyright (C) 2023-PRESENT: Keivan Ipchi Hagh
#
# Email:            keivanipchihagh@gmail.com
# GitHub:           https://github.com/keivanipchihagh
#
##########################################################

import pandas as pd
from ast import literal_eval
from dotenv import load_dotenv
from pandarallel import pandarallel

load_dotenv()
pandarallel.initialize(
    progress_bar = True,
    nb_workers = 64
)


def collect_space_info(row: pd.Series) -> pd.Series:
    """
        Collect extra information about each space

        Parameters:
            row (pd.Series): Single DataFrame row
        Returns:
            (pd.Series): Modified row
    """
    import os
    import requests
    import huggingface_hub
    TOKEN = os.getenv("HUGGING_FACE_TOKEN")

    try:
        _ = huggingface_hub.space_info(repo_id = row['name'], token = TOKEN)

        # Disregard repositories with more than 1k files
        if len(_.siblings) < 1000:
            row['size'] = None
            row['n_files'] = len(_.siblings)
            return row

        size = 0    # In bytes
        for sibling in _.siblings:
            res = requests.head(f"https://huggingface.co/spaces/{row['name']}/raw/main/{sibling.rfilename}")    # Get the metadata only
            size += int(res.headers['Content-Length'])

        row['size'] = size
        row['n_files'] = len(_.siblings)
    except:
        # Handle 404, 401 or 400 error codes
        row['size'] = None
        row['n_files'] = None
    return row


if __name__ == '__main__':

    spaces_df = pd.read_csv('data/spaces_extra.csv')
    models_df = pd.read_csv('data/models.csv')

    # Remove spaces with no issued models (since we won't analyze them)
    spaces_df = spaces_df.loc[spaces_df['models'].notna()].copy()

    # Transform each model to a row (expand)
    spaces_df['models'] = spaces_df['models'].apply(literal_eval)
    spaces_models_df = spaces_df.explode(column='models', ignore_index=True).rename(columns={'models': 'model'})

    # Remove models outside our scope of analysis
    spaces_models_df = spaces_models_df.loc[spaces_models_df['model'].isin(models_df['name'])]

    spaces_df = spaces_df.loc[spaces_df['name'].isin(spaces_models_df['name'])]
    print(f"N.Repositories to fetch: {spaces_df.shape[0]}")

    # Collect extra information for spaces
    # NOTE: Using pandarallel would run the function on all cores, and is likely to simulate a small DDOS attack
    #       on HuggingFace API servers, and thus may not be a good solution. However, it's x64 faster than normal (:
    df = spaces_df.parallel_apply(collect_space_info, axis=1)
    # df = df.apply(collect_space_info, axis=1)

    df.to_csv('data/files.csv', index=False)
