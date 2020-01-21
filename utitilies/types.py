import enum


class StatusType(enum.Enum):
    active = "active"
    inactive = "inactive"
    blocked = "blocked"
    archived = "archived"
    deleted = "deleted"


class GenderType(enum.Enum):
    male = "male"
    female = "female"
