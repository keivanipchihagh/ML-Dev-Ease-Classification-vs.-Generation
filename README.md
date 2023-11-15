# ML-Dev-Ease-Classification-vs.-Generation
An Exploratory (Data) Analysis on Development Ease in ML Applications - Text Classification vs. Generation


## Table of Contents
- Task 1




## Task 1
A simple scraper under `src/scrapers/models.py` is developed to obtain the models for both *Text-Classification* and *Text-Generation*, then store them under `data/models.csv`. Furthermore, the script supports arguments to change the number of models to retrieve (default: 20) and the sorting strategy (default: likes). A usage example is provided below:

```python
python .\src\scrapers\models.py --sort likes --count 20
```