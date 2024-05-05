import logging

import pytest

import pyecm
from pyecm.soem import (
    ec_eepromFMMUt,
    ec_eepromSMt,
    ecx_config_init,
    ecx_config_map_group,
    ecx_contextt,
    ecx_init,
)

_logger = logging.getLogger(__name__)


def log_subdevices(subdevices: list[pyecm.soem.ec_slavet]):
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


def log_context(ctx: pyecm.soem.ecx_contextt):
    _logger.info(f"{ctx.port=}")
    _logger.info(f"{ctx.slavelist=}")
    _logger.info(f"{ctx.slavecount=}")
    _logger.info(f"{ctx.maxslave=}")
    _logger.info(f"{ctx.grouplist=}")
    _logger.info(f"{ctx.maxgroup=}")
    _logger.info(f"{ctx.esibuf=}")
    _logger.info(f"{ctx.esimap=}")
    _logger.info(f"{ctx.esislave=}")
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
    _logger.info(f"{ctx.userdata=}")
    log_subdevices(ctx.slavelist)


@pytest.mark.parametrize(
    ("maxslave", "maxgroup"),
    [[12345456, 12], [12, 12345], [-1, 23], [23, -1], [123456, 123456]],
)
def test_ecx_contextt_incompatible_arguments(maxslave, maxgroup):
    """context init should raise when args are too big / negative"""
    with pytest.raises(TypeError):
        ecx_contextt(maxslave, maxgroup)


@pytest.mark.parametrize(("maxslave", "maxgroup"), [[0, 1], [1, 0]])
def test_ecx_contextt_value_errors(maxslave, maxgroup):
    with pytest.raises(ValueError):
        ecx_contextt(maxslave, maxgroup)


@pytest.mark.parametrize(
    ("maxslave", "maxgroup"),
    [
        [12, 12],
        [1345, 1],
    ],
)
def test_ecx_contextt_compatible_arguments(maxslave, maxgroup):
    ecx_contextt(maxslave, maxgroup)


def test_ecx_init():
    context = ecx_contextt(maxslave=3, maxgroup=2)
    assert ecx_init(context, "eth0") == 0
    assert ecx_config_init(context, False) == -1
    iomap = bytearray(256)
    assert ecx_config_map_group(context, iomap, 1) == 0
    _logger.info(f"{iomap=}")
    log_context(context)


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
