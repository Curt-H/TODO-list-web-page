from route import generate_header
from template import Template
from util import log


def index(request):
    r = request
    body = Template.render('index.html', r=r)
    header = generate_header(len(body))

    response = header + body
    return response.encode()


def image(request):
    r = request
    # 获取文件的文件名, 后缀名和路径
    filename = r.args.get('f', 'none.png')
    file_type = filename.split('.')[-1]
    file = f'static/{filename}'
    log(f'GET file info\nname:{filename}\ntype:{file_type}\npath:{file}')

    with open(file, 'rb') as f:
        body = f.read()
    header = generate_header(len(body), content_type=f'img/{file_type}')

    response = header.encode() + body
    return response


def css(request):
    r = request
    # 获取文件的文件名和路径
    filename = r.args.get('f', 'none.png')
    file = f'static/css/{filename}'
    log(f'GET file info\nname:{filename}\ntype:css\npath:{file}')

    with open(file, 'r') as f:
        body = f.read()
    header = generate_header(len(body), content_type=f'text/css')

    response = header + body
    return response.encode()


def error(request):
    r = request
    body = Template.render('error.html', r=r)
    header = generate_header(len(body), 404)

    response = header + body
    return response.encode()


def route_public(path):
    route_dict = {
        '/': index,
        '/static': image,
        '/static/css': css,
    }
    return route_dict.get(path, error)
