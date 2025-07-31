import re as _re
from unicodedata import normalize as _normalize


_TASK_ID_SUB_COMPILE = (
    (_re.compile(r"\W").sub, "_"),
    (_re.compile(r"_{2,}").sub, "_"),
)


def task_id(id: str):
    for sub, char in _TASK_ID_SUB_COMPILE:
        id = sub(char, id)

    return id.strip("_").upper()


def pascal_case_to_snake_case(text: str):
    _text = _re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)

    _text = _re.sub(r"(?<=[a-z])(?=[A-Z])", r"_", _text)

    _text = _re.sub(r"\.", r"__", _text)
    _text = _re.sub(r"\W", r"_", _text)
    _text = _re.sub(r"_{3,}", r"__", _text)
    _text = (
        _normalize("NFD", _text)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .lower()
    )

    return _text
