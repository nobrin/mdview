#!/usr/bin/python
# -*- coding: utf-8 -*-
# Processing server for Markdown format
from __future__ import with_statement
import os, sys
from os.path import join as pjoin
from rayphe import *
from subprocess import *

if len(sys.argv) >= 2: DOC_DIR = sys.argv[1]
else: DOC_DIR = pjoin(os.path.dirname(__file__), "doc")
sys.stderr.write("Using %s as DOC_DIR\n" % DOC_DIR)
if not os.path.isdir(DOC_DIR):
    sys.stderr.write("Oops %s does not exist! Abort.\n")
    sys.exit(-1)

APP_DIR = os.path.dirname(__file__)

app = Application()
app.config([
    ("debug", True),
    ("renderer", {
        "template_dir":os.path.join(APP_DIR, "templates"),
        "cache_dir":pjoin(APP_DIR, "templates", "cache"),
    }),
    ("StaticFileExtension", {"url":"static/", "path":pjoin(APP_DIR, "static")}),
])

with app.filter():
    @app.get("")
    def index():
        files = os.listdir(DOC_DIR)
        return app.renderer.listdir({"files":files})

    @app.get(r"(unicode:\w+\.md$)")
    def view(name):
        filename = pjoin(DOC_DIR, name)
        body = Popen(["markdown", filename], stdout=PIPE).communicate()[0]
        return app.renderer.viewer({"name":name, "body":body.decode("utf8")})

app.run_simple(port=7000, host="0.0.0.0")

