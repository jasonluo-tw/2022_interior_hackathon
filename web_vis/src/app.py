from flask import Flask, jsonify, request, render_template
from flask_cors import cross_origin
from py_utils.get_data import get_region_data, process_region_data
from py_utils.get_data import get_shop_data, process_shop_data
from py_utils.calculation import calculate_shop_similarity
import yaml

app = Flask(__name__)

with open('./path.yaml', 'r') as f:
    config_path = yaml.safe_load(f)

@app.route('/get_region_info', methods=['GET'])
@cross_origin()
def get_region_info():
    args = request.args
    data = get_region_data(config_path['data'], town_name=args['town'])
    response = process_region_data(data)

    ## Test
    #return args
    return jsonify(response)

@app.route('/get_shop_info', methods=['GET'])
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


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()
