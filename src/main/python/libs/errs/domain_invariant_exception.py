from libs.errs.error import Error


class DomainInvariantError[**P](Exception):
    def __init__(self, msg: Error, *args: P.args, **kwargs: P.kwargs) -> None:
        super().__init__(f"Domain invariant violated: {msg}", *args, **kwargs)
