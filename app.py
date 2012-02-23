#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import functools
import bottle

app = application = bottle.Bottle()


# Permanent redirects (303)

redirects = '''
/page/start     /docs/dev/index.html
/page/docs      /docs/dev/tutorial.html
/page/tutorial  /docs/dev/tutorial_app.html
/api            /docs/dev/
/api/:fname#.*# /docs/dev/%(fname)s
/               /docs/dev/
/docs           /docs/dev/
/docs/          /docs/dev/
/docs/:ver      /docs/%(ver)s/
'''.strip()

def rdcb(target, **vars):
    bottle.redirect(target % vars)

for line in redirects.splitlines():
    url, target = line.split()
    tmp = functools.partial(rdcb, target)
    functools.update_wrapper(tmp, rdcb)
    app.route(url, callback=tmp)

# Static API docs

@app.get('/docs/:version/')
@app.get('/docs/:version/:filename#.+#')
def static(version, filename='index.html'):
    return bottle.static_file(filename, root='./docs/%s/' % version)

# Git commit redirect

@app.get('/commit/:hash#[a-zA-Z0-9]+#')
def commit(hash):
    url = 'https://github.com/defnull/bottle/commit/%s'
    bottle.redirect(url % hash.lower())

# bottle.py redirect

@app.get('/bottle.py')
def download():
    url = 'https://github.com/defnull/bottle/raw/master/bottle.py'
    bottle.redirect(url)

# Other static files

@app.get('/:filename#.+\.(css|js|ico|png|txt|html)#')
def static(filename):
    return bottle.static_file(filename, root='./static/')

# Start server
if __name__ == '__main__':
	bottle.run(app, debug=True)
