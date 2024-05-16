import logging

import pytest

import pyecm
from pyecm.soem import SOEM, SubDeviceVector, ec_eepromFMMUt, ec_eepromSMt

_logger = logging.getLogger(__name__)


def log_subdevices(subdevices: SubDeviceVector):
    for i, subdevice in enumerate(subdevices):
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
        _logger.info(f"    {subdevice.name=}")


def log_context(ctx: pyecm.soem.SOEM):
    _logger.info(f"{ctx.port=}")
    _logger.info(f"{ctx.subdevices=}")
    _logger.info(f"{ctx.subdevice_count=}")
    _logger.info(f"{ctx.max_subdevices=}")
    _logger.info(f"{ctx.grouplist=}")
    _logger.info(f"{ctx.maxgroup=}")
    _logger.info(f"{ctx.elist=}")
    _logger.info(f"{ctx.idxstack=}")
    _logger.info(f"{ctx.ecaterror=}")
    _logger.info(f"{ctx.DCtime=}")
    _logger.info(f"{ctx.SMcommtype=}")
    _logger.info(f"{ctx.PDOassign=}")
    _logger.info(f"{ctx.PDOdesc=}")
    _logger.info(f"{ctx.eepSM=}")
    _logger.info(f"{ctx.eepFMMU=}")
    _logger.info(f"{ctx.manualstatechange=}")
    # _logger.info(f"{ctx.userdata=}")
    log_subdevices(ctx.subdevices)


@pytest.mark.parametrize(
    ("max_subdevices", "maxgroup"),
    [[12345456, 12], [12, 12345], [-1, 23], [23, -1], [123456, 123456]],
)
def test_SOEM_incompatible_arguments(max_subdevices, maxgroup):
    """context init should raise when args are too big / negative"""
    with pytest.raises(TypeError):
        SOEM(max_subdevices, maxgroup, 1)


@pytest.mark.parametrize(
    ("max_subdevices", "maxgroup", "iomap_size_bytes"), [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
)
def test_SOEM_value_errors(max_subdevices, maxgroup, iomap_size_bytes):
    with pytest.raises(ValueError):
        SOEM(max_subdevices, maxgroup, iomap_size_bytes)


@pytest.mark.parametrize(
    ("max_subdevices", "maxgroup", "iomap_size_bytes"),
    [
        [12, 12, 1],
        [1345, 1, 12345],
    ],
)
def test_SOEM_compatible_arguments(max_subdevices, maxgroup, iomap_size_bytes):
    SOEM(max_subdevices, maxgroup, iomap_size_bytes)


def test_ec_eepromFMMUt():
    t = ec_eepromFMMUt()
    t.FMMU0 = 23
    t.FMMU1 = 234
    t.FMMU2 = 0
    t.FMMU3 = 34
    t.nFMMU = 2
    with pytest.raises(TypeError):
        t.FMMU0 = 12345


def test_ec_eepromSM():
    t = ec_eepromSMt()
    t.nSM = 23
    with pytest.raises(TypeError):
        t.Creg = 12345


def test_get_subdevice():
    context = SOEM(max_subdevices=2, maxgroup=2)
    context.get_subdevice(0).state = 13
    assert context.get_subdevice(0).state == 13
    assert context.subdevices[0].state == 13


def test_manualstatechange():
    context = SOEM(max_subdevices=2, maxgroup=2, manualstatechange=True)
    assert context.manualstatechange is True
