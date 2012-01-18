#!/usr/bin/python
# -*- coding: utf-8 -*-
# Processing server for Markdown format
from __future__ import with_statement
import os
from os.path import join as pjoin
from rayphe import *
from subprocess import *

APP_DIR = os.path.dirname(__file__)
DOC_DIR = pjoin(os.path.dirname(__file__), "doc")

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
        return app.renderer.viewer({"name":name, "body":body})

app.run_simple(port=7000, host="0.0.0.0")

