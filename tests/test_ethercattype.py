from pyethercat.soem import ec_err_type

def test_ec_err_type():
    assert ec_err_type.EC_ERR_TYPE_SDO_ERROR.value == 0
    assert ec_err_type.EC_ERR_TYPE_EMERGENCY.value == 1