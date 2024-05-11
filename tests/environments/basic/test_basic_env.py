"""

run using command:

pip install . && pytest --log-cli-level=INFO -s tests/environments/basic/test_basic_env.py
"""

import logging
import struct
import threading
import time

import numpy as np
import pytest

import pyecm
from pyecm.soem import SOEM, ec_state

_logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def basic_environment():
    # info about this environment
    USE_REDUNDANCY = False
    NETWORK_ADAPTER_NAME = "enx00e04c681629"
    RED_NETWORK_ADAPTER_NAME = "enp0s20f0u3"
    NUM_SUBDEVICES = 5

    adapters = pyecm.soem.ec_find_adapters()
    adapter_names = [adapter.name for adapter in adapters]
    _logger.info(f"{adapters=}")

    assert NETWORK_ADAPTER_NAME in adapter_names

    if USE_REDUNDANCY:
        assert RED_NETWORK_ADAPTER_NAME in adapter_names

    main_device = pyecm.soem.SOEM(
        maxslave=512, maxgroup=2, iomap_size_bytes=4096, manualstatechange=True
    )
    _logger.info(f"{main_device=}")
    if USE_REDUNDANCY:
        assert main_device.init_redundant(NETWORK_ADAPTER_NAME, RED_NETWORK_ADAPTER_NAME) > 0
        _logger.info("init_redundant successfull")
    else:
        assert main_device.init(NETWORK_ADAPTER_NAME) > 0
        _logger.info("init successfull")
    # i don't know why but this fails frequently unless the subdevices are power cycled
    assert main_device.config_init() == NUM_SUBDEVICES
    assert main_device.slavecount == NUM_SUBDEVICES
    _logger.info("config_init successfull")

    # request and verify PREOP state
    main_device_entry = main_device.slavelist[0]
    main_device_entry.state = ec_state.PRE_OP
    main_device.slavelist[0] = main_device_entry
    main_device.writestate(slave=0)
    lowest_state_found = main_device.statecheck(
        slave=0,
        reqstate=pyecm.soem.ec_state.PRE_OP,
        timeout_us=2000,
    )
    assert (
        lowest_state_found == ec_state.PRE_OP
    ), f"not all subdevices reached PREOP! lowest state found: {ec_state(lowest_state_found)}"
    print(f"reached state: {ec_state(lowest_state_found)}")

    if main_device.configdc():
        _logger.info("distrubuted clocks configured")
    else:
        _logger.info("no distributed clock enabled subdevices found")

    _logger.info("test starting")

    # log_context(main_device)
    yield main_device
    _logger.info("test finished")

    while main_device.iserror():
        iserror, error = main_device.poperror()
        if iserror:
            _logger.error(
                f"{error.Slave=} {hex(error.Index)=} {hex(error.SubIdx)=} {error.Etype=} {hex(error.AbortCode)=} {hex(error.ErrorCode)=} {error.ErrorReg=} {error.b1=} {error.w1=} {error.w2=}"
            )

    # log_context(main_device)
    main_device.close()


