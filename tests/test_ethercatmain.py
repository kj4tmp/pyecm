import logging

import pyethercat

_logger = logging.getLogger(__name__)



def test_ec_find_adapters():
    adapters = pyethercat.soem.ec_find_adapters()
    for i, adapter in enumerate(adapters):
        _logger.info(adapter)
        _logger.info(f"adapter {i}: name: {adapter.name}, desc: {adapter.desc}")