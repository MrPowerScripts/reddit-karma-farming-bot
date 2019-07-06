from flask import (Flask, request, session, g, redirect, url_for, abort,
                   render_template, flash, jsonify, copy_current_request_context)
import os
import sqlite3
import psutil

import subprocess
import multiprocessing
from logger import log


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    USERNAME='admin',
    PASSWORD='default'
)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('app.db')
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    return connect_db()


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'app_db'):
        g.app_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print "Initialized db"


@app.route('/')
def home_page():
    db = get_db()
    cur = db.execute('select username, proxy, running from profiles')
    entries = cur.fetchall()
    return render_template('home.html', entries=entries)


@app.route('/save', methods=['POST'])
def save_bot():
    db = get_db()
    db.execute(
        'insert into profiles (username, password, client_id, client_secret, proxy, running) values (?, ?, ?, ?, ?, ?)',
        [request.form['username'], request.form['password'], request.form['client_id'],
         request.form['client_secret'], request.form['proxy'], 0])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('home_page'))


@app.route('/run', methods=['POST'])
def run_bot():
    bot_name = request.get_data().split("=")[1]

    @copy_current_request_context
    def handle_sub_view():
        exec_command(bot_name)
        # Do Expensive work

    p = multiprocessing.Process(target=handle_sub_view)
    p.start()
    return jsonify(started='success')


@app.route('/delete', methods=['POST'])
def delete_bot():
    bot_name = request.get_data().split("=")[1]
    db = get_db()
    db.execute(
        """DELETE from profiles  WHERE username= ? """,
        (bot_name,))
    db.commit()

    return jsonify(started='success')


@app.route('/kill', methods=['POST'])
def kill_bot():
    db = get_db()

    uname = request.get_data().split("=")[1]
    cur = db.cursor()
    cur.execute(
        """SELECT pid from profiles  WHERE username= ? """,
        (uname,))
    pid = cur.fetchone()
    pid = pid['pid']
    log.info("PID trying to terminate bot "+uname+" process id " +str(pid))

    if pid:
        print "********* in"
        try:
            parent = psutil.Process(int(pid))

            children = parent.children(recursive=True)
            log.info("PID children  " + str(children))
            for process in children:
                process.terminate()
        except psutil.NoSuchProcess:
            pass
        db.execute(
            """UPDATE profiles SET running = ? ,pid = ?  WHERE username= ? """,
            (0, 0, uname))
        db.commit()
    return jsonify(started='success')


def exec_command(bot_name):
    db = connect_db()
    cur = db.execute("select * from profiles where username = '%s'" % bot_name)
    bot_details = cur.fetchone()
    proxy = bot_details['proxy']
    ip = proxy.split(":")[0].strip()
    port = proxy.split(":")[1].strip()
    os.environ["REDDIT_CLIENT_ID"] = bot_details['client_id']
    os.environ["REDDIT_SECRET"] = bot_details['client_secret']
    os.environ["REDDIT_PASSWORD"] = bot_details['password']
    os.environ["REDDIT_USER_AGENT"] = "exp made by u/" + bot_name
    os.environ["REDDIT_USERNAME"] = bot_name
    p = subprocess.Popen("python run.py " + ip + " " + port, shell=True)
    db.execute(
        """UPDATE profiles SET running = ? ,pid = ?  WHERE username= ? """,
        (1, p.pid, bot_name))
    db.commit()
    log.info("Started process ID " + str(p.pid))
    return p
