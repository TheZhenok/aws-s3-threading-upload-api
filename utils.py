import os


def get_environ_variable(key: str) -> str:
    try:
        return os.environ[key]
    except KeyError:
        raise KeyError(
            f'Key {key} not found in environ!'
        )