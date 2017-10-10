# backend

The backend for our SE 464 project.

## Development

* Instructions assume you're using Ubuntu or macOS.

### Branching

Create a topic branch for every separate change you make. Otherwise `pre-commit` will stop you.
For example:

1. Create your feature branch (`git checkout -b dongyuzheng/my-new-feature`)
2. Commit your changes (`git commit -am 'Added some feature'`)
3. Push to the branch (`git push origin dongyuzheng/my-new-feature`)
4. Create new Pull Request

### Prerequisites

These instructions are for Ubuntu.

1. `python3.6`
```bash
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt update
sudo apt install python3.6
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
rm get-pip.py
```
2. `virtualenv`
```bash
sudo pip3.6 install virtualenv
```
3. `make`
```bash
sudo apt install build-essential
```

4. `graphviz` (optional, for visualizing DB tables)
```bash
wget http://graphviz.org/pub/graphviz/stable/ubuntu/ub13.10/x86_64/graphviz_2.38.0-1~saucy_amd64.deb
wget http://graphviz.org/pub/graphviz/stable/ubuntu/ub13.10/x86_64/graphviz-dev_2.38.0-1~saucy_all.deb
sudo dpkg -i graphviz_2.38.0-1~saucy_amd64.deb graphviz-dev_2.38.0-1~saucy_all.deb
sudo apt install -f
rm graphviz_2.38.0-1~saucy_amd64.deb graphviz-dev_2.38.0-1~saucy_all.deb
```

### Environment Variables

```bash
export FB_APP_SECRET='https://developers.facebook.com/apps/457054341361327/dashboard/'
```

### Make commands

1. `make` / `make install`
    * Creates venv and installs dependencies
    * Creates and migrates local database
    * Creates a superuser
2. `make start-dev`
    * Runs the dev server
3. `make clean`
    * Deletes venv
    * Deletes migration files
    * Deletes the local database

### Virtual Environment

You **must** activate the venv every time you want to do stuff with `python` or `pip`!

1. Init venv with `make install`
2. Activate venv: `source venv/bin/activate`
3. Leave venv with `deactivate`

### Debugging

1. Insert `import ipdb; ipdb.set_trace()` into the code
2. Reload the relevant page
3. Debug!

### Testing

1. `make test`

If you add new functionality, please create new tests accordingly.

### Visualizing DB tables

`python manage.py graph_models -g -o ~/db_tables.png db_models`

## Authors

* [Bo Peng](https://github.com/pobeng) (<bopengexpress@gmail.com>)
* [Dongyu (Gary) Zheng](https://github.com/dongyuzheng) (<garydzheng@gmail.com>)
* [Gautam Gupta](https://github.com/GautamGupta) (<gg@gaut.am>)
* [George Gao](https://github.com/celestimon) (<georgegao96@hotmail.com>)
