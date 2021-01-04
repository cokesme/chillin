#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, request, abort, after_this_request
from urllib.parse import urlparse
import os
import re

'''
ParseResult(scheme='https', netloc='sourcegraph.com', path='/{github,gitlab}/<account>/<repo>', params='', query='', fragment='')
ParseResult(scheme='https', netloc='github.com', path='/<account>/<repo>', params='', query='', fragment='')
ParseResult(scheme='https', netloc='gist.github.com', path='/search.html', params='', query='q=<search>', fragment='')
ParseResult(scheme='https', netloc='elixir.bootlin.com', path='/{linux,<version>}/latest/source', params='', query='', fragment='')
ParseResult(scheme='https', netloc='j00ru.vexillium.org', path='/syscalls/{nt,win32k}/{64,32}/', params='', query='', fragment='')
ParseResult(scheme='https', netloc='security-tracker.debian.org', path='/tracker/source-package/<package-name>', params='', query='', fragment='')
ParseResult(scheme='https', netloc='docs.python.org', path='/{3,2}/search.html', params='', query='q=<search term>', fragment='')
ParseResult(scheme='https', netloc='doc.sagemath.org', path='/html/en/reference/search.html', params='', query='q=<search term>', fragment='')
ParseResult(scheme='https', netloc='api.binary.ninja', path='/search.html', params='', query='q=<search term>', fragment='')
'''
class Site():
    def __init__(self, route, args, redir, path, url):
        self.route = route
        self.args = args
        self.redir_fmt = redir
        self.path = path
        self.url = url 

    def redir(self, args):
        # explode the args which will match the length of the format specifiers
        return self.redir_fmt.format(*args)

def build_site(site):
    # Parse required choice args {} ugh embedding <> in {}
    # Parse optional args need to build a real route <>
    required = re.compile("\{([^}]+)\}")
    optional = re.compile("<([^>]+)>")
    req_iter = required.finditer(site)
    op_iter = optional.finditer(site)
    # first get value names
    # TODO get required working 
    for req in req_iter:
        options = req.split(',')

    # make the flask route path from the domain
    domain = urlparse(site).netloc
    if ':' in domain:
        domain = domain.split(":")[0]

    flask_path = '/'+ ''.join(domain.split('.'))

    # get the args because we need to pass their names to the template engine
    args = list(map(lambda x: x.group(1), op_iter))
    print(args)
    # route need to build the flask params with <>
    # XXX just using the optional args right now to test
    # XXX because we are using forms, we have query string as the get request
    # YOU dont need to pull this out here you use  request.args to get query args
    route = flask_path #+ '?' + '&'.join(map(lambda x: x+'='+'<'+x+'>', args))
    print(route)

    # split all matches, replace with %s for redir url
    #redir = re.split(required+"|"+optional, site)
    # XXX had to remove the capture group for split?
    optional = re.compile("<[^>]+>")
    redir = re.split(optional, site)
    redir = '{}'.join(redir)
    print(redir)

    return Site(route, args, redir, flask_path, domain)
    
def parse_sites():
    sites = None
    try: 
        # We control the sites and their format 
        with open("./sites", "r") as f:
            sites = f.read().split('\n')
    except:
        pass

    built = [build_site(site) for site in filter(lambda x: len(x)>0, sites)]

    # build the route as the key
    sites = {}
    for site in built:
        sites[site.route] = site
    return sites

# View for all of our generated sites
def on_demand():
    # Use the matched url_rule to find the matching site 'route'
    site = app.config['sites'][request.url_rule.endpoint]
    # We only care if they sent less
    try:
        togo = site.redir(list(request.args.values()))
        return redirect(togo, code=302)
    except:
        abort(404)

on_demand.methods = ['GET']

app = Flask(__name__)

@app.route('/')
def src():
    '''
    Render with the other search engines

    {% macro site_form(site) -%}
        <form method=GET action={{site.path}}>
        {{ site.url }}
        {% for i in site.args %}
        /<input type=text name={{ i }}>
        {% endfor %}
        </form>
    {%- endmacro %}
    '''
    @after_this_request
    def no_embed(response):
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    return render_template('./index.html', sites=app.config['sites'].values())

@app.route('/<string:org>/<string:repo>')
def srcgr(org, repo):
    return redirect(f"https://sourcegraph.com/github.com/{org}/{repo}", code=302)

if __name__ == '__main__':
    app.config['sites'] = parse_sites()

    # The keys are the route, values are the site objects
    for site in app.config['sites'].values():
        app.add_url_rule(site.route, site.route, on_demand)

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
