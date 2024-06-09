from pathlib import Path

from returns.pipeline import is_successful

import pyecm


def test_use_eni():
    eni_path = Path(__file__).resolve().parent / "basic_environment_eni.xml"
    xml_doc = Path(eni_path).read_text()
    eni = pyecm.ENI.from_xml(xml_doc)
    main_device = pyecm.MainDevice(main_adapter_name="enx00e04c68191a", eni=eni)
    init_res = main_device.init_verify_network()
    assert is_successful(init_res)
