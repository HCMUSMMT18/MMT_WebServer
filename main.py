import socket
import mimetypes
import os
import logging
import user_data

logging.basicConfig(filename="server.log", filemode='w', level=logging.DEBUG, format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#redirect logging to both file and console output
logging.getLogger().addHandler(logging.StreamHandler())

# TODO: EXTERNAL CONFIG (SERVERNAME, ROOT PATH ....)
# TODO: UI


class TCPServer:
    def __init__(self, host='127.0.0.1', port=80):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        logging.info("Listening at %s", s.getsockname())

        while True:
            conn, addr = s.accept()
            logging.debug("Connected by %s", addr)
            data = conn.recv(1024)
            response = self.handle_request(data)
            self.handle_response(conn, response)
            conn.close()

    def handle_request(self, data):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data

    def handle_response(self, conn, response):
        """Sends data to client.
        Override this in subclass.
        """
        return True


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
        logging.debug("Handling HTTP Request")
        # create an instance of `HTTPRequest`
        if (data != b''):
            request = HTTPRequest(data)
            # now, look at the request method and call the
            # appropriate handler
            handler = getattr(self, 'handle_%s' % request.method)
            logging.debug("Found handler for request: %s", handler)
            response = handler(request)
            return response

    def handle_response(self, conn, response):
        logging.debug("Sending HTTP response")
        if (response != None):
            if (type(response) is not list):
                conn.sendall(response.encode('utf-8'))
            else:
                for each in response:
                    if (type(each) is bytes):
                        conn.sendall(each)
                    else:
                        conn.sendall(each.encode('utf-8'))
        logging.debug("Done sending HTTP response")

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
        logging.debug("Request type: OPTIONS")
        response_line = self.response_line(200)

        extra_headers = {'Allow': 'OPTIONS, GET, POST'}
        response_headers = self.response_headers(extra_headers)
        logging.debug("Headers: %s", extra_headers)

        return "%s%s%s" % (
            response_line,
            response_headers,
            "\r\n"
        )

    def handle_GET(self, request):

        logging.debug("Request type: GET")
        #constructing path to file
        filename = os.getcwd() + "\\html\\"

        logging.debug("Requested resource: %s", request.uri)

        #if a file is specified
        if (request.uri.strip('/') != ''):
            #constructs filename
            filename = filename + request.uri.strip('/')

            #if file is found
            if os.path.exists(filename):
                logging.debug("Found resource at: %s", filename)
                response_line = self.response_line(200)

                # find out a file's MIME type
                # if nothing is found, just send `text/html`
                content_type = mimetypes.guess_type(filename)[0] or 'text/html'
                logging.debug("Content type: %s", content_type)
                extra_headers = {'Content-Type': content_type}

                response_headers = self.response_headers(extra_headers)

                #if content is plain text
                if ('text' in content_type):
                    with open(filename, 'r', encoding='utf-8') as f:
                        response_body = f.read()
                    return "%s%s%s%s" % (response_line,
                                         response_headers,
                                         "\r\n",
                                         response_body
                                         )
                #if content needs to be sent raw
                else:
                    with open(filename, 'rb') as f:
                        response_body = f.read()
                rep = [response_line + response_headers + "\r\n", response_body]
                return rep
            else:
                logging.warning("Resource not found")
                if os.path.exists(os.getcwd() + "\\html\\404.html"):
                    with open(os.getcwd() + "\\html\\404.html", 'r', encoding='utf-8') as f:
                        response_body = f.read()
                else:
                    logging.warning("404 not found")
                    response_body = '<h1>404 Not Found</h1>'
                response_line = self.response_line(404)
                response_headers = self.response_headers()

                return "%s%s%s%s" % (
                    response_line,
                    response_headers,
                    "\r\n",
                    response_body
                )
        else:
            logging.debug("Redirecting to homepage")
            return self.redirect(request, 301, '/index.html')

    def handle_POST(self, request):
        logging.debug("Username: %s | Password: %s", request.username, request.password)
        #if (request.username == username and request.password == password):
        if (user_data.login_check(request.username, request.password) == True):
            logging.debug("Login accepted")
            return self.redirect(request, 303, '/info.html')
        else:
            logging.debug("Login denied")
            return self.redirect(request, 303, '/404.html')

    def redirect(self, request, status_code, url):
        if (status_code < 300 or status_code > 399):
            status_code = 301
        extra_headers = {'Location': url}
        response_line = self.response_line(status_code)
        response_headers = self.response_headers(extra_headers)
        logging.debug("Redirecting to %s with status code %s", url, status_code)
        return "%s%s%s" % (
            response_line,
            response_headers,
            "\r\n"
        )


class HTTPRequest:

    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = '1.1'  # default to HTTP/1.1 if request doesn't provide a version
        self.headers = {}  # a dictionary for headers
        self.POST_types = {'LOGIN': 'parse_LOGIN'}

        # call self.parse method to parse the request data
        self.parse(data)

    def parse_POST(self, lines):
        logging.debug("Parsing POST request")
        info = lines[-1].split('&')
        POST_type = info[-1].split('=')[1]
        logging.debug("POST type: %s", POST_type)
        if (POST_type in self.POST_types):
            logging.debug("Found matching parser for POST type: %s", POST_type)
            parser = getattr(self, self.POST_types[POST_type])
            parser(info)
        else:
            logging.debug("Did not find matching parser for POST type: %s", POST_type)
            pass
        logging.debug("Done parsing POST request")

    def parse_LOGIN(self, info):
        self.username = info[0].split('=')[1]
        self.password = info[1].split('=')[1]

    def parse(self, data):
        logging.debug("Parsing HTTP request")
        if (data != b''):
            lines = data.decode().split('\r\n')

            request_line = lines[0]

            if (request_line.split(' ')[0] == 'POST'):
                self.parse_POST(lines)

            self.parse_request_line(request_line)
        logging.debug("Done parsing HTTP request")

    def parse_request_line(self, request_line):
        words = request_line.split(' ')
        self.method = words[0]
        self.uri = words[1]

        if len(words) > 2:
            self.http_version = words[2]


if __name__ == '__main__':
    server = HTTPServer()
    server.start()
