from returns.result import Failure, Result, Success

from pyecm import soem


class AdapterNotFoundError(Exception):
    pass


def validate_network_adapter_name(adapter_name: str) -> Result[str, AdapterNotFoundError]:
    available_adapters = [adapter.name for adapter in soem.ec_find_adapters()]
    if adapter_name not in available_adapters:
        return Failure(
            AdapterNotFoundError(
                f"Adapter {adapter_name} not in available adapters: {available_adapters}"
            )
        )
    return Success(adapter_name)
