#!/usr/bin/python
# coding: utf-8
from logger import log
from flask import Flask, render_template, jsonify
from logger import file_handler
import json
from db import get_db_size, get_user_info, get_all_db_size, get_all_karma
import os

app = Flask(__name__)

port = os.environ.get('PORT') or 5000

app.logger.addHandler(file_handler)

@app.route('/')
def entry_point():
  data = {}
  user = json.dumps(get_user_info(), sort_keys = True, indent = 4, separators = (',', ': '))
  data['user'] = user
  data['db'] = "DB Size: " + str(get_db_size(human=True)) + " MB"
  data['alldb'] = get_all_db_size()
  data['allkarma'] = get_all_karma()
  return render_template("dashboard.html", data=data)
  # return 

@app.route('/api/alldb')
def db_data():
  return jsonify(get_all_db_size())

def run():
  if os.environ.get('PORT'):
    app.run(port=port,host='0.0.0.0')
  else:
    app.run(port=port, debug=True)
