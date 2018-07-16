import time

from models.todo import Todo
from route import json_response
from util import log


def api_todo_all(request):
    ms = Todo.all()
    data = [m.json() for m in ms]

    return json_response(data).encode()


def api_todo_add(request):
    r = request

    form = r.json()
    log('JSON form', form)

    form['create_time'] = time.time()
    form['update_time'] = form['create_time']
    m = Todo.new(form)
    log(f'Form is:\n {form}')

    return json_response(m.json()).encode()


def route_api_todo():
    route_dict = {
        '/api/todo/add': api_todo_add,
        '/api/todo/all': api_todo_all,
    }
    return route_dict
