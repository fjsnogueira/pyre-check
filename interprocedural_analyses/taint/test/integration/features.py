# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from builtins import __test_sink, __test_source
from typing import Any, Optional, Tuple


def len(o: Any) -> int:
    ...


def min(x: int, y: str):
    ...


def named(*, named_parameter: int, **kw):
    ...


def tito_via_len(o: Any):
    return len(o)


def tito_via_min_left(o: Any):
    return min(o, "")


def tito_via_min_right(o: Any):
    return min(5, o)


def tito_via_named(o: Any):
    return named(named_parameter=o)


def tito_via_min_or_not(o: Any, b: bool):
    if b:
        return min(o, "abc")
    else:
        return o


def tito_via_constructor(o: Any):
    return int(o)


def optional_scalar(parameter) -> Optional[int]:
    return 0


def tito_via_optional(o: Any):
    return optional_scalar(o)


def issue_via_bool():
    o = __test_source()
    x = bool(o)
    __test_sink(x)


def returns_tainted_object() -> object:
    return __test_source()


def issue_via_equality():
    o = returns_tainted_object()
    matches_tainted = o == "tainted"
    __test_sink(matches_tainted)


def return_tuple_of_bools() -> Tuple[bool, bool]:
    return __test_source(), __test_source()


def issue_from_tuple():
    a, b = return_tuple_of_bools()
    __test_sink(a)


def tito_with_tuple(o: Any, b: bool) -> Tuple[bool, bool]:
    if b:
        return min(o, "abc"), min(o, "abc")
    else:
        return o, o


async def async_tuple_of_bools() -> Tuple[bool, bool]:
    return __test_source(), __test_source()


async def async_issue_bools() -> None:
    x, y = await async_tuple_of_bools()
    __test_sink(x)
