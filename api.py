# encoding: utf-8

from flask import Flask
app = Flask(__name__)

from ads.api import ads_bp
app.register_blueprint(ads_bp)

from topic_modeling.api import topic_bp
app.register_blueprint(topic_bp)

from sentiment.api import sentiment_bp
app.register_blueprint(sentiment_bp)
