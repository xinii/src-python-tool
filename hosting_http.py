# -*- coding:utf-8 -*-
from http.server import HTTPServer, SimpleHTTPRequestHandler


class RequestHandler(SimpleHTTPRequestHandler, object):
    def do_GET(self):
        super().do_GET()

    def do_POST(self):
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len).decode('utf-8')
        print(post_body)
        self.do_GET()


if __name__ == '__main__':
    httpd = HTTPServer(("", 4000), RequestHandler)
    httpd.serve_forever()
