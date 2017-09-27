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

if [ ! -d $VENV_DIR ]; then
  python3.6 -m virtualenv $VENV_DIR
fi

source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install -r "$ROOT_PATH/requirements.txt"
pip install -r "$ROOT_PATH/requirements-dev.txt"

pre-commit install

cd "$ROOT_PATH/backend"

NO_DB=0
if [ ! -f "$ROOT_PATH/backend/db.sqlite3" ]; then
    NO_DB=1
fi

python manage.py makemigrations db_models
python manage.py migrate

if (($NO_DB)); then
    COMMAND="
from django.contrib.auth.models import User
from db_models.models.profile import Profile

user = User.objects.create_superuser('admin@gymapp.life', 'admin@admin@gymapp.life', 'password')
user.first_name = 'Gymapp'
user.last_name = 'Life'
user.save()
Profile.objects.create(user=user)
"
    echo "$COMMAND"
    echo "$COMMAND" | python manage.py shell
fi
