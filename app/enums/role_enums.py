from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


RoleFilterEnum = Enum(
    "RoleFilterEnum", {"ALL": "all", **{r.name: r.value for r in RoleEnum}}, type=str
)
