import json

class JsonUndefined:

    def __str__(self):
        return 'undefined'

    def __init__(self):
        if JsonUndefined.INSTANCE:
            raise Error('Instance already initalized')
        JsonUndefined.INSTANCE = self

    INSTANCE = None

JsonUndefined()

class Json(dict):
    """Dict that can use Javascript like JSON"""

    undefined = JsonUndefined.INSTANCE

    def __setattr__(self, name, value):
        if value == Json.undefined:
            del self[name]
        else:
            self[name] = value

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            return Json.undefined

    def __delattr__(self, name):
        del self[name]

    def __str__(self):
        return json.dumps(self, indent=2)


if __name__ == '__main__':
    x = Json(a=3)
    x.b = 'c'
    assert x['b'] == 'c'
    print(x)
    x.truc = None
    del x.a
    print(x)
    print('a' in x)
    print('b' in x)
    print(x.a)
    x.truc = Json.undefined
    print(x)