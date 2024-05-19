from enum import IntEnum, StrEnum
from pathlib import Path

from pydantic_xml import BaseXmlModel, element


class ProcessImage(BaseXmlModel):
    pass


class Cyclic(BaseXmlModel):
    pass


class SubDevice(BaseXmlModel):
    pass


class EtherType(StrEnum):
    UDP_ETHERCAT = "0080"  # little endian 0x8000
    ETHERCAT = "a488"  # little endian 0x88a4


class Info(BaseXmlModel):
    name: str = element(tag="Name")
    destination: str = element(tag="Destination")  # hex string MAC little endian
    source: str = element(tag="Source")  # hex string MAC little endian
    ether_type: EtherType | None = element(tag="EtherType")  # hex string


class MailboxStates(BaseXmlModel):
    start_addr: int = element(tag="StartAddr")
    count: int = element(tag="Count")


class EoE(BaseXmlModel):
    max_ports: int = element(tag="MaxPorts")
    max_frames: int = element(tag="MaxFrames")
    max_macs: int = element(tag="MaxMACs")


class Transition(StrEnum):
    INIT_TO_PREOP = "IP"
    PREOP_TO_SAFEOP = "PS"
    PREOP_TO_INIT = "PI"
    SAFEOP_TO_PREOP = "SP"
    SAFEOP_TO_OP = "SO"
    SAFEOP_TO_INIT = "SI"
    OP_TO_SAFEOP = "OS"
    OP_TO_PREOP = "OP"
    OP_TO_INIT = "OI"
    INIT_TO_BOOT = "IB"
    BOOT_TO_INIT = "BI"
    INIT_TO_INIT = "II"
    PREOP_TO_PREOP = "PP"
    SAFEOP_TO_SAFEOP = "SS"


class Requires(StrEnum):
    SEPARATE_FRAME = "frame"
    SEPARATE_CYCLE = "cycle"


class EtherCATCommand(IntEnum):
    NOP = 0
    APRD = 1
    APWR = 2
    APRW = 3
    FPRD = 4
    FPWR = 5
    FPRW = 6
    BRD = 7
    BWR = 8
    BRW = 9
    LRD = 10
    LWR = 11
    LRW = 12
    ARMW = 13
    FRMW = 14


class InitCmd(BaseXmlModel):
    transitions: list[Transition] = element(tag="Transition", default_factory=list)
    before_subdevice: bool | None = element(tag="BeforeSlave", default=None)
    comment: str | None = element(tag="Comment", default=None)
    requires: Requires | None = element(tag="Requires", default=None)
    command: EtherCATCommand = element(tag="Cmd")
    subdevice_address: int | None = element(tag="Adp", default=None)
    physical_memory_address: int | None = element(tag="Ado", default=None)


class InitCmds(BaseXmlModel):
    init_cmds: list[InitCmd] = element(tag="InitCmd", default_factory=list)


class MainDevice(BaseXmlModel):
    info: Info = element(tag="Info")
    mailbox_states: MailboxStates | None = element(tag="MailboxStates", default=None)
    eoe: EoE | None = element(tag="EoE", default=None)
    init_cmds: InitCmds | None = element(tag="InitCmds", default=None)


class Config(BaseXmlModel):
    main_device: MainDevice = element(tag="Master")
    subdevices: list[SubDevice] = element(tag="Slave", default_factory=list)
    cyclics: list[Cyclic] = element(tag="Cyclic", default_factory=list)
    process_image: ProcessImage | None = element(tag="ProcessImage", default=None)


class ENI(BaseXmlModel, tag="EtherCATConfig"):
    config: Config = element(tag="Config")


if __name__ == "__main__":
    xml_doc = Path("./tests/assets/eni/empty.xml").read_text()
    eni = ENI.from_xml(xml_doc)
    assert eni.config

    print(eni.to_xml())
