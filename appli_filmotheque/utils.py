import typing


def check_type(object_, type_):
    print(f'type(object_) == type_ : {type(object_) == type_} ;')
    print(f'object_.__class__ == type_ : {object_.__class__ == type_} ;')
    print(f'isinstance(object_, type_) : {isinstance(object_, type_)} ;')

