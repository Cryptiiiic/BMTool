import os


def file_io(path: str, binary: bool, write: bool, callback) -> bool:
    if len(path) < 1:
        return False
    if not write and not os.path.exists(path):
        return False
    if write:
        openType = "w"
    else:
        openType = "a"
    if binary:
        openType = f"{openType}b"

    if not write:
        openType = f"{openType}+"
    with open(path, openType) as file:
        return callback(file)
