"""
    © Jürgen Schoenemeyer, 25.02.2025 15:45

    src/utils/result.py

    PUBLIC:
     - is_ok(result: Result[T, E]) -> bool:
     - is_err(result: Result[T, E]) -> bool:
     - unwrap_ok(result: Result[T, E]) -> T:
     - unwrap_err(result: Result[T, E]) -> E:
"""
from __future__ import annotations

from typing import Generic, TypeVar

from result import Err, Ok, Result

T = TypeVar("T")
E = TypeVar("E")

def is_ok(result: Result[T, E]) -> bool:
    return isinstance(result, Ok)

def is_err(result: Result[T, E]) -> bool:
    return isinstance(result, Err)

def unwrap_ok(result: Result[T, E]) -> T:
    assert isinstance(result, Ok)  # noqa: S101
    return result.ok()

def unwrap_err(result: Result[T, E]) -> E:
    assert isinstance(result, Err)  # noqa: S101
    return result.err()

class ResultUtils(Generic[T, E]):
    @staticmethod
    def is_ok(result: Result[T, E]) -> bool:
        return isinstance(result, Ok)

    @staticmethod
    def is_err(result: Result[T, E]) -> bool:
        return isinstance(result, Err)

    @staticmethod
    def unwrap_ok(result: Result[T, E]) -> T:
        assert isinstance(result, Ok)  # noqa: S101
        return result.ok()

    @staticmethod
    def unwrap_err(result: Result[T, E]) -> E:
        assert isinstance(result, Err)  # noqa: S101
        return result.err()
