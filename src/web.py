#!/usr/bin/python
# coding: utf-8
from flask import Flask
from utils import get_db_size
import os

app = Flask(__name__)

port = os.environ.get('PORT') or 5000


@app.route('/')
def entry_point():
    return "DB Size: " + str(get_db_size(human=True)) + " MB"

def webapp():
  if os.environ.get('PORT'):
    app.run(port=port,host='0.0.0.0')
  else:
    app.run(port=port)
