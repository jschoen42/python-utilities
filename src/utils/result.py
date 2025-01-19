# from result import Result, Ok, Err
# from typing import TypeVar

# T = TypeVar("T")
# E = TypeVar("E")

# def is_ok(result: Result[T, E]) -> bool:
#     return isinstance(result, Ok)

# def is_err(result: Result[T, E]) -> bool:
#     return isinstance(result, Err)

# def unwrap_ok(result: Result[T, E]) -> T:
#     assert isinstance(result, Ok)
#     return result.ok()

# def unwrap_err(result: Result[T, E]) -> E:
#     assert isinstance(result, Err)
#     return result.err()

from result import Result, Ok, Err
from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E")

class ResultUtils(Generic[T, E]):
    @staticmethod
    def is_ok(result: Result[T, E]) -> bool:
        return isinstance(result, Ok)

    @staticmethod
    def is_err(result: Result[T, E]) -> bool:
        return isinstance(result, Err)

    @staticmethod
    def unwrap_ok(result: Result[T, E]) -> T:
        assert isinstance(result, Ok)
        return result.ok()

    @staticmethod
    def unwrap_err(result: Result[T, E]) -> E:
        assert isinstance(result, Err)
        return result.err()