def log_subdevices(subdevices: pyecm.soem.ECSlaveTVector, slavecount):
    for i, subdevice in enumerate(subdevices[0 : slavecount + 1]):
        if i == 0:
            _logger.info("MainDevice:")
        else:
            _logger.info(f"SubDevice: {i-1}")
        _logger.info(f"    {subdevice.state=}")
        _logger.info(f"    {subdevice.ALstatuscode=}")
        _logger.info(f"    {subdevice.configadr=}")
        _logger.info(f"    {subdevice.aliasadr=}")
        _logger.info(f"    {subdevice.eep_man=}")
        _logger.info(f"    {subdevice.eep_id=}")
        _logger.info(f"    {subdevice.eep_rev=}")
        _logger.info(f"    {subdevice.Itype=}")
        _logger.info(f"    {subdevice.Dtype=}")
        _logger.info(f"    {subdevice.Obits=}")
        _logger.info(f"    {subdevice.Obytes=}")
        _logger.info(f"    {subdevice.outputs=}")
        _logger.info(f"    {subdevice.Ostartbit=}")
        _logger.info(f"    {subdevice.Ibits=}")
        _logger.info(f"    {subdevice.Ibytes=}")
        _logger.info(f"    {subdevice.inputs=}")
        _logger.info(f"    {subdevice.Istartbit=}")
        # _logger.info(f"    {subdevice.SM=}")
        # _logger.info(f"    {subdevice.SMtype=}")
        # _logger.info(f"    {subdevice.FMMU=}")
        _logger.info(f"    {subdevice.FMMU0func=}")
        _logger.info(f"    {subdevice.FMMU1func=}")
        _logger.info(f"    {subdevice.FMMU2func=}")
        _logger.info(f"    {subdevice.FMMU3func=}")
        _logger.info(f"    {subdevice.mbx_l=}")
        _logger.info(f"    {subdevice.mbx_wo=}")
        _logger.info(f"    {subdevice.mbx_rl=}")
        _logger.info(f"    {subdevice.mbx_ro=}")
        _logger.info(f"    {subdevice.mbx_proto=}")
        _logger.info(f"    {subdevice.mbx_cnt=}")
        _logger.info(f"    {subdevice.hasdc=}")
        _logger.info(f"    {subdevice.ptype=}")
        _logger.info(f"    {subdevice.topology=}")
        _logger.info(f"    {subdevice.activeports=}")
        _logger.info(f"    {subdevice.consumedports=}")
        _logger.info(f"    {subdevice.parent=}")
        _logger.info(f"    {subdevice.parentport=}")
        _logger.info(f"    {subdevice.entryport=}")
        _logger.info(f"    {subdevice.DCrtA=}")
        _logger.info(f"    {subdevice.DCrtB=}")
        _logger.info(f"    {subdevice.DCrtC=}")
        _logger.info(f"    {subdevice.DCrtD=}")
        _logger.info(f"    {subdevice.pdelay=}")
        _logger.info(f"    {subdevice.DCnext=}")
        _logger.info(f"    {subdevice.DCprevious=}")
        _logger.info(f"    {subdevice.DCcycle=}")
        _logger.info(f"    {subdevice.DCshift=}")
        _logger.info(f"    {subdevice.DCactive=}")
        _logger.info(f"    {subdevice.configindex=}")
        _logger.info(f"    {subdevice.SIIindex=}")
        _logger.info(f"    {subdevice.eep_8byte=}")
        _logger.info(f"    {subdevice.eep_pdi=}")
        _logger.info(f"    {subdevice.CoEdetails=}")
        _logger.info(f"    {subdevice.FoEdetails=}")
        _logger.info(f"    {subdevice.EoEdetails=}")
        _logger.info(f"    {subdevice.SoEdetails=}")
        _logger.info(f"    {subdevice.Ebuscurrent=}")
        _logger.info(f"    {subdevice.blockLRW=}")
        _logger.info(f"    {subdevice.group=}")
        _logger.info(f"    {subdevice.FMMUunused=}")
        _logger.info(f"    {subdevice.islost=}")
        # _logger.info(f"    {subdevice.PO2SOconfig=}")
        # _logger.info(f"    {subdevice.PO2SOconfigx=}")
        _logger.info(f"    {subdevice.name=}")


def log_context(ctx: pyecm.soem.SOEM):
    _logger.info(f"{ctx.port=}")
    _logger.info(f"{ctx.slavecount=}")
    _logger.info(f"{ctx.maxslave=}")
    _logger.info(f"{ctx.grouplist=}")
    _logger.info(f"{ctx.maxgroup=}")
    # _logger.info(f"{ctx.esibuf=}")
    # _logger.info(f"{ctx.esimap=}")
    # _logger.info(f"{ctx.esislave=}")
    _logger.info(f"{ctx.elist=}")
    _logger.info(f"{ctx.idxstack=}")
    _logger.info(f"{ctx.ecaterror=}")
    _logger.info(f"{ctx.DCtime=}")
    _logger.info(f"{ctx.SMcommtype=}")
    _logger.info(f"{ctx.PDOassign=}")
    _logger.info(f"{ctx.PDOdesc=}")
    _logger.info(f"{ctx.eepSM=}")
    _logger.info(f"{ctx.eepFMMU=}")
    # _logger.info(f"{ctx.manualstatechange=}")
    # _logger.info(f"{ctx.userdata=}")
    log_subdevices(ctx.slavelist, ctx.slavecount)


# we are at PREOP
def test_correct_subdevices(basic_environment: pyecm.soem.SOEM):
    ctx = basic_environment

    assert ctx.slavelist[1].name == "EK1100"
    assert ctx.slavelist[2].name == "EL3314"
    assert ctx.slavelist[3].name == "EL2088"
    assert ctx.slavelist[4].name == "EL3681"
    assert ctx.slavelist[5].name == "EL3204"
    pass


