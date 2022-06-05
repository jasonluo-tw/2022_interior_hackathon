import pandas as pd
import numpy as np
import os
import yaml

def store_wishlist(path, wish_form):
    ## open mapping table
    with open('/home/jasonluo/Documents/competition/2022_interior_hackathon/web_vis/src/py_utils/shop_feature_mapping.yaml', 'r') as f:
        map_table = yaml.safe_load(f)

    ## read wishlist & embedding
    folder = os.path.join(path, 'wish_list')
    if os.path.exists(os.path.join(folder, 'wish_info.csv')):
        wish_info = pd.read_csv(os.path.join(folder, 'wish_info.csv'), dtype='str')
        wish_embed = pd.read_csv(os.path.join(folder, 'wish_embedding.csv'), dtype='str')
        wish_info = wish_info.drop('index', axis=1)
        wish_embed = wish_embed.drop('index', axis=1)
    else:
        wish_info = None

    ## make embedding
    wish_embedding = {}
    wish_embedding['name'] = wish_form['name']
    wish_embedding['email'] = wish_form['email']
    tmp_embedding = make_embedding(path, wish_form, map_table)
    wish_embedding.update(tmp_embedding)
    ## change wish_form
    wish_form = change_wish_attr(wish_form, map_table)
    print(wish_form)
    ## Store data
    wish_form = pd.DataFrame({i: [wish_form[i]] for i in wish_form})
    wish_embedding = pd.DataFrame({i: [wish_embedding[i]] for i in wish_embedding})
    if wish_info is not None:
        wish_info = pd.concat((wish_info, wish_form))
        wish_embed = pd.concat((wish_embed, wish_embedding))
        ##
        wish_info = wish_info.drop_duplicates()
        wish_embed = wish_embed.drop_duplicates()
        wish_info.insert(0, 'index', np.arange(len(wish_info)))
        wish_embed.insert(0, 'index', np.arange(len(wish_embed)))
    else:
        wish_info = wish_form
        wish_info.insert(0, 'index', 0)

        wish_embed = wish_embedding
        wish_embed.insert(0, 'index', 0)

    wish_info.to_csv(os.path.join(folder, 'wish_info.csv'), index=None, float_format="%.5f")
    wish_embed.to_csv(os.path.join(folder, 'wish_embedding.csv'), index=None, float_format="%.5f")

def make_embedding(path, wish_form, map_table):
    ## open embedding statics
    embed_statics = pd.read_csv(os.path.join(path, 'shops', 'embedding_statics.csv'))
    embed_statics = embed_statics.set_index('feature_name')

    #print(wish_form)
    #print(map_table)
    wish_embedding = {}
    ## read district data & second data
    filepath = os.path.join(path, 'final_output', 'district_features.csv')
    district_feature = pd.read_csv(filepath)
    district_feature = district_feature.set_index('TOWN')
    ## read mean/std data
    ## longitude, latitude
    district = district_feature.loc[wish_form['town']]
    wish_embedding['longitude'] = district['lon']
    wish_embedding['latitude'] = district['lat']
    ## numerical data
    ##TODO: 裝潢
    keys = ['rental_price', 'size', 'house_age', 'MRT_distance', '裝潢']
    for i in keys:
        value = map_table[i][wish_form[i]][0]
        if i == 'rental_price' or i == 'size':
            value = np.log(value)
        wish_embedding[i] = value

    ## normalize
    for i in wish_embedding:
        min_ = embed_statics.loc[i, 'min']
        max_ = embed_statics.loc[i, 'max']
        wish_embedding[i] = (wish_embedding[i] - min_) / (max_ - min_)

    ## categorical data
    wish_embedding['road/alley'] = map_table['road/alley'][wish_form['road/alley']][0]
    # human age, people_stream, house_type
    for ele in ['human_age', 'people_stream', 'house_type']:
        for key in map_table[ele]:
            if key == wish_form[ele]:
                value = 1
            else:
                value = 0
            wish_embedding[map_table[ele][key][0]] = value

    for key in wish_embedding:
        wish_embedding[key] = '%.5f'%(wish_embedding[key])

    return wish_embedding

def change_wish_attr(wish_form, map_table):
    wish_form['county'] = '台北市'
    keys = ['house_type', 'rental_price', 'size', 'MRT_distance', 
     'house_age', 'human_age', 'road/alley', '裝潢', 'people_stream']

    for key in keys:
        wish_form[key] = map_table[key][wish_form[key]][1]

    return wish_form

if __name__ == '__main__':
    with open("/home/jasonluo/Documents/competition/2022_interior_hackathon/data/wish_list/wishlist_demo.csv") as f:
        data = f.readlines()

    header = data[0].rstrip('\n').split(',')[1:]
    info = data[1].rstrip('\n').split(',')[1:]

    wish_form = dict([(i, j) for i, j in zip(header, info)])
    path = '/home/jasonluo/Documents/competition/2022_interior_hackathon/data'
    store_wishlist(path, wish_form)
    #print(wish_form)
