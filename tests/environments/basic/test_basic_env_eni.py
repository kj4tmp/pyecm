from pathlib import Path

from returns.pipeline import is_successful

import pyecm
from pyecm.maindevice import ALControl, ALStatus


def test_use_eni():
    eni_path = Path(__file__).resolve().parent / "basic_environment_eni.xml"
    xml_doc = Path(eni_path).read_text()
    eni = pyecm.ENI.from_xml(xml_doc)
    main_device = pyecm.MainDevice(main_adapter_name="enx00e04c68191a", eni=eni)

    # scan, request_INIT
    init_res = main_device.init_verify_network()
    assert is_successful(init_res)

    # request PRE_OP
    state_res = main_device.request_state(subdevice=0, state=ALControl.PRE_OP, timeout_us=30_000)
    assert is_successful(state_res)
    assert main_device.read_states() == ALStatus.PRE_OP

    main_device.config_map()

    # request SAFE_OP
    state_res = main_device.request_state(subdevice=0, state=ALControl.SAFE_OP, timeout_us=30_000)
    assert is_successful(state_res)
    assert main_device.read_states() == ALStatus.SAFE_OP
