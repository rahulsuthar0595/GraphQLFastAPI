import logging
from typing import Any

import strawberry
from graphql import DirectiveLocation

logging.basicConfig(level=logging.INFO)


@strawberry.directive(
    locations=[DirectiveLocation.FIELD],
    description="Make String to Title Case",
    name="toTitleCase"
)
def to_upper_case(value: str) -> Any | str:
    if isinstance(value, str):
        return value.upper()
    return value


directives = [to_upper_case,]
