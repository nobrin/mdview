#!/usr/bin/python
import re
fh = open("github.css", "r")
buf = fh.read()
fh.close()
s = re.sub(r"}", "}\n", buf)
print s

