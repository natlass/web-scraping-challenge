from pymongo import MongoClient
from flask import Flask, render_template, redirect
import scrape_mars

app=Flask(__name__)

mongo = MongoClient("mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    mars_dict2 = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_dict2) 

@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)