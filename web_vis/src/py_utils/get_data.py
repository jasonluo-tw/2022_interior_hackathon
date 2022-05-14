from re import I
import pandas as pd
import os, sys

def get_region_data(root_path, town_name=None):
    file_path = os.path.join(root_path, 'final_output', 'district_features.csv')
    data = pd.read_csv(file_path)
    if town_name is not None:
        data = data[data['TOWN'] == town_name]

    return data

def process_region_data(data):
    ## land use
    all_land = data[['商業', '純住宅', '混合使用住宅']].copy()#.sum(axis=1)
    land_use = round(all_land / float(all_land.sum(axis=1)) * 100)
    land_use = land_use.T.iloc[:, 0].to_dict()
    land_use = [{'name': key, 'y': int(land_use[key])} for key in land_use]
    ## age
    age = data[['0-14歲人口數', '15-64歲人口數', '65歲以上人口數']].copy()
    age = round(age / float(age.sum(axis=1)) * 100)
    age = age.T.iloc[:, 0].map(lambda x: int(x)).to_dict()
    ## shop price
    shop_price = {'x': [], 'value': []}
    for i in range(104, 110):
        value = float(data['shop_price_unit_'+str(i)])
        shop_price['x'].append(i)
        shop_price['value'].append(round(value))
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

    ## add features
    output['land_use'] = land_use
    output['age'] = age
    output ['shop_price'] = shop_price
    output['population'] = population

    return output

def get_shop_data(path):
    ##TODO: In the future, if the data becomes larger, we should consider database
    file_path = os.path.join(path, 'shop_info.csv')
    data = pd.read_csv(file_path)

    return data

def process_shop_data(data, scores=None):
    ##TODO: image url/path
    data = data[['town', 'name', 'rental_price', 'size', 'floor', 'address', 'longitude', 'latitude', 'type', 'house_age', 'MRT_within_1km', 'bus_within_1km']].copy()
    data = data.fillna('no data')
    if scores is not None:
        data['score'] = scores

    ## process response
    dicts = data.T.to_dict()

    response = [dicts[key] for key in dicts]

    return data, response


if __name__ == '__main__':
    data = get_region_data('/home/jasonluo/Documents/competition/2022_interior_hackathon/data', town_name='松山區')
    data = process_region_data(data)
    #print(data)
    data = get_shop_data('/home/jasonluo/Documents/competition/2022_interior_hackathon/data')
    data = process_shop_data(data)
    #print(data)
