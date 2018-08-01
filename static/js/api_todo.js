// Todo API
let apiTodoAll = function (callback) {
    let path = '/api/todo/all';
    ajax('GET', path, '', callback)
};

let apiTodoAdd = function (form, callback) {
    let path = '/api/todo/add';
    ajax('POST', path, form, callback)
};

let apiTodoDelete = function (form, callback) {
    let path = '/api/todo/delete';
    ajax('POST', path, form, callback)
};

let apiTodoUpdate = function (form, callback) {
    let path = '/api/todo/update';
    ajax('POST', path, form, callback)
};

let todoTemplate = function (todo) {
    let template = `
    <div class="todo-block pure-u-1-2">
    <div class="todo-cell" data-id="${todo.id}">

        <div class="todo-content">
            <p>${todo.content}</p>
        </div>

        <div class="todo-edit-cell">
            <input class="todo-edit pure-button pure-button-primary" value="EDIT" type="submit">
            <input class="todo-delete pure-button pure-button-primary" value="DELE" type="submit">
        </div>
    </div>
    </div>
    `;
    return template
};

let todoEditTemplate = function (todo) {
    let template = `
    <div class="todo-edit-input">
        <input class="todo-edit-content " value="${todo}">
        <input class="todo-update pure-button pure-button-primary" value="UPDATE" type="submit">
    </div>
    `;
    return template
};

let insertTodo = function (todo) {
    let todoCell = todoTemplate(todo);
    let todolist = e('#id-todo-list');
    todolist.insertAdjacentHTML('beforeend', todoCell)
};

let insertTodoEdit = function (todo, todoCell) {
    let todoEdit = todoEditTemplate(todo);
    todoCell.insertAdjacentHTML('beforeend', todoEdit)
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
        input.value = "";
        apiTodoAdd(form, function (todo) {
            insertTodo(todo)
        })
    })
};

let bindEventTodoDelete = function () {
    let todoList = e('#id-todo-list');
    todoList.addEventListener('click', function (t) {
        self = t.target;
        log('被点击的元素', self);
        log('此元素的Class List', self.classList);

        if (self.classList.contains('todo-delete')) {
            log('点击了删除按钮', self);

            let todoCell = self.closest('.todo-cell');
            let todoId = todoCell.dataset['id'];
            let form = {
                id: todoId,
            };
            log('要被删除的TODO id:', form);

            apiTodoDelete(form, function () {
                todoCell.parentElement.remove()
                alert('删除成功')
            })
        }
    })
};

let bindEventTodoEdit = function () {
    let todoList = e('#id-todo-list');
    todoList.addEventListener('click', function (t) {
        self = t.target;
        log('被点击的元素', self);
        log('此元素的Class List', self.classList);

        if (self.classList.contains('todo-edit')) {
            log('点击了编辑按钮', self);

            let todoCell = self.closest('.todo-cell');
            let content = e('.todo-content', todoCell);

            log(e('.todo-edit-input', content));
            if (e('.todo-edit-input', content) == null) {
                insertTodoEdit(content.innerText, content)
            }
        }
    })
};

let bindEventTodoUpdate = function () {
    let todoList = e('#id-todo-list');
    todoList.addEventListener('click', function (t) {
        self = t.target;
        log('被点击的元素', self);
        log('此元素的Class List', self.classList);

        if (self.classList.contains('todo-update')) {
            log('点击了编辑按钮', self);

            let todoCell = self.closest('.todo-cell');
            let content = e('.todo-content', todoCell);
            let updateContent = e('.todo-edit-content', content);
            let form = {
                id: todoCell.dataset['id'],
                content: updateContent.value
            };
            log('需要更新的数据', form);

            apiTodoUpdate(form, function (todo) {
                let p = e('p', content);
                p.innerText = todo.content;
                updateContent.closest('.todo-edit-input').remove();
                alert('更新完成')
            })
        }
    })
};

let bindEvents = function () {
    bindEventTodoAdd();
    bindEventTodoDelete();
    bindEventTodoEdit();
    bindEventTodoUpdate()
};

let __main = function () {
    loadTodos();
    bindEvents()
};

__main();