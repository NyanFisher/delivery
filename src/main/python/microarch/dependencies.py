from microarch.delivery.core.domain.services.order_dispatcher import IOrderDispatcher, OrderDispatcher


async def provide_order_dispatcher() -> IOrderDispatcher:
    return OrderDispatcher()
