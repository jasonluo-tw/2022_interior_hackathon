from tkinter import W
from flask import request, jsonify, url_for, redirect, session
from flask_cors import cross_origin
from py_utils.get_data import get_region_data, process_region_data
from py_utils.get_data import get_shop_data, process_shop_data
from py_utils.get_data import get_all_wish_list
from py_utils.function import calculate_shop_similarity
import yaml

with open('./path.yaml', 'r') as f:
    config_path = yaml.safe_load(f)

@cross_origin()
def get_region_info():
    args = request.args
    data = get_region_data(config_path['data'], town_name=args['town'], second_dis=args['second_dis'])
    response = process_region_data(data)

    return jsonify(response)


@cross_origin()
def get_shop_info():
    args = request.args
    
    data = get_shop_data(config_path['data'])
    ##TODO
    scores = calculate_shop_similarity(data)
    if 'counts' in args.to_dict():
        data = data.iloc[:int(args['counts'])]
        scores = scores[:int(args['counts'])]

    ## process_shop_data
    data, response = process_shop_data(data, scores)

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
        session['landlord_houses_'+form['username']] = response
        session['username'] = form['username']
        print(response)
        return redirect(url_for("landlord_page", username=form['username']))
    else:
        response = 'NoData'
        return jsonify(response)

@cross_origin()
def calculate_scores_wish_list():
    ## Get the house index by user
    form = request.form.to_dict()
    username = session['username']
    shop_items = session['landlord_page_'+username]
    target_shop_item = shop_items[form['house_index']]
    ## get shop embedding 
    target_shop_embedding = get_shop_embedding(username, form['house_index'])
    ##
    wish_list, wish_embedding = get_all_wish_list(config_path['data'])

    scores, index = calculate_shop_similarity(target_shop_embedding, wish_embedding)
    ## Sorted
    sorted_scores = scores[index]
    sorted_wish_list = wish_list[index]
    ## and return the sorted wish list

    session['sorted_wish'] = wish_list[:10]

    return redirect(url_for("", ))

if __name__ == '__main__':
    pass
