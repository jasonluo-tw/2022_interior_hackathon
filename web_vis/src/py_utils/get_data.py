from re import I
import json
import pandas as pd
import os, sys

def get_region_data(root_path, town_name=None, second_dis=None):
    file_path = os.path.join(root_path, 'final_output', 'district_features.csv')
    data = pd.read_csv(file_path)
    ## second district
    file_path = os.path.join(root_path, 'final_output', 'second_district_features.csv')
    second_data = pd.read_csv(file_path)
    ## electronic invoice
    file_path = os.path.join(root_path, 'electronic_invoice.csv')
    consumption_index = pd.read_csv(file_path)[['TOWN', 'industry', 'year', 'consumption_index']]
    if town_name is not None:
        data = data[data['TOWN'] == town_name]
        consumption_index = consumption_index[consumption_index['TOWN'] == town_name]
    if second_dis is not None:
        second_data = second_data[second_data['二級發布區代碼'] == second_dis]

    data = {'data': data, 'consumption_index': consumption_index, 'second_data': second_data}

    return data

def process_region_data(data, second_dis=None):
    consume_index = data['consumption_index']
    if second_dis is not None:
        second_data = data['second_data']
    else:
        second_data = data['data']
    data = data['data']
    ## land use
    all_land = second_data[['商業', '純住宅', '混合使用住宅']].copy()#.sum(axis=1)
    land_use = round(all_land+1 / float(all_land.sum(axis=1) +1) * 100)
    land_use = land_use.T.iloc[:, 0].to_dict()
    land_use = [{'name': key, 'y': int(land_use[key])} for key in land_use]
    ## age
    age = second_data[['0-14歲人口數', '15-24歲人口數', '25-39歲人口數', '40-64歲人口數', '65歲以上人口數']].copy()
    age = round(age / float(age.sum(axis=1)) * 100)
    age = age.T.iloc[:, 0].map(lambda x: int(x)).to_dict()
    ## shop price
    shop_price = {'name': '店舖價格', 'data': []}
    for i in range(104, 110):
        value = float(data['shop_price_unit_'+str(i)])
        shop_price['data'].append([i+1911, round(value)])
    shop_price = [shop_price]

    ## population
    population = {'x': [], 'value': []}
    keys = {'DAY_WORK(7:00~13:00)': '平日7-13時', 
                   'DAY_WORK(13:00~19:00)': '平日13-19時', 
                   'NIGHT_WORK': '平日晚上', 
                   'DAY_WEEKEND(7:00~13:00)': '週末7-13時', 
                   'DAY_WEEKEND(13:00~19:00)': '週末13-19時', 
                   'NIGHT_WEEKEND': '週末晚上'}
    for kk in keys:
        population['x'].append(keys[kk])
        population['value'].append(int(data[kk]))

    output = data[['人口數', '人口密度', 'bus_stops', 'MRT_stops']] .copy()
    output = output.T.iloc[:, 0].to_dict()

    ## consumption_index
    consume_index = consume_index.drop(columns=['TOWN'])
    index2name = {56: '餐飲業', 47: '零售業', 55:'住宿業'}
    consume_out = []
    for key in index2name:
        tmp = consume_index[consume_index['industry'] == key].copy().sort_values('year')
        dd = [[float(item['year']), float('%.1f'%(item['consumption_index']))] for index, item in tmp.iterrows()]
        cc = {'name': index2name[key], 'data': dd}
        consume_out.append(cc)

    ## add features
    output['land_use'] = land_use
    output['age'] = age
    output ['shop_price'] = shop_price
    output['population'] = population
    output['consume_index'] = consume_out

    return output

def get_shop_data(path):
    ##TODO: In the future, if the data becomes larger, we should consider database
    file_path = os.path.join(path, 'shops', '591-datadb.tsv')
    data = pd.read_csv(file_path, sep='\t')

    return data

def process_shop_data(data, scores=None):
    data = data
    #data = data[['house_index', '二級', 'town', 'name', 'rental_price', 'size', 'floor', 'address', 'longitude', 'latitude', 'type', 'house_age', 'MRT_within_1km',
    #             'Bus_within_1km', 'img_url', '餐廳餐館', '便利商店', '美容美髮服務', '日常用品零售', '飲料店業', '其他綜合零售']].copy()
    data = data.fillna('no data')
    data['house_index'] = data['house_index'].astype('str')

    if scores is not None:
        data['score'] = scores

    ## process response
    dicts = data.T.to_dict()

    response = [dicts[key] for key in dicts]

    return data, response

def get_shop_embedding(path, house_index):
    filepath = os.path.join(path, 'shops', 'shop_embedding.csv')
    shop_embedding = pd.read_csv(filepath)
    shop_embedding['house_index'] = shop_embedding['house_index'].astype('str')

    target_shop = shop_embedding[shop_embedding['house_index'] == house_index]

    return target_shop

def get_all_wish_list(path):
    ## get wish list
    file_path = os.path.join(path, 'wish_list', 'wish_info.csv')
    wish_list = pd.read_csv(file_path, dtype='str')
    ## get embedding list
    file_path = os.path.join(path, 'wish_list', 'wish_embedding.csv')
    wish_embedding = pd.read_csv(file_path, dtype='str')

    return wish_list, wish_embedding

def read_geojson(path, prefix, filename):
    filepath = os.path.join(path, 'geojson', prefix, filename)
    with open(filepath, 'r') as f:
        geojson = json.load(f)

    return geojson

if __name__ == '__main__':
    #data = get_region_data('/home/jasonluo/Documents/competition/2022_interior_hackathon/data', town_name='大安區', second_dis='A6303-18')
    #data = process_region_data(data)
    #print(data)
    data = get_shop_data('/home/jasonluo/Documents/competition/2022_interior_hackathon/data')
    data, response = process_shop_data(data)
    print(response)
    #get_all_wish_list('/home/jasonluo/Documents/competition/2022_interior_hackathon/data')

