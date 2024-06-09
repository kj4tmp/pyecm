import logging

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from pyecm.eni import ENI
from pyecm.network_adapters import AdapterNotFoundError, validate_network_adapter_name
from pyecm.soem.soem_ext import SOEM

_logger = logging.getLogger(__name__)


class SubDevice:
    pass


class MainDevice:

    def __init__(self, main_adapter_name: str, eni: ENI, red_adapter_name: str = ""):
        maxgroup = max(len(eni.config.cyclics), 1)
        iomap_size_bytes = self._get_soem_iomap_size_bytes(eni=eni)
        self.soem = SOEM(
            max_subdevices=len(eni.config.subdevices),
            maxgroup=maxgroup,
            iomap_size_bytes=iomap_size_bytes,
            manualstatechange=True,
        )
        self.main_adapter_name = main_adapter_name
        self.red_adapter_name = red_adapter_name
        pass

    def init_verify_network(self) -> Result[int, AdapterNotFoundError]:
        res = validate_network_adapter_name(adapter_name=self.main_adapter_name)
        if not is_successful(res):
            return res

        pass

    @staticmethod
    def _get_soem_iomap_size_bytes(eni: ENI) -> int:
        """Calculate an iomap size that will exceed the required iomap size
        for SOEM."""

        # TODO: investigate how SOEM actually performs overlap map
        # and return accurate iomap size.
        iomap_size_bits: int = 0

        for subdevice in eni.config.subdevices:
            if process_data := subdevice.process_data:
                if send := process_data.send:
                    iomap_size_bits += send.bit_length
                if recv := process_data.recv:
                    iomap_size_bits += recv.bit_length
        _logger.debug(f"Calcuated soem iomap size bits: {iomap_size_bits}")
        return iomap_size_bits // 8 + 1
