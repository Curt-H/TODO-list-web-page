import _thread
import urllib.parse
from util import log
from socket import socket
from route.public import route_public


class Request(object):
    def __init__(self, request):
        """
        :param request: receieved from server, string and cannot be null
        """
        # Initialize the origin data
        self.method = ''
        self.path = ''
        self.args = dict()
        self.form = dict()

        # Dealing with the request
        self.raw_data = request
        self.header, self.body = request.split('\r\n\r\n')
        self.analyse_header()

    def analyse_header(self):
        request_line = self.header.split('\r\n')[0]
        request_line_element = request_line.split(' ')

        self.method = request_line_element[0]
        path_with_args = request_line_element[1]

        self.analyse_const(path_with_args)

    def analyse_const(self, path_with_args):
        """
        :param path_with_args: path like this '/index?foo=bar'
        :return: None
        """
        self.path = path_with_args
        if self.method == 'GET' and path_with_args.find('?') > 0:
            self.path, args_str = path_with_args.split('?')
            args_str = urllib.parse.unquote_plus(args_str)

            for a in args_str.split('&'):
                k, v = a.split('=')
                self.args[k] = v
        elif self.method == 'POST':
            self.path = path_with_args
            if self.body != '':
                form_list = self.body.split('&')
                for a in form_list:
                    k, v = a.split('=')
                    self.form[k] = v


def recieve_request(connection):
    request = b''
    buffer_size = 1024
    # start to read the request
    log('Recieving request...')
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            log('All recieved', request)
            return request.decode(encoding='utf-8')


def make_response(request):
    r = request

    response = route_public(r.path)(r)
    log(response)
    return response


def process_connection(connection):
    with connection:
        request = recieve_request(connection)

        # Chrome may send null request to keep connection alive, it may make programme crashed
        # So here we need to make sure if request is null
        if len(request) == 0:
            log('收到空请求')
        else:
            log(f'Raw request (length:{len(request)}):\n{request}')
            r = Request(request)

            response = make_response(r)
            log(response)
            connection.sendall(response)


def app(host, port):
    with socket() as s:
        # bind host and port and listen
        s.bind((host, port))
        s.listen()
        log(f'Start listening @ http://{host}:{port}\nYou can access it at http://localhost')

        while True:
            # Accept the client connection
            client, address = s.accept()
            log(f'Connected by ({address})')
            _thread.start_new_thread(process_connection, (client,))


if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 80,
    }

    app(**config)
