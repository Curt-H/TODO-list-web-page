import _thread

from request import Request
from route.api_todo import route_api_todo
from util import log
from socket import socket
from route.public import route_public, error


def route_dict():
    r = dict()
    r.update(route_public())
    r.update(route_api_todo())
    return r


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

    route = route_dict().get(r.path, error)
    response = route(r)

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
