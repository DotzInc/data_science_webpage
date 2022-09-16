import os

from flask import Blueprint
from flask import request, render_template, redirect, url_for
import requests
import yaml


otim = Blueprint("otim", __name__, template_folder="templates", url_prefix="/otim")


@otim.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_yaml = request.form['yaml_data']
        return redirect(url_for('otim.submitted', input_yaml=input_yaml))
    return render_template(
        "page/index.html",
        flask_debug=os.environ["FLASK_DEBUG"]
    )


@otim.get("/submitted")
def submitted():
    input_yaml = request.args['input_yaml']
    input_data = yaml.safe_load(input_yaml)
    response = requests.post('http://promo_scheduling:5000/v1/promo_scheduling', json=input_data)
    msg_content = response.content.decode('unicode-escape')
    return render_template(
        "page/submitted.html",
        flask_debug=os.environ["FLASK_DEBUG"],
        msg_content=msg_content
    )
