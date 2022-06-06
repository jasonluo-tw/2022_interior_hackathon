from flask import request, jsonify, url_for, redirect, session
from flask_cors import cross_origin
from py_utils.get_data import get_region_data, process_region_data
from py_utils.get_data import get_shop_data, process_shop_data
from py_utils.get_data import get_all_wish_list, get_shop_embedding
from py_utils.get_data import read_geojson
from py_utils.function import calculate_shop_similarity
from py_utils.function import filter_shops_by_smart, filter_shops_by_options
from py_utils.function import calculate_shop_embedding
from py_utils.store_data import store_wishlist
import yaml, os
import pandas as pd

with open('./path.yaml', 'r') as f:
    config_path = yaml.safe_load(f)

@cross_origin()
def get_region_info():
    args = request.args
    if 'second_dis' in args.to_dict():
        data = get_region_data(config_path['data'], town_name=args['town'], second_dis=args['second_dis'])
        response = process_region_data(data, second_dis=args['second_dis'])
    else:
        data = get_region_data(config_path['data'], town_name=args['town'], second_dis=None)
        response = process_region_data(data)

    return jsonify(response)

# This is used by Vue, at tenant map
@cross_origin()
def get_shop_info():
    args = request.args
    data = get_shop_data(config_path['data'])

    ##TODO: filtering
    scores = None
    ## smart search
    if 'smart' in args.to_dict():
        dicts = args.to_dict()
        data, scores = filter_shops_by_smart(config_path['data'], data, dicts)
    ## general filter
    elif 'county' in args.to_dict():
        dicts = args.to_dict()
        data = filter_shops_by_options(data, dicts)
    
    ## get top N items
    if 'counts' in args.to_dict():
        data = data.iloc[:int(args['counts'])]

    ## process_shop_data
    data, response = process_shop_data(data, scores=scores)

    return jsonify(response)

## confirm login
@cross_origin()
def confirm_landlord_login():
    form = request.form.to_dict()
    data = get_shop_data(config_path['data'])

    ## check if user_index in data
    data['user_index'] = data['user_index'].astype('str')

    if form['username'] in data['user_index'].tolist():
        data = data[data['user_index'] == form['username']]
        data, response = process_shop_data(data)
        session.permanent = True
        ## Store data to cookie
        session.clear()
        session['landlord_houses_'+form['username']] = response
        session['username'] = form['username']
        #print(response)
        return redirect(url_for("landlord_page", username=form['username']))
    else:
        response = 'NoData'
        return jsonify(response)

## This is used by Vue, at landlord map page
#@cross_origin()
def calculate_scores_wish_list():
    ## Get the house index by user
    ### TEST code
    #username = '0'
    #house_index = '0'
    #data = get_shop_data(config_path['data'])
    #data['user_index'] = data['user_index'].astype('str')
    #data = data[data['user_index'] == username]
    #data, response = process_shop_data(data)
    #shop_items = response
    ###

    ### Get data from URL get, get house index/or name
    args = request.args.to_dict()
    try:
        username = session['username']
        shop_items = session['landlord_houses_'+username]
        house_index = args['house_index']
        for item in shop_items:
            if str(item['house_index']) == house_index:
                target_shop_item = item
                break
        ## get shop embedding 
        target_shop_embedding = get_shop_embedding(config_path['data'], house_index)
    except:
        ##TEST
        #args = {'town': '松山區', 'item_name': '哈囉', 'house_type': 'villa'}
        if "item_name" in args:
            target_shop_embedding, target_shop_item = calculate_shop_embedding(config_path['data'], args)
        else:
            response = 'Error'
            return jsonify(response)

    ## get all wish list
    ##TODO: check join features 
    wish_list, wish_embedding = get_all_wish_list(config_path['data'])

    scores, index = calculate_shop_similarity(target_shop_embedding, wish_embedding)

    wish_list['scores'] = ['%.2f'%(i) for i in scores]
    ## wish list is DataFrame 
    sorted_wish_list = wish_list.iloc[index]
    top_10_wish = sorted_wish_list.iloc[:10]
    top_10_wish = top_10_wish.fillna("")
    ## process town
    town = top_10_wish['town']
    town_counts = town.value_counts().to_dict()
    town = list(set(town))
    ## get town longitude, latitude
    town_info = pd.read_csv(os.path.join(config_path['data'], 'final_output', 'district_features.csv'))
    town_info = town_info[['TOWN', 'lon', 'lat']].set_index('TOWN')
    town_info = town_info.loc[town].to_dict('index')
    ## make geojson
    geojson_pts = []
    for town_name in town:
        g_point = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [town_info[town_name]['lon'], town_info[town_name]['lat']]
            },
            "properties": {
                "text": str(town_counts[town_name]),
                "radius": 20
            }
        }
        geojson_pts.append(g_point)
    ## end make geopoint

    top_10_wish = list(top_10_wish.to_dict('index').values())

    output = {'wish': top_10_wish, 
              'target_shop': [target_shop_item],
              'town': town,
              'town_counts': town_counts,
              'town_info': town_info,
              'town_geojson': geojson_pts
              }

    return jsonify(output)

@cross_origin()
def store_tenant_wish():
    form = request.form.to_dict()
    try:
        store_wishlist(config_path['data'], config_path['mapping_file'], form)
        response = 'success'
    except:
        response = 'failure'

    return jsonify(response)

def get_geojson():
    args = request.args
    if args['type'] == 'shop_area':
        geojson = read_geojson(config_path['data'], prefix='', filename='shop_area.geojson')
    elif args['type'] == 'district':
        name = '臺北市'+args['name']
        geojson = read_geojson(config_path['data'], prefix='district', filename=f'{name}.geojson')
    elif args['type'] == 'second_district':
        name = args['name']
        geojson = read_geojson(config_path['data'], prefix='second_district', filename=f'{name}.geojson')

    return jsonify(geojson)

def get_poi_info():
    args = request.args
    type_name = args['name']
    
    ##TEST
    #type_name = '餐廳餐館'

    data = pd.read_csv(os.path.join(config_path['data'], 'existing_shops', type_name+'.csv'))
    data = data[['商業名稱', 'lon', 'lat']].rename(columns={'商業名稱': 'name', 'lon': 'longitude', 'lat': 'latitude'})
    data = data.fillna('')
    if type_name == '餐廳餐館':
        data = data.iloc[::2]
    out_dict = data.to_dict('index')
    out_dict = list(out_dict.values())

    return jsonify(out_dict)

#def 

if __name__ == '__main__':
   #json_wish = calculate_scores_wish_list()
    #print(json_wish)
    get_poi_info()
