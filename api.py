# encoding: utf-8

from flask import Flask
app = Flask(__name__)

from classify_chat.api import ads_bp
app.register_blueprint(ads_bp)

from cluster_comment_taptap.api import topic_bp
app.register_blueprint(topic_bp)
