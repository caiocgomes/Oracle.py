from functools import wraps
from types import FunctionType

def getQueryString(func, instance, *args, **kwargs):
    """Gets query string from instance.func(*args) and format the 
    resulting string with kwargs, instance.tableAlias and instance.sqlPatterns"""

    strargs = kwargs.copy()

    if hasattr(instance,'tableAlias'):
        strargs.update(instance.tableAlias)

    if hasattr(instance,'sqlPatterns'):
        strargs.update(instance.sqlPatterns)

    callstring = func(instance, *args)
    return callstring.format(**strargs)

def sqlQueryFetchOne(func):
    @wraps(func)
    def call(instance, *args, **kwargs):
        queryString = getQueryString(func, instance, *args, **kwargs)
        return instance.fetchOne(queryString)[0]
    return call

def sqlQuery(func):
    @wraps(func)
    def call(instance, *args, **kwargs):
        queryString = getQueryString(func, instance, *args, **kwargs)
        return instance.query(queryString)
    return call


def dontDecorate(func):
    func.decorate = False
    return func

def isDecorable(attr, value):
    isInstanceMethod = ('__' not in attr) and ('_' not in attr)
    isFunction = isinstance(value, FunctionType)
    isMarkedForDecoration = getattr(value, 'decorate', True)
    return isInstanceMethod and isFunction and isMarkedForDecoration

def whichDecorator(attr):
    if attr.startswith("get"):
        return sqlQueryFetchOne
    elif attr.startswith("query"):
        return sqlQuery
    else:
        raise Exception("No decorator defined for this prefix.")

def decorated(attr, value):
    if isDecorable(attr, value):
        decorator = whichDecorator(attr)
        return decorator(value)
    else:
        return value

def decorateSQL():
    class DecorateSQL(type):
        def __new__(cls, name, bases, dct):
            for attr, value in dct.iteritems():
                dct[attr] = decorated(attr, value)
            return super(DecorateSQL, cls).__new__(cls, name, bases, dct)

        def __setattr__(self, attr, value):
            value = decorated(value)
            super(DecorateSQL, self).__setattr__(attr, value)

    return DecorateSQL
