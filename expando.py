import json

class Expando(object):
    """Javascript like extensible object"""

    def __init__(self, *args, **kw):
        self.__dict__.update(kw)

    def __toDict(self):
        d = {}
        for key in dir(self):
            if not key.startswith('_'):
                d[key] = self.__dict__[key]
        return d

    def __str__(self):
        return json.dumps(self.__toDict())


if __name__ == "__main__":
    x = Expando(a=3)
    x.b = "c"
    print(x)
