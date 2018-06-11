import json
from typing import Any

class JsonUndefined:
    def __str__(self):
        return 'undefined'

    def __bool__(self):
        return False

    def __init__(self):
        if JsonUndefined.INSTANCE != None:
            raise Error('Instance already initalized')

    INSTANCE: Any = None

JsonUndefined.INSTANCE = JsonUndefined()

class Json(dict):
    """Dict that can use Javascript like JSON"""

    undefined: JsonUndefined = JsonUndefined.INSTANCE

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

    def __repr__(self):
        return json.dumps(self, indent=2)

    @staticmethod
    def loads(s: str):
        return json.loads(s, object_hook=Json)


if __name__ == '__main__':
    import re

    # Checking is None and Json.undefined have JS boolean semantics
    assert not None
    assert not Json.undefined

    x = Json(a=3)
    x.b = 'c'
    assert 'b' in x
    assert x['b'] == 'c'  # x.b ==> x['b']
    assert re.sub('\s', '', str(x)) == '{"a":3,"b":"c"}'

    x.none = None
    assert x['none'] == None  # None => null

    del x.a
    assert 'a' not in x
    assert x.a == Json.undefined  # missing return Json.undefined
    assert x.never_used == Json.undefined
    assert re.sub('\s', '', str(x)) == '{"b":"c","none":null}'

    x.none = Json.undefined  # setting undefined removes
    assert 'none' not in x
    y = Json.loads(str(x))
    assert x == y
