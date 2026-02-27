import uuid

import pytest
from libs.errs.guard import Guard
from microarch.delivery.core.domain.model.courier.storage_place import StoragePlace
from pytest_mock import MockerFixture

STORAGE_PLACE_UUID = uuid.uuid4()


class TestStoragePlace:
    @pytest.fixture
    def sut(self) -> StoragePlace:
        return StoragePlace.create(name="backpack", total_volume=20).value

    def test_equal(self, mocker: MockerFixture) -> None:
        mock_uuid4 = mocker.patch("microarch.delivery.core.domain.model.courier.storage_place.uuid.uuid4")
        mock_uuid4.return_value = STORAGE_PLACE_UUID
        storage_1 = StoragePlace.create(name="backpack", total_volume=20).value
        storage_2 = StoragePlace.create(name="bicycle", total_volume=30).value

        assert storage_1 == storage_2
        assert storage_1.id_ == storage_2.id_

    def test_not_equal(self) -> None:
        storage_1 = StoragePlace.create(name="backpack", total_volume=20).value
        storage_2 = StoragePlace.create(name="bicycle", total_volume=30).value

        assert storage_1 != storage_2
        assert storage_1.id_ != storage_2.id_

    @pytest.mark.parametrize(
        ("name", "total_volume", "expected"),
        [("", 20, "value.is.required"), ("backpack", 0, "value.must.be.greater.or.equal")],
    )
    def test_failure_create_storage_place(self, name: str, total_volume: int, expected: str) -> None:
        result = StoragePlace.create(name=name, total_volume=total_volume)

        assert result.is_failure
        assert expected in result.error.serialize()

    def test_success_create_storage_place(self) -> None:
        result = StoragePlace.create(name="backpack", total_volume=20)

        assert result.is_success
        assert result.value.id_ is not None
        assert result.value.name == "backpack"
        assert result.value.total_volume == 20

    @pytest.mark.parametrize(("volume", "expected"), [(10, True), (25, False)])
    def test_can_store(self, volume: int, expected: bool, sut: StoragePlace) -> None:
        assert sut.can_store(volume) is expected

    def test_store(self, sut: StoragePlace) -> None:
        result = sut.store(STORAGE_PLACE_UUID, 10)

        assert result.is_success
        assert sut.order_id is STORAGE_PLACE_UUID

    def test_failure_store_if_volume_exceeds_total_volume(self, sut: StoragePlace) -> None:
        result = sut.store(STORAGE_PLACE_UUID, 25)

        assert result.is_failure
        assert result.error.code == "value.is.out.of.range"
        assert sut.order_id is None

    @pytest.mark.parametrize("volume", [-1, 0])
    def test_failure_store_if_unacceptable_volume(self, volume: int, sut: StoragePlace) -> None:
        result = sut.store(STORAGE_PLACE_UUID, volume)

        assert result.is_failure
        assert result.error.code == "value.is.out.of.range"
        assert sut.order_id is None

    def test_failure_store_if_already_contains_another_order(self, sut: StoragePlace) -> None:
        sut.store(STORAGE_PLACE_UUID, 19)

        result = sut.store(uuid.uuid4(), 26)

        assert result.is_failure
        assert result.error.code == "already.contains.another.order"
        assert sut.order_id == STORAGE_PLACE_UUID

    def test_failure_store_if_order_id_is_empty_uuid(self, sut: StoragePlace) -> None:
        result = sut.store(Guard.EMPTY_UUID, 20)

        assert result.is_failure
        assert result.error.code == "value.is.required"
        assert sut.order_id is None

    def test_clear(self, sut: StoragePlace) -> None:
        sut.store(STORAGE_PLACE_UUID, 10)

        result = sut.clear(STORAGE_PLACE_UUID)

        assert result.is_success
        assert sut.order_id is None

    def test_failure_clear_if_there_is_no_order_id_in_the_storage_place(self, sut: StoragePlace) -> None:
        result = sut.clear(STORAGE_PLACE_UUID)

        assert result.is_failure
        assert result.error.code == "order.id.does.not.match"
        assert sut.order_id is None

    def test_failure_clear_if_order_id_is_empty_uuid(self, sut: StoragePlace) -> None:
        result = sut.clear(Guard.EMPTY_UUID)

        assert result.is_failure
        assert result.error.code == "value.is.required"
        assert sut.order_id is None

    def test_failure_clear_if_order_id_doesnt_match(self, sut: StoragePlace) -> None:
        sut.store(STORAGE_PLACE_UUID, 10)

        result = sut.clear(uuid.uuid4())

        assert result.is_failure
        assert "order.id.does.not.match" in result.error.serialize()
        assert sut.order_id == STORAGE_PLACE_UUID

    def test_is_not_occupied(self, sut: StoragePlace) -> None:
        assert sut.is_occupied is False

    def test_is_occupied(self, sut: StoragePlace) -> None:
        sut.store(STORAGE_PLACE_UUID, 10)

        assert sut.is_occupied is True
