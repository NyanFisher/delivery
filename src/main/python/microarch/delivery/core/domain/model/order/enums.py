import enum


class OrderStatusEnum(enum.StrEnum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    COMPLETED = "COMPLETED"
