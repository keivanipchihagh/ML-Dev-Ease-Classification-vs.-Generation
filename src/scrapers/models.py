##########################################################
#
# Copyright (C) 2023-PRESENT: Keivan Ipchi Hagh
#
# Email:            keivanipchihagh@gmail.com
# GitHub:           https://github.com/keivanipchihagh
#
##########################################################

import requests
import pandas as pd
from typing import List
from bs4 import BeautifulSoup
from argparse import ArgumentParser

# Constants
PIPELINE_TAGS = ['text-classification', 'text-generation']


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



def retrieve_models(pipeline_tag: str, sort: str) -> List[list]:
    """
        Retrieves models details

        Arguments:
            pipeline_tag (str): Model type to retrive
            sort (str): Sorting strategy
        Returns:
            (List[list]): List of models' details
    """

    # Retrieve URL content
    response = requests.get(
        url = "https://huggingface.co/models",
        params = {
            "pipeline_tag": pipeline_tag,   # Model type
            "sort": sort                    # Sorting strategy
        },
        headers = {
            "User-Agent": "Mozilla/5.0"     # Avoid being detected as bot
        }
    )

    soup = BeautifulSoup(response.content, "html.parser")
    elements = soup.find_all(
        name = "article",                   # Element name
        attrs = {"class": "group/repo"}     # Element classes
    )

    models: List[list] = []
    for element in elements:
        name: str = element.find('h4').text # Model name
        text: str = element.div.text        # Model details as text

        # Post-process
        text = text.replace('\n', '')       # Remove newlines
        text = text.replace('\t', '')       # Remove tabs
        details = text.split('•')           # Split to a list
        details.insert(0, name)             # Insert model name
        if len(details) == 4:
            details.insert(3, 0)            # In case it has no downloads

        models.append(details)
    
    return models



if __name__ == '__main__':
    args = load_args()      # Load CMD Arguments

    # Retrieve all model types
    models: list = []
    for pipeline_tag in PIPELINE_TAGS:
        _ = retrieve_models(pipeline_tag, args.sort)
        _ = _[:args.count]  # Filter the top n items
        models.extend(_)

    # Construct DataFrame
    df = pd.DataFrame(
        data = models,
        columns = ['name', 'tag', 'updated_at', 'downloads', 'likes']
    )
    df.to_csv('data/models.csv', index=False)
