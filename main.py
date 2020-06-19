# main.py
import socket
import mimetypes
import os

username = "admin"
password = "admin"


class TCPServer:
    def __init__(self, host='127.0.0.1', port=6789):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(1024)
            response = self.handle_request(data)
            if (response != None):
                conn.sendall(response.encode('utf-8'))
            conn.close()

    def handle_request(self, data):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data


class HTTPServer(TCPServer):
    headers = {
        'Server': 'MMT_18_5',
        'Content-Type': 'text/html',
    }
    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
        303: 'See Other',
        302: 'Found',
        301: 'Moved Permanently'
    }
    def handle_request(self, data):
        # create an instance of `HTTPRequest`
        if (data != b''):
            request = HTTPRequest(data)
            # now, look at the request method and call the
            # appropriate handler
            handler = getattr(self, 'handle_%s' % request.method)

            response = handler(request)

            return response

    def response_line(self, status_code):
        """Returns response line"""
        reason = self.status_codes[status_code]
        return "HTTP/1.1 %s %s\r\n" % (status_code, reason)

    def response_headers(self, extra_headers=None):
        """Returns headers
        The `extra_headers` can be a dict for sending 
        extra headers for the current response
        """
        headers_copy = self.headers.copy()  # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])
        return headers

    def handle_OPTIONS(self, request):
        response_line = self.response_line(200)

        extra_headers = {'Allow': 'OPTIONS, GET, POST'}
        response_headers = self.response_headers(extra_headers)

        blank_line = "\r\n"

        return "%s%s%s" % (
            response_line,
            response_headers,
            blank_line
        )

    def handle_GET(self, request):
        filename = os.getcwd() + "\\html\\"
        if (request.uri.strip('/') != ''):
            filename = filename + request.uri.strip('/')
            if os.path.exists(filename):
                response_line = self.response_line(200)

                # find out a file's MIME type
                # if nothing is found, just send `text/html`
                content_type = mimetypes.guess_type(filename)[0] or 'text/html'

                extra_headers = {'Content-Type': content_type}
                print(extra_headers)

                response_headers = self.response_headers(extra_headers)
                print("Response headers:\n", response_headers)
                if ('text' in content_type):
                    with open(filename, 'r') as f:
                        response_body = f.read()
                    blank_line = "\r\n"
                    return "%s%s%s%s" % (response_line,
                                        response_headers,
                                        blank_line,
                                        response_body
                                        )
                else:
                    with open(filename, 'rb') as f:
                        response_body = f.read()
                print('Response body:', response_body)
                rep = response_line + response_headers + "\r\n" + str(response_body)
                return rep
            else:
                if os.path.exists(os.getcwd() + "\\html\\404.html"):
                    with open(os.getcwd() + "\\html\\404.html", 'r') as f:
                        response_body = f.read()
                else:
                    response_body = '<h1>404 Not Found</h1>'
                response_line = self.response_line(404)
                response_headers = self.response_headers()

                blank_line = "\r\n"

                return "%s%s%s%s" % (
                    response_line,
                    response_headers,
                    blank_line,
                    response_body
                )
        else:
            return self.redirect(request, 301, '/index.html')

    def handle_POST(self, request):
        print("Raw data:", request)
        if (request.username == username and request.password == password):
            return self.redirect(request, 303, '/info.html')
        else:
            return self.redirect(request, 303, '/404.html')

    def redirect(self, request, status_code, url):
        if (status_code < 300 or status_code > 399):
            status_code = 301
        extra_headers = {'Location': url}
        response_line = self.response_line(status_code)
        response_headers = self.response_headers(extra_headers)
        response_body = ""

        blank_line = "\r\n"

        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )


class HTTPRequest:

    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = '1.1'  # default to HTTP/1.1 if request doesn't provide a version
        self.headers = {}  # a dictionary for headers
        self.POST_types = {'Login': 'parse_Login'}

        # call self.parse method to parse the request data
        self.parse(data)

    def parse_POST(self, lines):
        info = lines[-1].split('&')
        POST_type = info[-1].split('=')[1]
        if (POST_type in self.POST_types):
            handler = getattr(self, self.POST_types[POST_type])
            run = handler(info)
        else:
            pass

    def parse_Login(self, info):
        self.username = info[0].split('=')[1]
        self.password = info[1].split('=')[1]

    def parse(self, data):
        print("DATA: ", data)
        if (data != b''):
            lines = data.decode().split('\r\n')

            request_line = lines[0]
            print("REQUEST: ", request_line)

            if (request_line.split(' ')[0] == 'POST'):
                self.parse_POST(lines)

            self.parse_request_line(request_line)

    def parse_request_line(self, request_line):
        words = request_line.split(' ')
        self.method = words[0]
        self.uri = words[1]

        if len(words) > 2:
            self.http_version = words[2]


if __name__ == '__main__':
    server = HTTPServer()
    server.start()
