from pathlib import Path

import pytest

from pyecm.eni import ENI


@pytest.mark.parametrize(
    ("file_path"),
    [
        (Path(__file__).resolve().parent / "assets/eni/basic.xml"),
        (Path(__file__).resolve().parent / "assets/eni/empty.xml"),
    ],
)
def test_valid_eni_files(file_path):
    xml_doc = Path(file_path).read_text()
    ENI.from_xml(xml_doc)
