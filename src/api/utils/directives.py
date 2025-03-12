from typing import Any

import strawberry
from graphql import DirectiveLocation


@strawberry.directive(
    locations=[DirectiveLocation.FIELD],
    description="Make String to Title Case"
)
def to_title_case(value: Any) -> Any | str:
    if isinstance(value, str):
        return value.title()
    return value