''' A set of file io routines to handle input data '''

from typing import Callable, TypeVar

identity = lambda x: x
ReturnValue = TypeVar("ReturnValue")
def read(filename: str,
         func: Callable[[str], ReturnValue] = identity
        ) -> list[ReturnValue]:
    with open(filename) as read_file:
        return [func(l.strip()) for l in read_file]

def read_ints(filename: str) -> list[int]:
    return read(filename, int)
