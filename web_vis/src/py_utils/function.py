import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sys

def calculate_shop_similarity(target_shop_embedding, wish_embedding):
    target_shop_embedding, wish_embedding = get_only_embedding(target_shop_embedding, wish_embedding)
    scores = np.squeeze(cosine_similarity(target_shop_embedding, wish_embedding))
    scores = (np.array(scores) + 1) * 50
    index = np.argsort(scores)[::-1]

    print(scores, index)
    return scores, index

def get_only_embedding(target_shop_embedding, wish_embedding):
    wish_embedding = wish_embedding.drop(columns=['index', 'name', 'email'])
    cols = list(wish_embedding.columns)
    target_shop_embedding = target_shop_embedding[cols]

    return target_shop_embedding.astype('float'), wish_embedding.astype('float')
