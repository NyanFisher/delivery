import pytest
from microarch.delivery.core.domain.model.kernel.location import Location


class TestLocation:
    @pytest.mark.parametrize(
        ("coords", "expected"),
        [
            ((0, 1), "Value 0 for x is out of range. Min value is 1, max value is 10."),
            ((1, 0), "Value 0 for y is out of range. Min value is 1, max value is 10."),
            ((11, 1), "Value 11 for x is out of range. Min value is 1, max value is 10."),
            ((1, 11), "Value 11 for y is out of range. Min value is 1, max value is 10."),
        ],
    )
    def test_failure_create_location(self, coords: tuple[int, ...], expected: str) -> None:
        sut = Location.create(*coords)

        assert sut.is_failure
        assert expected in sut.error.serialize()

    @pytest.mark.parametrize("coords", [(1, 1), (10, 10), (5, 5)])
    def test_success_create_location(self, coords: tuple[int, ...]) -> None:
        sut = Location.create(*coords)

        assert sut.is_success
        assert sut.value == Location(x=coords[0], y=coords[1])

    @pytest.mark.parametrize(
        ("courier_coords", "home_coords", "expected"),
        [
            ((1, 6), (1, 3), 3),
            ((1, 3), (1, 6), 3),
            ((6, 1), (3, 1), 3),
            ((3, 1), (6, 1), 3),
            ((4, 9), (2, 6), 5),
            ((2, 6), (4, 9), 5),
        ],
    )
    def test_distance_to(self, courier_coords: tuple[int, ...], home_coords: tuple[int, ...], expected: int) -> None:
        courier_location = Location.create(*courier_coords).value
        home_location = Location.create(*home_coords).value

        result = courier_location.distance_to(home_location)

        assert result == expected
