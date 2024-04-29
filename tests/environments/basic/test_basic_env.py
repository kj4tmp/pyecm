'''

run using command:

pip install . && pytest --log-cli-level=INFO -s tests/environments/basic/test_basic_env.py 
'''
import logging

import pyecm
import pytest

_logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def basic_environment():
    # info about this environment
    USE_REDUNDANCY = True
    NETWORK_ADAPTER_NAME = 'enp0s20f0u1'
    RED_NETWORK_ADAPTER_NAME = 'enp0s20f0u3'
    NUM_SUBDEVICES = 5


    adapters = pyecm.soem.ec_find_adapters()
    adapter_names = [adapter.name.decode() for adapter in adapters]
    
    assert NETWORK_ADAPTER_NAME in adapter_names

    if USE_REDUNDANCY:
        assert RED_NETWORK_ADAPTER_NAME in adapter_names
    
    ctx = pyecm.soem.ecx_contextt()

    if USE_REDUNDANCY:
        red_port = pyecm.soem.ecx_redportt()
        assert pyecm.soem.ecx_init_redundant(ctx, red_port, NETWORK_ADAPTER_NAME, RED_NETWORK_ADAPTER_NAME) > 0
    else:
        assert pyecm.soem.ecx_init(ctx, NETWORK_ADAPTER_NAME) > 0
    

    # i don't know why but this fails frequently unless the subdevices are power cycled
    assert  pyecm.soem.ecx_config_init(ctx, False) == NUM_SUBDEVICES
    assert  ctx.slavecount == NUM_SUBDEVICES
    
    _logger.info('test starting')
    log_context(ctx)
    yield ctx
    _logger.info('test finished')
    log_context(ctx)
    pyecm.soem.ecx_close(ctx)

def log_subdevices(subdevices: list[pyecm.soem.ec_slavet]):
    for i, subdevice in enumerate(subdevices):
        if i ==0:
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

    
def test_correct_subdevices(basic_environment: pyecm.soem.ecx_contextt):

    ctx = basic_environment

    assert ctx.slavelist[1].name == 'EK1100'
    assert ctx.slavelist[2].name == 'EL3314'
    assert ctx.slavelist[3].name == 'EL2088'
    assert ctx.slavelist[4].name == 'EL3681'
    assert ctx.slavelist[5].name == 'EL3204'
    pass

def test_process_data():
    pass






