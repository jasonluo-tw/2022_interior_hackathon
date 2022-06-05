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

def filter_shops_by_smart(data, dicts):
    """
    data: shops dataframe from shops-datadb.csv
    dicts['smart']
        values:
            bt_ss1 -> 小資首選金店面
            bt_ss2 -> 台北不夜城
            bt_ss3 -> 老屋新生潛力空間
            bt_ss4 -> 政府合作特色物件
    """
    ## Need implementation
    scores = None
    return data, scores

def filter_shops_by_options(data, dicts):
    """
    data: shops dataframe from shops-datadb.csv
    dicts (shop_feature_mapping.yaml)
        keys:
            county(only taipei)
            town
            house_type
            rental_price
            size
            MRT_distance
            human_age
            road/alley
            house_age
            special(?) -> might delete
    """
    ## Need implementation
    return data