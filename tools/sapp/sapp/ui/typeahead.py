# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from typing import List, NamedTuple

import graphene
from sqlalchemy.orm import Session

from ..models import Issue, IssueInstance, SharedText, SharedTextKind


class CodeType(graphene.ObjectType):
    code = graphene.Int()


class Code(NamedTuple):
    code: int


def all_codes(session: Session) -> List[Code]:
    return session.query(Issue.code.distinct().label("code")).all()


class PathType(graphene.ObjectType):
    path = graphene.String()


class Path(NamedTuple):
    path: str


def all_paths(session: Session) -> List[Path]:
    return (
        # pyre-fixme[16]: `str` has no attribute `label`.
        session.query(IssueInstance, SharedText.contents.label("path"))
        .join(SharedText, SharedText.id == IssueInstance.filename_id)
        .group_by(SharedText)
        .all()
    )


class CallableType(graphene.ObjectType):
    callable = graphene.String()


class Callable(NamedTuple):
    callable: str


def all_callables(session: Session) -> List[Callable]:
    return (
        # pyre-fixme[16]: `str` has no attribute `label`.
        session.query(IssueInstance, SharedText.contents.label("callable"))
        .join(SharedText, SharedText.id == IssueInstance.callable_id)
        .group_by(SharedText)
        .all()
    )


class Feature(graphene.ObjectType):
    feature = graphene.String()


def all_features(session: Session) -> List[Feature]:
    return (
        # pyre-fixme[16]: `str` has no attribute `label`.
        session.query(SharedText, SharedText.contents.label("feature"))
        .filter(SharedText.kind == SharedTextKind.FEATURE)
        .all()
    )
