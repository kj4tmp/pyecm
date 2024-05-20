from pathlib import Path

import pytest

from pyecm.eni import ENI


@pytest.mark.parametrize(
    ("file_path"), [("./tests/assets/eni/basic.xml"), ("./tests/assets/eni/empty.xml")]
)
def test_valid_eni_files(file_path):
    xml_doc = Path(file_path).read_text()
    ENI.from_xml(xml_doc)
