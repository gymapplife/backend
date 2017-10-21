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

user = User.objects.create_superuser('admin@gymapp.life', 'admin@gymapp.life', 'password')

Profile.objects.create(pk=1, goal='CARDIO', experience='NEW', weight=75, height=182)
Profile.objects.create(pk=2, goal='STRENGTH_TRAINING', experience='BEGINNER', weight=40, height=120)
"
  echo "$COMMAND"
  echo "$COMMAND" | python manage.py shell
  python manage.py loaddata db_models/fixtures/exercise.json
  python manage.py loaddata db_models/fixtures/day_of_week.json
  python manage.py loaddata db_models/fixtures/stronglifts_5x5.json
  python manage.py loaddata db_models/fixtures/531_beginner.json
fi
