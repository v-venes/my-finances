from typing import TypedDict, Optional, Literal


class Category(TypedDict):
    id: int
    name: str
    color: str
    parent_id: Optional[int]
    group_id: str
    fixed: bool
    essential: bool
    default: bool
    uuid: str
    kind: Literal["expenses", "income"]
    archived: bool
