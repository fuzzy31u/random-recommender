import cgi
import BaseHTTPServer,CGIHTTPServer

BaseHTTPServer.HTTPServer(('127.0.0.1', 80), CGIHTTPServer.CGIHTTPRequestHandler ).serve_forever()
