from flask import Flask, render_template
from scraper import scrape_tv3_news


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summary")
def summary():
    articles = scrape_tv3_news() 
    
if __name__ == "__main__":
    app.run(debug=True) 