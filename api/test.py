#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from zhilianzp.api.untils import MongoApi

app = Flask(__name__)

tasks = [MongoApi().mongo_api()]


@app.route("/api/v1.0/tasks")
def get_tasks():
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True)
