import logging

from pyecm.soem import ec_err_type, ec_errort, ec_state, ec_timet

_logger = logging.getLogger(__name__)

def test_ec_err_type():
    assert ec_err_type.EC_ERR_TYPE_SDO_ERROR.value == 0
    assert ec_err_type.EC_ERR_TYPE_EMERGENCY.value == 1


def test_ec_state():
    assert ec_state.EC_STATE_NONE.value == 0
    assert ec_state.EC_STATE_INIT.value == 1