#!/usr/bin/python
# coding: utf-8
from flask import Flask
from utils import get_db_size
import os

app = Flask(__name__)

if 'DYNO' in os.environ:
  port = 80
else:
  port = 5000

@app.route('/')
def entry_point():
    return "DB Size: " + str(get_db_size(human=True)) + " MB"

def webapp():
  app.run(port=port)