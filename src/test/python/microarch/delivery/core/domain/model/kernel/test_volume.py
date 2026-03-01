import pytest
from microarch.delivery.core.domain.model.kernel.volume import Volume


class TestVolume:
    @pytest.mark.parametrize("value", [1, 2])
    def test_success_create(self, value: int) -> None:
        result = Volume.create(value=value)

        assert result.is_success
        assert result.value.value == value

    @pytest.mark.parametrize("value", [-1, 0])
    def test_failure_create(self, value: int) -> None:
        result = Volume.create(value=value)

        assert result.is_failure
        assert result.error.code == "value.must.be.greater.or.equal"
