from flask import Flask, jsonify, request, render_template, session
from flask_cors import cross_origin
from py_utils.get_data import get_region_data, process_region_data
from py_utils.get_data import get_shop_data, process_shop_data
from py_utils.calculation import calculate_shop_similarity
from datetime import timedelta
import yaml
import api

app = Flask(__name__)

with open('./path.yaml', 'r') as f:
    config_path = yaml.safe_load(f)

## router
@app.route("/landlord_login")
def landlord_login():
    return render_template("landlord_login.html")


@app.route("/landlord_page/<username>")
def landlord_page(username):
    try:
        response = session['landlord_houses_'+username]
        return render_template(f"landlord_page.html", username=username, house_infos=response)
    except:
        return "Please login again"

@app.route("/tenant_map")
def tenant_map():
    return app.send_static_file("demo.html")

## API 
app.add_url_rule('/get_region_info', view_func=api.get_region_info, methods=['GET'])
app.add_url_rule('/get_shop_info', view_func=api.get_shop_info, methods=['GET'])
app.add_url_rule('/login_confirm', view_func=api.confirm_landlord_login, methods=['POST'])


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.secret_key = "sjefkl;ajeske;fjaslkejgalsejg"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    #app.static_url_path = "/home/jasonluo/Documents/competition/2022_interior_hackathon/web_vis/dist/"
    #app.static_folder = "/home/jasonluo/Documents/competition/2022_interior_hackathon/web_vis/dist/"
    #app.root_path = "/home/jasonluo/Documents/competition/2022_interior_hackathon/web_vis/dist/"

    print(app.root_path)
    print(app.static_url_path)
    print(app.static_folder)
    app.run(debug=True)
