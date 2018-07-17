import json

from util import log


def load(fname):
    file = fname
    with open(file, 'r', encoding='utf-8') as f:
        d = json.load(f)
    return d


def save(fname, data):
    d = data
    file = fname

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)


class Model(object):

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        path = f'data/{cls.__name__}.txt'
        return path

    @classmethod
    def all(cls):
        models = load(cls.db_path())
        ms = [cls(m) for m in models]
        return ms

    def save(self):
        models = self.all()

        if self.id is None:
            if len(models) == 0:
                self.id = 0
            else:
                self.id = models[-1].id + 1
            models.append(self)
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        d = [m.__dict__ for m in models]
        save(self.db_path(), d)

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def delete(cls, model_id):
        ms = cls.all()
        for i, m in enumerate(ms):
            if m.id == model_id:
                log(f'Deleting {ms[i]}')
                del ms[i]
                log('Deleting finished')
                break

        d = [m.__dict__ for m in ms]
        save(cls.db_path(), d)

    @classmethod
    def find_by(cls, **kwargs):
        ms = cls.all()

        for m in ms:
            find_it = True
            for k, v in kwargs.items():
                log(m, k, v)
                if not hasattr(m, k) or not getattr(m, k) == v:
                    find_it = False

            if find_it:
                return m

    @classmethod
    def find_all(cls, **kwargs):
        result = list()
        ms = cls.all()

        for m in ms:
            find_it = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    find_it = False

            if find_it:
                result.append(m)
        return result

    def __repr__(self):
        classname = self.__class__.__name__
        class_attr = self.__dict__

        attributes = [f'{k}: {v}' for k, v in class_attr.items()]
        return f'{classname}\n' + '\n'.join(attributes)

    def json(self):
        return self.__dict__


if __name__ == '__main__':
    pass
