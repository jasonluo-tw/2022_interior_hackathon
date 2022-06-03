import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def calculate_shop_similarity(target_shop_embedding, wish_embedding):
    scores = np.squeeze(cosine_similarity(target_shop_embedding, wish_embedding))
    index = np.argsort(scores)[::-1]

    return scores, index


