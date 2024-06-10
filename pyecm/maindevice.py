# TODO: hotconnect support
# TODO: initcmds from ENI
# TODO: process data from ENI
# TODO: workcounter error detection
# TODO: EC_NOFRAME Define

import logging
from enum import IntEnum
from typing import Annotated

from annotated_types import Ge
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


class NoFrameError(Exception):
    pass


class ALStatus(IntEnum):
    """Possible read states of subdevices (the ALStatus register)."""

    UNKNOWN = 0x00
    INIT = 0x01
    PRE_OP = 0x02
    BOOT = 0x03
    SAFE_OP = 0x04
    OPERATIONAL = 0x08

    INIT_ERROR = 0x01 + 0x10
    PRE_OP_ERROR = 0x02 + 0x10
    BOOT_ERROR = 0x03 + 0x10
    SAFE_OP_ERROR = 0x04 + 0x10
    OPERATIONAL_ERROR = 0x08 + 0x10

    def is_error(self) -> bool:
        return self.value in [
            self.INIT_ERROR,
            self.PRE_OP_ERROR,
            self.BOOT_ERROR,
            self.SAFE_OP_ERROR,
            self.OPERATIONAL_ERROR,
        ]

    def without_error(self) -> "ALStatus":
        return ALStatus(self.value & 0x0F)


class ALControl(IntEnum):
    """Requestable states for subdevies.

    Use ack to clear errors in ALStatus.
    """

    INIT = 0x01
    PRE_OP = 0x02
    BOOT = 0x03
    SAFE_OP = 0x04
    OPERATIONAL = 0x08

    INIT_ACK = 0x01 + 0x10
    PRE_OP_ACK = 0x02 + 0x10
    BOOT_ACK = 0x03 + 0x10
    SAFE_OP_ACK = 0x04 + 0x10
    OPERATIONAL_ACK = 0x08 + 0x10

    def without_ack(self) -> "ALControl":
        return ALControl(self.value & 0x0F)


class MainDevice:
    """
    EtherCAT MainDevice.
    """

    def __init__(self, main_adapter_name: str, eni: ENI, red_adapter_name: str = ""):

        self.main_adapter_name = main_adapter_name
        self.eni = eni
        self.red_adapter_name = red_adapter_name

        maxgroup = max(len(self.eni.config.cyclics), 1)
        self.estimated_iomap_size_bytes: int = self._get_soem_iomap_size_bytes(eni=self.eni)
        self.soem = SOEM(
            max_subdevices=len(self.eni.config.subdevices),
            maxgroup=maxgroup,
            iomap_size_bytes=self.estimated_iomap_size_bytes,
            manualstatechange=True,
        )

    def init_verify_network(
        self,
    ) -> Result[
        None,
        AdapterNotFoundError
        | SOEMInitializationError
        | NoSubdevicesFoundError
        | NoFrameError
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
            return Failure(NoSubdevicesFoundError("No subdevices found."))
        elif num_subdevices_found == -1:
            return Failure(NoFrameError("No frame returned from broadcast read."))

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

    def config_map(self) -> None:
        req_iomap_size_bytes = self.soem.config_overlap_map()
        _logger.debug(f"Required iomap size bytes: {req_iomap_size_bytes}")
        assert (
            req_iomap_size_bytes <= self.estimated_iomap_size_bytes
        ), f"Required iomap size ({req_iomap_size_bytes} B) exceeds estimated iomap size ({self.estimated_iomap_size_bytes} B). seg fault likely!"

    def get_subdevice_state(self, subdevice: int) -> Result[int, ValueError]:
        """Get the last read state of a subdevice.
        This function does not actually communicate with the subdevices.
        The subdevice states should be actually read by self.read_states.
        """
        if subdevice > self.soem.subdevice_count or subdevice < 0:
            return Failure(
                ValueError(
                    f"Attempted to write state to subdevice ({subdevice}) outside of available subdvices (0-{self.soem.subdevice_count})"
                )
            )
        return Success(ALStatus(self.soem.subdevices[subdevice].state))

    def read_states(self) -> ALStatus:
        """Read the state of all subdevices. Returns lowest state found.

        This function sends frames to query the state of the subdevices.
        The state of each subdevice is then stored in self.soem.subdevices[...].state.
        The lowest state found is also stored in self.soem.subdevices[0].state
        """
        return ALStatus(self.soem.readstate())

    def request_state(
        self, subdevice: int, state: ALControl, timeout_us: Annotated[int, Ge(0)]
    ) -> Result[ALStatus, ALStatus | NoFrameError | ValueError]:
        """
        Send command to subdevice to transition to state.
        The subdevice may not complete the transition.
        The actual state of the subdevice must be read by self.read_states.

        Use subdevice=0 to request all subdevices.

        Use timeout=0 to send state change request to subdevice and return ALStatus.UNKNOWN immediatly.

        If timeout is >0, send state change request to subdevice and poll status every 1 ms until
        state is requested state or timeout is exceeded. If timeout is exceeded, return failure with
        the state of the subdevice.

        When subdevice=0 the state returned is the lowest state found.
        """
        if subdevice > self.soem.subdevice_count or subdevice < 0:
            return Failure(
                ValueError(
                    f"Attempted to write state to subdevice ({subdevice}) outside of available subdvices (0-{self.soem.subdevice_count})"
                )
            )
        self.soem.subdevices[subdevice].state = state.value
        res = self.soem.writestate(subdevice=subdevice)

        if res == -1:  # EC_NOFRAME
            return Failure(NoFrameError())
        else:
            # TODO: workcounter error detection
            pass

        if timeout_us <= 0:
            return Success(ALStatus.UNKNOWN)
        else:
            res = self.soem.statecheck(
                subdevice=subdevice, reqstate=state.value, timeout_us=timeout_us
            )
            status = ALStatus(res)
            if status.without_error().value != state.without_ack().value:
                return Failure(status)
            elif status.is_error():
                return Failure(status)
            else:
                return Success(status)

    def receive_process_data(self, timeout_us: int, group: int = 0) -> Result[int, NoFrameError]:
        res = self.soem.receive_processdata_group(group=group, timeout_us=timeout_us)
        if res == -1:
            return Failure(NoFrameError())
        else:
            # TODO: workcounter error detection
            return Success(res)

    def send_process_data(self, group: int = 0) -> None:
        self.soem.send_overlap_processdata_group(group=group)

    @staticmethod
    def _get_soem_iomap_size_bytes(eni: ENI) -> int:
        """Calculate an iomap size that will exceed the required iomap size
        for SOEM."""

        # TODO: investigate how SOEM actually performs overlap map
        # and return accurate iomap size.
        iomap_size_bytes: int = 0

        for subdevice in eni.config.subdevices:
            if process_data := subdevice.process_data:
                if send := process_data.send:
                    input_size_bytes = (send.bit_length + 7) // 8
                else:
                    input_size_bytes = 0
                if recv := process_data.recv:
                    output_size_bytes = (recv.bit_length + 7) // 8
                else:
                    output_size_bytes = 0
                iomap_size_bytes += max(input_size_bytes, output_size_bytes) * 2
        _logger.debug(f"Calcuated soem iomap size bytes: {iomap_size_bytes}")
        return iomap_size_bytes