# still in PREOP
def test_sdo_read(basic_environment: SOEM):
    # read device name (EL3314-0000)
    wkc, bytes_read, res = basic_environment.SDOread(
        slave=2, index=0x1008, subindex=0x00, complete_access=False, size=32, timeout_us=2000
    )
    _logger.info(f"{wkc=} {bytes_read=} {res=}")
    assert wkc == 1
    assert bytes_read == 11
    assert bytes(res[:bytes_read]) == b"EL3314-0000"

    # read vendor id (0x00000002) (little endian)
    wkc, bytes_read, res = basic_environment.SDOread(
        slave=2, index=0x1018, subindex=0x01, complete_access=False, size=32, timeout_us=2000
    )
    _logger.info(f"{wkc=} {bytes_read=} {res=}")

    assert wkc == 1
    assert bytes_read == 4
    assert np.array_equal(res[:bytes_read], np.array([2, 0, 0, 0]))

    lowest_state_found = basic_environment.statecheck(
        slave=0,
        reqstate=pyecm.soem.ec_state.PRE_OP,
        timeout_us=2000,
    )
    assert (
        lowest_state_found == ec_state.PRE_OP
    ), f"not all subdevices reached PREOP! lowest state found: {ec_state(lowest_state_found)}"


# still in PREOP
def test_sdo_write(basic_environment: SOEM):

    # write presentation setting of EL3314

    # read signed (0)
    wkc, bytes_read, res = basic_environment.SDOread(
        slave=2, index=0x8000, subindex=0x02, complete_access=False, size=1, timeout_us=4000
    )
    assert wkc == 1
    assert bytes_read == 1
    assert res[0] in [0, 1, 2]  # signed
    _logger.info("good read 1")

    # write high resolution (2)
    wkc = basic_environment.SDOwrite(
        slave=2,
        index=0x8000,
        subindex=0x02,
        complete_access=False,
        timeout_us=10000,
        data=np.array([0b00000010], dtype="uint8"),
    )

    assert wkc == 1
    _logger.info("good write 2")

    # read high resolution (2)
    wkc, bytes_read, res = basic_environment.SDOread(
        slave=2, index=0x8000, subindex=0x02, complete_access=False, size=1, timeout_us=4000
    )
    assert wkc == 1
    assert bytes_read == 1
    assert res[0] == 2  # high resolution
    _logger.info("good read 3")

    # write signed (0)
    wkc = basic_environment.SDOwrite(
        slave=2,
        index=0x8000,
        subindex=0x02,
        complete_access=False,
        timeout_us=10000,
        data=np.array([0], dtype="uint8"),
    )
    assert wkc == 1
    _logger.info("good write 4")

    # read signed (0)
    wkc, bytes_read, res = basic_environment.SDOread(
        slave=2, index=0x8000, subindex=0x02, complete_access=False, size=1, timeout_us=2000
    )
    assert wkc == 1
    assert bytes_read == 1
    assert res[0] == 0  # signed
    _logger.info("good read 5")

    # write high resolution (2)
    wkc = basic_environment.SDOwrite(
        slave=2,
        index=0x8000,
        subindex=0x02,
        complete_access=False,
        timeout_us=10000,
        data=np.array([2], dtype="uint8"),
    )
    assert wkc == 1
    _logger.info("good write 6")

    # read high resolution (2)
    wkc, bytes_read, res = basic_environment.SDOread(
        slave=2, index=0x8000, subindex=0x02, complete_access=False, size=1, timeout_us=2000
    )
    assert wkc == 1
    assert bytes_read == 1
    assert res[0] == 2  # high resolution
    _logger.info("good read 7")

    lowest_state_found = basic_environment.statecheck(
        slave=0,
        reqstate=pyecm.soem.ec_state.PRE_OP,
        timeout_us=2000,
    )
    assert (
        lowest_state_found == ec_state.PRE_OP
    ), f"not all subdevices reached PREOP! lowest state found: {ec_state(lowest_state_found)}"


