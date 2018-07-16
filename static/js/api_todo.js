// Todo API
let apiTodoAll = function (callback) {
    let path = '/api/todo/all';
    ajax('GET', path, '', callback)
};

let apiTodoAdd = function (form, callback) {
    let path = 'api/todo/add';
    ajax('POST', path, form, callback)
};

let todoTemplate = function (todo) {
    let temp = `
    <div class="pure-u-1-1">
    <div class="todo-cell">

        <div class="todo-content">
            <p>${todo.content}</p>
        </div>

        <div class="todo-edit">
            <input class="todo-edit pure-button pure-button-primary" value="EDIT" type="submit">
            <input class="todo-delete pure-button pure-button-primary" value="DELE" type="submit">
        </div>
    </div>
    </div>
    `;
    return temp
};

let insertTodo = function (todo) {
    let todoCell = todoTemplate(todo);
    let todolist = e('#id-todo-list');
    todolist.insertAdjacentHTML('beforeend', todoCell)
};

let loadTodos = function () {
    apiTodoAll(function (todos) {
        log('load all todos type', typeof(todos));
        log('load all todos', todos);
        for (let i = 0; i < todos.length; i++) {
            let todo = todos[i];
            log('Todo object', typeof(todo));
            insertTodo(todo)
        }
    })

};

let bindEventTodoAdd = function () {
    let submit = e('#id-todo-submit');
    submit.addEventListener('click', function (t) {
        let self = t.target;
        log('被点击的对象是', self);

        let input = e('#id-todo-input');
        let content = input.value;
        log('输入的数据是', content);

        let form = {
            content: content,
        };
        log('表单数据:', form);
        apiTodoAdd(form, function (todo) {
            insertTodo(todo)
        })
    })
};

let bindEvents = function () {
    bindEventTodoAdd()
};

let __main = function () {
    loadTodos();
    bindEvents()
};

__main();