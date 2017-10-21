#!/usr/bin/env bash

set -e

# https://stackoverflow.com/a/630387
MY_PATH="`dirname \"$0\"`"                         # relative
ROOT_PATH="`( cd \"$MY_PATH\" && cd .. && pwd )`"  # absolutized and normalized
if [ -z "$ROOT_PATH" ] ; then
  # error; for some reason, the path is not accessible
  # to the script (e.g. permissions re-evaled after suid)
  exit 1  # fail
fi

VENV_DIR="$ROOT_PATH/venv"

source "$ROOT_PATH/venv/bin/activate"

cd "$ROOT_PATH/backend"

python manage.py shell_plus
