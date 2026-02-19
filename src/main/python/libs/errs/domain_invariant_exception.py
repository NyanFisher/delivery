class DomainInvariantError[**P](Exception):
    def __init__(self, msg: str, *args: P.args, **kwargs: P.kwargs) -> None:
        super().__init__(f"Domain invariant violated: {msg}", *args, **kwargs)
