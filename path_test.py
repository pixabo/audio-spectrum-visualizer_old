#!/usr/bin/python
import sys
import os
print "Content-type: text/html\n"
print "<html><body>"
print "<h2>Python Environment Info:</h2>"
print "<p>Python Version:", sys.version, "</p>"
print "<p>Python Path:", sys.path, "</p>"
print "<p>Current Directory:", os.getcwd(), "</p>"
print "</body></html>"
