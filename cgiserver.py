import cgi
import BaseHTTPServer,CGIHTTPServer

BaseHTTPServer.HTTPServer(('0.0.0.0', 8080), CGIHTTPServer.CGIHTTPRequestHandler).serve_forever()
