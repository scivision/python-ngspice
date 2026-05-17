import shutil
import functools


@functools.cache
def get_exe(name: str) -> str:
    exe = shutil.which(name)
    if exe is None:
        raise FileNotFoundError(f"{name} not found in PATH")

    return exe
