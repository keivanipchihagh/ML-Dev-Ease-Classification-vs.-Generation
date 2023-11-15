# ML-Dev-Ease-Classification-vs.-Generation
An Exploratory (Data) Analysis on Development Ease in ML Applications - Text Classification vs. Generation


## Table of Contents
- [Step 1](https://github.com/keivanipchihagh/ML-Dev-Ease-Classification-vs.-Generation#step-1)
- [Step 2](https://github.com/keivanipchihagh/ML-Dev-Ease-Classification-vs.-Generation#step-2)




## Step 1 - Obtaining Popular Models
A simple scraper is developed under `src/scrapers/models.py` using [huggingface library](https://pypi.org/project/huggingface-hub/). This script is used to retrieve models for both *Text-Classification* and *Text-Generation* and store them under `data/models.csv`. Furthermore, the script supports arguments to customize the results. A usage example is provided below:

```python
python .\src\scrapers\models.py --sort likes --count 20
```

## Step 2 - Obtaining ML Spaces
For this purpose, another scraper is developed under `src/scrapers/spaces.csv` and its process is broken down into two steps. First, a list of all spaces is acquired under `data/spaces.csv` which contains the names of *175k* ML apps. Then, using parallelism, more details of each space is retrieved (i.e. models and datasets).

> **Warning**
> Although it's very unlikely, parallelism could possibly result in DDOS attack, and thus should be used with caution.