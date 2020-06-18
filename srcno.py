#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def src():
    return render_template('index.html')

@app.route('/<string:org>/<string:repo>')
def srcgr(org, repo):
    return redirect(f"https://sourcegraph.com/github.com/{org}/{repo}", code=302)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)