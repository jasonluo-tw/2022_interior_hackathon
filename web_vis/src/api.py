from flask import request, jsonify, url_for, redirect, session
from flask_cors import cross_origin
from py_utils.get_data import get_region_data, process_region_data
from py_utils.get_data import get_shop_data, process_shop_data
from py_utils.get_data import get_all_wish_list, get_shop_embedding
from py_utils.function import calculate_shop_similarity
from py_utils.function import filter_shops_by_smart, filter_shops_by_options
from py_utils.store_data import store_wishlist
import yaml

with open('./path.yaml', 'r') as f:
    config_path = yaml.safe_load(f)

@cross_origin()
def get_region_info():
    args = request.args
    data = get_region_data(config_path['data'], town_name=args['town'], second_dis=args['second_dis'])
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
        data, scores = filter_shops_by_smart(data, dicts['smart'])
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
@cross_origin()
def calculate_scores_wish_list():
    ## Get the house index by user
    ### Get data from URL get, get house index/or name
    #form = request.form.to_dict()
    #try:
    #    username = session['username']
    #    shop_items = session['landlord_page_'+username]
    #    house_index = form['house_index']
    #else:
    #    resopne = 'Error'
    #    return jsonify(response)

    ## TEST code
    username = '0'
    house_index = '0'
    data = get_shop_data(config_path['data'])
    data['user_index'] = data['user_index'].astype('str')
    data = data[data['user_index'] == username]
    data, response = process_shop_data(data)
    shop_items = response
    ##
    for item in shop_items:
        if str(item['house_index']) == house_index:
            target_shop_item = item
            break
    ## get shop embedding 
    target_shop_embedding = get_shop_embedding(config_path['data'], house_index)
    ## get all wish list
    wish_list, wish_embedding = get_all_wish_list(config_path['data'])

    scores, index = calculate_shop_similarity(target_shop_embedding, wish_embedding)

    wish_list['scores'] = scores
    ## wish list is DataFrame 
    sorted_wish_list = wish_list.iloc[index]
    top_10_wish = wish_list.iloc[:10]
    
    top_10_wish = list(top_10_wish.to_dict('index').values())

    #return response
    return jsonify(response)

#@cross_origin()
def store_tenant_wish():
    form = request.form.to_dict()
    try:
        store_wishlist(config_path['data'], form)
        response = 'success'
    except:
        response = 'failure'

    return jsonify(response)

if __name__ == '__main__':
    json_wish = calculate_scores_wish_list()
    print(json_wish)
