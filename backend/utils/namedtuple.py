from collections import namedtuple


def namedtuple_and_choices_from_kwargs(name, **kwargs):
    return (
        namedtuple(name, sorted(kwargs.keys()))(
            **{k: k for k in kwargs.keys()}
        ),
        list(kwargs.items()),
    )
