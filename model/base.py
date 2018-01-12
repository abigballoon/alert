from model.db import client

def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})


class EmptyResult(object):
    pass

class Query(object):
    def __init__(self, query={}):
        self.query = query

    def update(self, query):
        self.query.update(query)

class QueryResult(object):
    def __init__(self, model, query=None):
        self._model = model
        if not query:
            query = {}
        self._query = Query(query)
        self._result = EmptyResult

    @property
    def result(self):
        if self._result == EmptyResult:
            self.execute()
        return self._result

    def execute(self):
        self._result = [
            self._model(item) for item in self._model._meta.collection.find(self._query.query)
        ]

    def filter(self, **kwargs):
        self._query.update(kwargs)
        return self

    def get(self, **kwargs):
        self._query.update(kwargs)
        result = self.result
        result_length = len(result)
        if not result_length:
            raise self._model.DoesNotExist(self._query.query)
        elif result_length > 1:
            raise self._model.MoreThanOneResult(result_length)
        else:
            return result[0]


class _meta(object):
    def __init__(self, *args, **kwargs):
        self.collection = None


class Base(type):
    fields = []
    mongo = client

    def __new__(cls, name, bases, attrs):
        super_new = super(Base, cls).__new__

        parents = [b for b in bases if isinstance(b, Base)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        new_class = super_new(cls, name, bases, attrs)

        if 'Meta' not in attrs:
            return new_class
        Meta = attrs['Meta']
        db = Meta.db
        collection = Meta.collection
        meta = _meta()
        meta.collection = cls.mongo[db][collection]
        new_class._meta = meta
        return new_class

    def add_to_class(cls, attr, val):
        setattr(cls, attr, val)

class Model(with_metaclass(Base)):
    def __init__(self, data):
        self._objectid = None
        self._dict = data
        for attr in self.fields + ['_id', ]:
            setattr(self, attr, data.get(attr, None))

    @property
    def dictdata(self):
        result = {}
        for field in self.fields + ['_id', ]:
            result[field] = getattr(self, field, None)
        return result

    @classmethod
    def get(cls, **kwargs):
        query = QueryResult(cls, kwargs)
        return query.get()

    @classmethod
    def create(cls, **kwargs):
        cls._meta.collection.insert_one(kwargs)

    @classmethod
    def filter(self, **kwargs):
        query = QueryResult(self, **kwargs)
        return query.filter(**kwargs)

    def save(self):
        self._meta.collection.insert_one(self.dictdata)