# still in PREOP
# TC in high resolution mode
def test_pdo(basic_environment: SOEM):
    iomap_size = basic_environment.config_overlap_map()
    assert iomap_size == 66
    assert iomap_size <= basic_environment.iomap.size  # type: ignore

    # request and verify SAFEOP
    basic_environment_entry = basic_environment.slavelist[0]
    basic_environment_entry.state = ec_state.SAFE_OP
    basic_environment.slavelist[0] = basic_environment_entry
    basic_environment.writestate(slave=0)
    lowest_state_found = basic_environment.statecheck(
        slave=0,
        reqstate=pyecm.soem.ec_state.SAFE_OP,
        timeout_us=2000,
    )
    assert (
        lowest_state_found == ec_state.SAFE_OP
    ), f"Not all subdevices reached SAFEOP! Lowest state found: {ec_state(lowest_state_found)}"
    print(f"reached state: {ec_state(lowest_state_found)}")

    # request and verify OP
    # need to send at least one set of process data
    res = basic_environment.send_overlap_processdata_group(0)
    assert res > 0, f"error on send process data({res})"
    wkc = basic_environment.receive_processdata_group(0, timeout_us=2000)

    basic_environment_entry = basic_environment.slavelist[0]
    basic_environment_entry.state = ec_state.OPERATIONAL
    basic_environment.slavelist[0] = basic_environment_entry
    basic_environment.writestate(slave=0)

    for _ in range(200):
        res = basic_environment.send_overlap_processdata_group(0)
        assert res > 0, f"error on send process data({res})"
        basic_environment.receive_processdata_group(0, timeout_us=2000)
        lowest_state_found = basic_environment.statecheck(
            slave=0,
            reqstate=ec_state.OPERATIONAL,
            timeout_us=2000,
        )
        if lowest_state_found == ec_state.OPERATIONAL:
            break
        _logger.info(f"attempting to reach OP. lowest state found: {ec_state(lowest_state_found)}")
    assert (
        lowest_state_found == ec_state.OPERATIONAL
    ), f"not all subdevices reached OP. Lowest state: {ec_state(lowest_state_found)}"
    _logger.info(f"reached state: {ec_state(lowest_state_found)}")
    log_subdevices(basic_environment.slavelist, basic_environment.slavecount)
    _logger.info(basic_environment.iomap.tobytes())


def test_get_iomap(basic_environment: SOEM):
    inputs, outputs = basic_environment.get_iomap(0)
    _logger.info(f"{inputs.size=}")
    _logger.info(f"{outputs.size=}")

    inputs, outputs = basic_environment.get_iomap(1)  # EK1100
    _logger.info(f"{basic_environment.slavelist[1].name} {inputs=}")
    _logger.info(f"{basic_environment.slavelist[1].name} {outputs=}")
    assert inputs.size == 0
    assert outputs.size == 0

    inputs, outputs = basic_environment.get_iomap(2)  # EL3314
    _logger.info(f"{basic_environment.slavelist[2].name} {inputs=}")
    _logger.info(f"{basic_environment.slavelist[2].name} {outputs=}")
    assert inputs.size == 16
    assert outputs.size == 0

    # check TC reading is 327.68 C (railed high)
    assert struct.unpack("<h", inputs[2:4])[0] == 32767

    inputs, outputs = basic_environment.get_iomap(3)  # EL2088
    _logger.info(f"{basic_environment.slavelist[3].name} {inputs=}")
    _logger.info(f"{basic_environment.slavelist[3].name} {outputs=}")
    assert inputs.size == 0
    assert outputs.size == 1

    inputs, outputs = basic_environment.get_iomap(4)  # EL3681
    _logger.info(f"{basic_environment.slavelist[4].name} {inputs=}")
    _logger.info(f"{basic_environment.slavelist[4].name} {outputs=}")
    assert inputs.size == 8
    assert outputs.size == 2

    inputs, outputs = basic_environment.get_iomap(5)  # EL3204
    _logger.info(f"{basic_environment.slavelist[5].name} {inputs=}")
    _logger.info(f"{basic_environment.slavelist[5].name} {outputs=}")
    assert inputs.size == 16
    assert outputs.size == 0


def test_iomap_byte_alignment(basic_environment: SOEM):

    inputs, outputs = basic_environment.get_iomap(0)
    _logger.info(f"main device: {inputs.size=} {outputs.size=}")
    total_inputs = inputs.size
    total_outputs = outputs.size

    count_inputs = 0
    count_outputs = 0
    for i, subdevice in enumerate(
        basic_environment.slavelist[1 : basic_environment.slavecount + 1]
    ):
        inputs, outputs = basic_environment.get_iomap(i + 1)
        _logger.info(
            f"{subdevice.name} {inputs.size=} {outputs.size=} {subdevice.Istartbit=} {subdevice.Ostartbit=}"
        )
        count_inputs += inputs.size
        count_outputs += outputs.size
    assert count_inputs == total_inputs
    assert count_outputs == total_outputs


def test_outputs(basic_environment: SOEM):

    # do 5 seconds of blinking LED
    _, el2088_outputs = basic_environment.get_iomap(3)
    start_time = time.perf_counter()
    last_toggle_time = time.perf_counter()
    while time.perf_counter() - start_time < 5:
        basic_environment.send_overlap_processdata_group(0)
        time.sleep(0.010)  # 10 ms cycletime
        basic_environment.receive_processdata_group(0, timeout_us=2000)

        if time.perf_counter() - last_toggle_time > 1:
            if el2088_outputs[0] == 1:  # type: ignore
                el2088_outputs[0] = 0  # type: ignore
            else:
                el2088_outputs[0] = 1  # type: ignore
            _logger.info(basic_environment.get_iomap(3))
            last_toggle_time = time.perf_counter()
