from flask import Flask, jsonify, request, render_template, session
from flask_cors import cross_origin
from py_utils.get_data import get_region_data, process_region_data
from py_utils.get_data import get_shop_data, process_shop_data
#from py_utils.calculation import calculate_shop_similarity
from datetime import timedelta
import yaml
import api
from waitress import serve

app = Flask(__name__)

with open('./path.yaml', 'r') as f:
    config_path = yaml.safe_load(f)

## router
## index
@app.route("/")
def index():
    return render_template("index.html")

###########
## tenant webpage
###########
@app.route(config_path['tenant']['tenant'][0])
def tenant():
    return render_template(config_path['tenant']['tenant'][1])

@app.route(config_path['tenant']['wish_upload'][0])
def tenant_wish_upload():
    return render_template(config_path['tenant']['wish_upload'][1])

@app.route(config_path['tenant']['map'][0])
def tenant_map():
    return app.send_static_file(config_path['tenant']['map'][1])


###########
## landlord
###########
@app.route(config_path['landlord']['landlord'][0])
def landlord():
    return render_template(config_path['landlord']['landlord'][1])

@app.route(config_path['landlord']['login'][0])
def landlord_login():
    return render_template(config_path['landlord']['login'][1])

@app.route(config_path['landlord']['portal'][0])
def landlord_page(username):
    try:
        response = session['landlord_houses_'+username]
        return render_template(config_path['landlord']['portal'][1], username=username, house_infos=response)
    except Exception as e:
        print(e)
        return "Please login again"

@app.route(config_path['landlord']['upload'][0])
def landlord_upload():
    return render_template(config_path['landlord']['upload'][1])

@app.route(config_path['landlord']['map'][0])
def landlord_map():
    return app.send_static_file(config_path['landlord']['map'][1])
    

## API 
app.add_url_rule('/api/get_region_info', view_func=api.get_region_info, methods=['GET'])
app.add_url_rule('/api/get_shop_info', view_func=api.get_shop_info, methods=['GET'])
app.add_url_rule('/api/login_confirm', view_func=api.confirm_landlord_login, methods=['POST'])
app.add_url_rule('/api/calculate_similar',
                 view_func=api.calculate_scores_wish_list, methods=['GET'])

app.add_url_rule('/api/store_wish', view_func=api.store_tenant_wish, methods=['POST'])
app.add_url_rule('/api/get_geojson', view_func=api.get_geojson, methods=['GET'])
app.add_url_rule('/api/get_poi_info', view_func=api.get_poi_info, methods=['GET'])


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.secret_key = "sjefkl;ajeske;fjaslkejgalsejg"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

    #app.static_url_path = ""
    #app.static_folder = ""
    #app.root_path = ""
    #print(app.root_path)
    #print(app.static_url_path)
    #print(app.static_folder)

    app.run(debug=True)
    #serve(app, host='0.0.0.0', port=5000, url_scheme='https')
