'''

run using command:

pytest --log-cli-level=INFO -s tests/environments/basic/test_basic_env.py 
'''

import logging

import pyethercat

_logger = logging.getLogger(__name__)

def log_context(ctx: pyethercat.soem.ecx_contextt):
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







def test_init():
    adapter_name = 'enp0s20f0u1'

    ctx = pyethercat.soem.ecx_contextt()

    adapters = pyethercat.soem.ec_find_adapters()
    adapter_names = [adapter.name for adapter in adapters]
    assert adapter_name.encode() in adapter_names
    assert pyethercat.soem.ecx_init(ctx, adapter_name) > 0
    log_context(ctx)

def test_config_init():

    adapter_name = 'enp0s20f0u1'
    ctx = pyethercat.soem.ecx_contextt()
    assert pyethercat.soem.ecx_init(ctx, adapter_name) > 0
    num_subdevices_found = pyethercat.soem.ecx_config_init(ctx, False)
    log_context(ctx)
    assert  num_subdevices_found == 5




