from flask import Flask, jsonify, request
import csv
import pandas as pd
from storage import all_articles, liked_articles, not_liked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    article_data = {
        "title": all_articles[0][11],
        "language": all_articles[0][13],
        "author_country": all_articles[0][8],
        "contentId": all_articles[0][3]
    }
    return jsonify({
        "data": article_data,
        "status": "success"
    })

@app.route("/liked-article", methods = ["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/disliked-article", methods = ["POST"])
def disliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status":"success"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[11],
            "language": article[13],
            "author_country": article[8],
            "contentId": article[3]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended, _ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[11],
            "language": recommended[13],
            "author_country": recommended[8],
            "contentId": recommended[3]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status" : "success"
    }), 200 

if __name__ == "__main__":
    app.run()