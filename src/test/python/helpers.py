from microarch.delivery.core.domain.model.kernel.volume import Volume


def create_volume(value: int) -> Volume:
    return Volume.create(value).value
