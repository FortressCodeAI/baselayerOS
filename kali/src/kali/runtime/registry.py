REGISTRY = {}


def register(name):

    def wrapper(fn):

        REGISTRY[name] = fn

        return fn

    return wrapper


def resolve(name):

    return REGISTRY[name]
