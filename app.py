from flask import Flask, render_template
from foreign_summary import summarize_foreign_news
from local_summary import summarize_local_news
from scraper import scrape_tv3_news
import time

app = Flask(__name__)

# cache storage
cache = {
    "articles": None,
    "timestamp": 0,
    "foreign_summary": None,
    "local_summary": None
}

CACHE_DURATION = 60 * 240  # cache for 240 minutes(4 hours)


def get_cached_articles():
    now = time.time()
    if cache["articles"] is None or (now - cache["timestamp"]) > CACHE_DURATION:
        print("Scraping fresh articles...")
        cache["articles"] = scrape_tv3_news()
        cache["timestamp"] = now
        # reset summaries because articles changed
        cache["foreign_summary"] = None
        cache["local_summary"] = None
    else:
        print("✅ Using cached articles")
    return cache["articles"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/foreign")
def foreign():
    articles = get_cached_articles()
    if cache["foreign_summary"] is None:  # only summarize once per cache cycle
        print("Generating foreign summaries...")
        cache["foreign_summary"] = summarize_foreign_news(articles)
    else:
        print("Using cached foreign summaries")
    return render_template("summaries.html", category="Foreign News", summaries=cache["foreign_summary"])


@app.route("/local")
def local():
    articles = get_cached_articles()
    if cache["local_summary"] is None:  # only summarize once per cache cycle
        print("Generating local summaries...")
        cache["local_summary"] = summarize_local_news(articles)
    else:
        print("Using cached local summaries")
    return render_template("summaries.html", category="Local News", summaries=cache["local_summary"])


if __name__ == "__main__":
    app.run(debug=False)
