from tkinter import W
from flask import request, jsonify, url_for, redirect, session
from flask_cors import cross_origin
from py_utils.get_data import get_region_data, process_region_data
from py_utils.get_data import get_shop_data, process_shop_data
from py_utils.calculation import calculate_shop_similarity
import yaml

with open('./path.yaml', 'r') as f:
    config_path = yaml.safe_load(f)

@cross_origin()
def get_region_info():
    args = request.args
    data = get_region_data(config_path['data'], town_name=args['town'])
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
        print(response)
        return redirect(url_for("landlord_page", username=form['username']))
    else:
        response = 'NoData'
        return jsonify(response)

