# web_data_app.py
# June 2024
# Modified by: Alireza Ghasemi
#
# A simple program for demonstrating web applications using Flask and web scraping of data using BeautifulSoup.
# Detailed specifications are provided via the Assignment 5 README file.

import pandas as pd
from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup
import requests
import logging

# Initialize our FLASK application object from the Flask class like so:
app = Flask(__name__)

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/hello/<name>")
def hello_there(name):
    from datetime import datetime
    import re

    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    match_object = re.match("[a-zA-Z]+", name)
    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! Welcome to Assignment 5. It's " + formatted_now
    return content

@app.route("/data")
def book_data():
    try:
        source = requests.get("http://books.toscrape.com/")
        soup = BeautifulSoup(source.content, 'html.parser')
        book_results = soup.find_all(attrs={'class': 'product_pod'})

        titles = []
        prices = []

        for book in book_results:
            titles.append(book.h3.a.get('title'))
            prices.append(float(book.find('p', class_="price_color").text[1:]))

        book_data = pd.DataFrame(list(zip(titles, prices)), columns=['Titles', 'Prices'])
        book_data['Sale Prices'] = book_data['Prices'] * 0.75

        return render_template('template.html', tables=[book_data.to_html(classes='data')], titles=book_data.columns.values)
    
    except Exception as e:
        logging.error("Error occurred in /data route", exc_info=True)
        return jsonify(error=str(e)), 500

@app.route("/learn")
def learn():
    return "I learned how to build a web application using Flask."

if __name__ == '__main__':
    app.run(debug=True)
