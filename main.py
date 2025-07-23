
## flask --app main run --debug

from flask import Blueprint
from flask import render_template, redirect, url_for, request
from markupsafe import escape
from flask import Flask
import ast

from models.sentiment_analysis import get_product_list

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET"])
def hello_world():
    return render_template("home_page.html")

@app.route("/", methods=["POST"])
def find_products():
        if request.method == 'POST':
             usr_name = request.form.get("usr_name")            # get the input user name
             if usr_name != "":                                 # if user name not empty
                  products = get_product_list(usr_name)         # get the final list of 5 products to suggest to the customer
             else:
                  return render_template("home_page.html")
        return render_template("content.html", user_name = usr_name, products=products)
