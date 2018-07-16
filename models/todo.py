from models import Model


class Todo(Model):
    def __init__(self, form):
        super().__init__(form)
        self.content = form['content']
        self.create_time = form['create_time']
        self.update_time = form['update_time']
