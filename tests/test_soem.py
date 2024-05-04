import logging

import pytest

from pyecm.soem import ecx_config_init, ecx_config_map_group, ecx_contextt, ecx_init

_logger = logging.getLogger(__name__)


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
