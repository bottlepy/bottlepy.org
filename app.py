#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import bottle

app = application = bottle.Bottle()

docs_path   = os.path.join(os.path.dirname(__file__), 'docs/')
static_path = os.path.join(os.path.dirname(__file__), 'static/')

@app.get('/')
def index():
    bottle.redirect('/docs/dev/')

@app.get('/docs/<version>/')
@app.get('/docs/<version>/<filename:path>')
def docs(version, filename='index.html'):
    filename = version + '/' + (filename or 'index.html')
    print filename
    return bottle.static_file(filename, root=docs_path)

@app.get('/commit/:hash#[a-zA-Z0-9]+#')
def commit(hash):
    url = 'https://github.com/defnull/bottle/commit/%s'
    bottle.redirect(url % hash.lower())

@app.get('/bottle.py')
def download():
    url = 'https://github.com/defnull/bottle/raw/master/bottle.py'
    bottle.redirect(url)

@app.get('/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root=static_path)

# Start server
if __name__ == '__main__':
	bottle.run(app, debug=True)
