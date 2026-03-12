import typing
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from microarch.delivery.core.domain.model.courier import Courier, StoragePlace
from microarch.delivery.core.domain.model.kernel.location import Location
from microarch.delivery.core.domain.model.kernel.speed import Speed
from microarch.delivery.core.domain.model.kernel.volume import Volume
from microarch.delivery.core.domain.model.order import Order, OrderStatusEnum


class BaseModel(DeclarativeBase): ...


class OrderModel(BaseModel):
    __tablename__ = "order"

    id_: Mapped[uuid.UUID] = mapped_column("id", primary_key=True)
    status: Mapped[OrderStatusEnum]
    volume: Mapped[int]
    location_x: Mapped[int]
    location_y: Mapped[int]

    courier_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("courier.id"))

    def to_entity(self) -> Order:
        return Order(
            order_id=self.id_,
            location=Location(self.location_x, self.location_y),
            volume=Volume(self.volume),
            status=self.status,
            courier_id=self.courier_id,
        )

    @classmethod
    def from_entity(cls, entity: Order) -> typing.Self:
        return cls(
            id_=entity.id_,
            status=entity.status,
            volume=entity.volume.value,
            location_x=entity.location.x,
            location_y=entity.location.y,
            courier_id=entity.courier_id,
        )


class StoragePlaceModel(BaseModel):
    __tablename__ = "storage_place"

    id_: Mapped[uuid.UUID] = mapped_column("id", primary_key=True)
    name: Mapped[str]
    volume: Mapped[int]

    order_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("order.id"))
    courier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courier.id"))
    courier: Mapped["CourierModel"] = relationship(back_populates="storage_places")

    def to_entity(self) -> StoragePlace:
        return StoragePlace(
            id_=self.id_,
            name=self.name,
            total_volume=Volume(self.volume),
            order_id=self.order_id,
        )

    @classmethod
    def from_entity(cls, entity: StoragePlace) -> typing.Self:
        return cls(id_=entity.id_, name=entity.name, volume=entity.total_volume.value, order_id=entity.order_id)


class CourierModel(BaseModel):
    __tablename__ = "courier"

    id_: Mapped[uuid.UUID] = mapped_column("id", primary_key=True)
    name: Mapped[str]
    speed: Mapped[int]
    location_x: Mapped[int]
    location_y: Mapped[int]

    storage_places: Mapped[list["StoragePlaceModel"]] = relationship(back_populates="courier", lazy="selectin")

    def to_entity(self) -> Courier:
        return Courier(
            id_=self.id_,
            name=self.name,
            speed=Speed(self.speed),
            location=Location(self.location_x, self.location_y),
            storage_places=[storage_place.to_entity() for storage_place in self.storage_places],
        )

    @classmethod
    def from_entity(cls, entity: Courier) -> typing.Self:
        return cls(
            id_=entity.id_,
            name=entity.name,
            speed=entity.speed.value,
            location_x=entity.location.x,
            location_y=entity.location.y,
            storage_places=[StoragePlaceModel.from_entity(storage_place) for storage_place in entity.storage_places],
        )
