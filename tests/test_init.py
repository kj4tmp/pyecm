
from pyecm.soem import ecx_contextt, ecx_init


def test_ecx_init():
    context = ecx_contextt()
    assert ecx_init(context, 'eth0') == 0