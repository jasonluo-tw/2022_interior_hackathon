import pandas as pd

def calculate_shop_similarity(data):
    scores = [120 - i for i in range(len(data))]

    return scores