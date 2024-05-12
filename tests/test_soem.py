import logging

import pytest

import pyecm
from pyecm.soem import SOEM, ec_eepromFMMUt, ec_eepromSMt, ec_slavet

_logger = logging.getLogger(__name__)


def log_subdevices(subdevices: pyecm.soem.ECSlaveTVector):
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
    # _logger.info(f"{subdevice.SM=}")
    # _logger.info(f"{subdevice.SMtype=}")
    # _logger.info(f"{subdevice.FMMU=}")
    # _logger.info(f"{subdevice.FMMU0func=}")
    # _logger.info(f"{subdevice.FMMU1func=}")
    # _logger.info(f"{subdevice.FMMU2func=}")
    # _logger.info(f"{subdevice.FMMU3func=}")
    # _logger.info(f"{subdevice.mbx_l=}")
    # _logger.info(f"{subdevice.mbx_wo=}")
    # _logger.info(f"{subdevice.mbx_rl=}")
    # _logger.info(f"{subdevice.mbx_ro=}")
    # _logger.info(f"{subdevice.mbx_proto=}")
    # _logger.info(f"{subdevice.mbx_cnt=}")
    # _logger.info(f"{subdevice.hasdc=}")
    # _logger.info(f"{subdevice.ptype=}")
    # _logger.info(f"{subdevice.topology=}")
    # _logger.info(f"{subdevice.activeports=}")
    # _logger.info(f"{subdevice.consumedports=}")
    # _logger.info(f"{subdevice.parent=}")
    # _logger.info(f"{subdevice.parentport=}")
    # _logger.info(f"{subdevice.entryport=}")
    # _logger.info(f"{subdevice.DCrtA=}")
    # _logger.info(f"{subdevice.DCrtB=}")
    # _logger.info(f"{subdevice.DCrtC=}")
    # _logger.info(f"{subdevice.DCrtD=}")
    # _logger.info(f"{subdevice.pdelay=}")
    # _logger.info(f"{subdevice.DCnext=}")
    # _logger.info(f"{subdevice.DCprevious=}")
    # _logger.info(f"{subdevice.DCcycle=}")
    # _logger.info(f"{subdevice.DCshift=}")
    # _logger.info(f"{subdevice.DCactive=}")
    # _logger.info(f"{subdevice.configindex=}")
    # _logger.info(f"{subdevice.SIIindex=}")
    # _logger.info(f"{subdevice.eep_8byte=}")
    # _logger.info(f"{subdevice.eep_pdi=}")
    # _logger.info(f"{subdevice.CoEdetails=}")
    # _logger.info(f"{subdevice.FoEdetails=}")
    # _logger.info(f"{subdevice.EoEdetails=}")
    # _logger.info(f"{subdevice.SoEdetails=}")
    # _logger.info(f"{subdevice.Ebuscurrent=}")
    # _logger.info(f"{subdevice.blockLRW=}")
    # _logger.info(f"{subdevice.group=}")
    # _logger.info(f"{subdevice.FMMUunused=}")
    # _logger.info(f"{subdevice.islost=}")
    # _logger.info(f"{subdevice.PO2SOconfig=}")
    # _logger.info(f"{subdevice.PO2SOconfigx=}")
    # _logger.info(f"{subdevice.name=}")


def log_context(ctx: pyecm.soem.SOEM):
    _logger.info(f"{ctx.port=}")
    _logger.info(f"{ctx.slavelist=}")
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
    log_subdevices(ctx.slavelist)


@pytest.mark.parametrize(
    ("maxslave", "maxgroup"),
    [[12345456, 12], [12, 12345], [-1, 23], [23, -1], [123456, 123456]],
)
def test_SOEM_incompatible_arguments(maxslave, maxgroup):
    """context init should raise when args are too big / negative"""
    with pytest.raises(TypeError):
        SOEM(maxslave, maxgroup, 1)


@pytest.mark.parametrize(
    ("maxslave", "maxgroup", "iomap_size_bytes"), [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
)
def test_SOEM_value_errors(maxslave, maxgroup, iomap_size_bytes):
    with pytest.raises(ValueError):
        SOEM(maxslave, maxgroup, iomap_size_bytes)


@pytest.mark.parametrize(
    ("maxslave", "maxgroup", "iomap_size_bytes"),
    [
        [12, 12, 1],
        [1345, 1, 12345],
    ],
)
def test_SOEM_compatible_arguments(maxslave, maxgroup, iomap_size_bytes):
    SOEM(maxslave, maxgroup, iomap_size_bytes)


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


# TODO: this fails due to nanobind copy return value policy for vector __getitem__
# def test_slavelist():
#     context = SOEM(maxslave=2, maxgroup=2)
#     context.slavelist[0].state = 13
#     assert context.slavelist[0].state == 13


def test_slavelist2():
    context = SOEM(maxslave=2, maxgroup=2, iomap_size_bytes=1)
    new_slave = ec_slavet()
    new_slave.state = 13
    context.slavelist[0] = new_slave
    assert context.slavelist[0].state == 13


def test_slavelist3():
    context = SOEM(maxslave=2, maxgroup=2, iomap_size_bytes=1)
    new_slave = context.slavelist[0]
    new_slave.state = 13
    context.slavelist[0] = new_slave
    assert context.slavelist[0].state == 13
