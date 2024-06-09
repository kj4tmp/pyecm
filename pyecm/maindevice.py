# TODO: hotconnect support

import logging

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from pyecm.eni import ENI
from pyecm.network_adapters import AdapterNotFoundError, validate_network_adapter_name
from pyecm.soem.soem_ext import SOEM

_logger = logging.getLogger(__name__)


class SubDevice:
    pass


class SOEMInitializationError(Exception):
    pass


class NoSubdevicesFoundError(Exception):
    pass


class BusENIMismatchError(Exception):
    pass


class MainDevice:

    def __init__(self, main_adapter_name: str, eni: ENI, red_adapter_name: str = ""):

        self.main_adapter_name = main_adapter_name
        self.eni = eni
        self.red_adapter_name = red_adapter_name

        maxgroup = max(len(self.eni.config.cyclics), 1)
        iomap_size_bytes = self._get_soem_iomap_size_bytes(eni=self.eni)
        self.soem = SOEM(
            max_subdevices=len(self.eni.config.subdevices),
            maxgroup=maxgroup,
            iomap_size_bytes=iomap_size_bytes,
            manualstatechange=True,
        )

    def init_verify_network(
        self,
    ) -> Result[
        None,
        AdapterNotFoundError
        | SOEMInitializationError
        | NoSubdevicesFoundError
        | BusENIMismatchError,
    ]:
        """Initialize network and verify network matches the ENI.

        This function requests INIT state for all subdevices.
        """
        match validate_network_adapter_name(adapter_name=self.main_adapter_name):
            case Failure(value):
                return Failure(value)
            case Success(adapter_name):
                _logger.debug(f"Main adapter {adapter_name} found.")

        if self.red_adapter_name:
            match validate_network_adapter_name(adapter_name=self.red_adapter_name):
                case Failure(value):
                    return Failure(value)
                case Success(adapter_name):
                    _logger.debug(f"Redundant adapter {adapter_name} found.")
        if self.red_adapter_name:
            if not self.soem.init_redundant(
                ifname=self.main_adapter_name, if2name=self.red_adapter_name
            ):
                return Failure(SOEMInitializationError())
            else:
                _logger.debug("SOEM init_redundant successfull.")
        else:
            if not self.soem.init(ifname=self.main_adapter_name):
                return Failure(SOEMInitializationError())
            else:
                _logger.debug("SOEM init successfull.")

        num_subdevices_found = self.soem.config_init()
        if num_subdevices_found == 0:
            return Failure(NoSubdevicesFoundError())

        # check number of subdevices.
        # ENI may contain passive subdevices that do not
        # respond to broadcast read in SOEM subdevice discovery.
        # i.e. EL9011
        expected_subdevice_count: int = 0
        for eni_subdevice in self.eni.config.subdevices:
            if eni_subdevice.process_data or eni_subdevice.mailbox or eni_subdevice.init_cmds:
                expected_subdevice_count += 1

        if num_subdevices_found != expected_subdevice_count:
            return Failure(
                BusENIMismatchError(
                    f"Number of subdevices found ({num_subdevices_found}) does not match ENI ({expected_subdevice_count})."
                )
            )
        for subdevice_index, bus_subdevice in enumerate(
            self.soem.subdevices[: num_subdevices_found + 1]
        ):
            if subdevice_index == 0:
                continue  # position zero reserved for main_device

            expected_subdevice_info = self.eni.config.subdevices[subdevice_index - 1].info
            exp_vendor_id = expected_subdevice_info.vendor_id
            exp_product_code = expected_subdevice_info.product_code
            exp_rev_num = expected_subdevice_info.revision_number

            # check vendor id
            if bus_subdevice.eep_man != exp_vendor_id:
                return Failure(
                    BusENIMismatchError(
                        f"Bus subdevice {subdevice_index} vendor id (0x{bus_subdevice.eep_man:08x}) does not match ENI (0x{exp_vendor_id:08x})"
                    )
                )
            # check product code
            if bus_subdevice.eep_id != exp_product_code:
                return Failure(
                    BusENIMismatchError(
                        f"Bus subdevice {subdevice_index} product code (0x{bus_subdevice.eep_id:08x}) does not match ENI (0x{exp_product_code:08x})"
                    )
                )
            # check revision number
            if bus_subdevice.eep_rev != exp_rev_num:
                return Failure(
                    BusENIMismatchError(
                        f"Bus subdevice {subdevice_index} revision number (0x{bus_subdevice.eep_rev:08x}) does not match ENI (0x{exp_rev_num:08x})"
                    )
                )
        return Success(None)

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
