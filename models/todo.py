from models import Model


class Todo(Model):
    def __init__(self, form):
        super().__init__(form)
        self.content = form['content']
        self.create_time = form['create_time']
        self.update_time = form['update_time']

    @classmethod
    def update(cls, form):
        form['id'] = int(form['id'])

        m = cls.find_by(id=form['id'])
        form.pop('id')

        m.content = form['content']
        m.update_time = form['update_time']
        m.save()
        return m
