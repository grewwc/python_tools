def get_public_attrs(cls):
    return [name for name in dir(cls)
            if not name.startswith('_')]
