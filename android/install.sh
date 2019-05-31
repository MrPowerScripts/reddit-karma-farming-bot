#!/bin/bash
set -ex

cp -a ../src .
# make sure we can write to brains dir
chmod u+w brains
# clang required for PyStemmmer
apt install nano git python2-dev sqlite libffi-dev clang -yq
pip2 install --upgrade pip -r requirements.txt
# now we need to alter a few paths for the 'brain'
python2 - <<'EOF'
import os
working_dir = os.getcwd()
util_file = "src/utils.py"
with open(util_file, "r") as f:
    lines = f.read().split("\n")
    _DB_DIR_IDX = [i for i, word in enumerate(lines) if word.startswith("DB_DIR")][0]
    lines[_DB_DIR_IDX] = "DB_DIR = \"{}/brains\"".format(working_dir)

with open(util_file, "w") as f:
    f.write('\n'.join(lines))
print('[*] DB_DIR changed -> "{}"'.format(working_dir))
EOF
echo "[*] reddit-karma-farming-bot installed!"
echo "[!] Please setup your credentials in reddit.py"
echo "[:] use 'nano reddit.py' -> fill in the required credentials"
echo "[:] run the bot using 'python2 run.py'"
