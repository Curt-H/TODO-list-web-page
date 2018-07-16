import time

from models.todo import Todo
from request import Request
from route import generate_header
from util import log


def api_todo_all(request):
    r = request

    ms = Todo.all()
    body = [m.json() for m in ms]
    header = generate_header(len(body), content_type='application/json')

    response = header + body
    return response


def api_todo_add(request):
    r = request

    form = r.json()
    form['create_time'] = time.time()
    form['update_time'] = form['create_time']
    m = Todo.new(form)
    log(f'Form is:\n {form}')

    body = m.json()
    header = generate_header(len(body), content_type='application/json')
    response = header + body
    return response


def route_api_todo():
    route_dict = {
        '/api/todo/add': api_todo_add,
        '/api/todo/all': api_todo_all,
    }
    return route_dict
