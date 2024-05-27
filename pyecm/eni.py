from enum import IntEnum, StrEnum
from typing import Annotated
from xml.etree.ElementTree import Element

from annotated_types import Len
from pydantic_xml import BaseXmlModel, attr, element

from pyecm.eni_types import HexBinary, HexDecValue


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


class DataTypeWithAttribute(BaseXmlModel):
    dscale: str | None = attr(name="DScale", default=None)

    # TODO: Base data types
    # TODO: Separate attribute type since dscale not availble to process image variables


class Variable(BaseXmlModel):
    name: str = element(tag="Name")
    comment: str | None = element(tag="Comment", default=None)
    data_type: str | None = element(tag="DataType", default=None)  # TODO: base data type
    bit_size: int = element(tag="BitSize")
    bit_offset: int = element(tag="BitOffs")


class Image(BaseXmlModel):
    byte_size: int = element(tag="ByteSize")
    variables: list[Variable] = element(tag="Variable", default_factory=list)


class ProcessImage(BaseXmlModel):
    inputs: Image | None = element(tag="Inputs", default=None)
    outputs: Image | None = element(tag="Outputs", default=None)


class MainDeviceState(StrEnum):
    INIT = "INIT"
    PREOP = "PREOP"
    SAFEOP = "SAFEOP"
    OP = "OP"


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


class CopyInfo(BaseXmlModel):
    source_bit_offset: HexDecValue = element(tag="SrcBitOffs")
    destination_bit_offset: HexDecValue = element(tag="DstBitOffs")
    bit_size: HexDecValue = element(tag="BitSize")


class CopyInfos(BaseXmlModel):
    copy_infos: list[CopyInfo] = element(tag="CopyInfo", default_factory=list)


class FrameCommand(BaseXmlModel):
    state: Annotated[list[MainDeviceState], Len(max_length=4)] = element(tag="State")
    comment: str | None = element(tag="Comment", default=None)
    command: EtherCATCommand = element(tag="Cmd")
    subdevice_address: int | None = element(tag="Adp", default=None)
    physical_memory_address: int | None = element(tag="Ado", default=None)
    logical_memory_address: int | None = element(tag="Addr", default=None)
    data: HexBinary | None = element(tag="Data", default=None)
    data_length: int | None = element(tag="DataLength", default=None)
    expected_wkc: int | None = element(tag="Cnt", default=None)
    input_offset_bytes: int = element(tag="InputOffs")
    output_offset_bytes: int = element(tag="OutputOffs")
    copy_info: CopyInfos | None = element(tag="CopyInfos", default=None)

    # TODO: model validator for adp etc.


class Frame(BaseXmlModel):
    comment: str | None = element(tag="Comment", default=None)
    command: Annotated[list[FrameCommand], Len(min_length=1)] = element(tag="Cmd")


class Cyclic(BaseXmlModel):
    comment: str | None = element(tag="Comment", default=None)
    cycle_time_us: int | None = element(tag="CycleTime", default=None)
    priority: int | None = element(tag="Priority", default=None)
    task_id: str | None = element(tag="TaskId", default=None)
    frame: Annotated[list[Frame], Len(min_length=1)] = element(tag="Frame")


class Send(BaseXmlModel):
    bit_start: int = element(tag="BitStart")
    bit_length: int = element(tag="BitLength")


class Recv(BaseXmlModel):
    bit_start: int = element(tag="BitStart")
    bit_length: int = element(tag="BitLength")


class SyncManagerType(StrEnum):
    INPUTS = "Inputs"
    OUTPUTS = "Outputs"


class SyncManagerSettings(BaseXmlModel):
    type: SyncManagerType = element(tag="Type")
    min_size_bytes: int | None = element(tag="MinSize", default=None)
    max_size_bytes: int | None = element(tag="MaxSize", default=None)
    default_size_bytes: int | None = element(tag="DefaultSize", default=None)
    start_address: int = element(tag="StartAddress")
    control_byte: int = element(tag="ControlByte")
    enable: bool = element(tag="Enable")
    virtual: bool | None = element(tag="Virtual", default=None)
    pdos: list[int] = element(tag="Pdo", default_factory=list)


class Name(BaseXmlModel):
    language_code_id: int | None = attr(name="LcId", default=None)


class Entry(BaseXmlModel):
    index: HexDecValue = element(tag="Index")
    subindex: HexDecValue | None = element(tag="SubIndex", default=None)
    bit_length: int = element(tag="BitLen")
    names: list[Name] = element(tag="Name", default_factory=list)
    comment: str | None = element(tag="Comment", default=None)
    data_type: str | None = element(
        tag="DataType", default=None
    )  # TODO: use data type with attribute

    # TODO: names mandatory when index != 0


class Pdo(BaseXmlModel):
    index: HexDecValue = element(tag="Index")
    names: Annotated[list[Name], Len(min_length=1)] = element(tag="Name")
    exclude: list[HexDecValue] = element(tag="Exclude", default_factory=list)
    entries: list[Entry] = element(tag="Entry", default_factory=list)
    fixed: bool | None = attr(name="Fixed", default=None)
    mandatory: bool | None = attr(name="Mandatory", default=None)
    virtual: bool | None = attr(name="Virtual", default=None)
    sync_manager: int | None = attr(name="Sm", default=None)
    sync_unit: int | None = attr(name="Su", default=None)
    oversampling_factor_default: int | None = attr(name="OSFac", default=None)
    oversampling_factor_min: int | None = attr(name="OSMin", default=None)
    oversampling_factor_max: int | None = attr(name="OSMax", default=None)
    oversamping_index_increment: int | None = attr(name="OSIndexInc", default=None)


class ProcessData(BaseXmlModel, search_mode="unordered"):
    # TODO: the order of tx_pdos vs rx_pdos is ambiguous

    send: Send | None = element(tag="Send", default=None)
    recv: Recv | None = element(tag="Recv", default=None)
    sm0: SyncManagerSettings | None = element(tag="Sm0", default=None)
    sm1: SyncManagerSettings | None = element(tag="Sm1", default=None)
    sm2: SyncManagerSettings | None = element(tag="Sm2", default=None)
    sm3: SyncManagerSettings | None = element(tag="Sm3", default=None)
    tx_pdos: list[Pdo] = element(tag="TxPdo", default_factory=list)
    rx_pdos: list[Pdo] = element(tag="RxPdo", default_factory=list)


class MailboxSendInfo(BaseXmlModel):
    start: int = element(tag="Start")
    length_bytes: int = element(tag="Length")


class MailboxRecvInfo(BaseXmlModel):
    start: int = element(tag="Start")
    length_bytes: int = element(tag="Length")
    poll_time_ms: int | None = element(tag="PollTime", default=None)
    status_bit_address: int | None = element(tag="StatusBitAddr", default=None)


class Bootstrap(BaseXmlModel):
    send: MailboxSendInfo = element(tag="Send")
    recv: MailboxRecvInfo = element(tag="Recv")


class Protocol(StrEnum):
    AoE = "AoE"
    EoE = "EoE"
    CoE = "CoE"
    SoE = "SoE"
    FoE = "FoE"
    VoE = "VoE"


class CCS(IntEnum):
    SDO_INITIATE_UPLOAD = 1
    SDO_INITIATE_DOWNLOAD = 2


class SDOCommand(BaseXmlModel):
    fixed: bool | None = element(tag="Fixed", default=None)
    complete_access: bool | None = element(tag="CompleteAccess", default=None)
    transitions: Annotated[list[Transition], Len(min_length=1)] = element(tag="Transition")
    comment: str | None = element(tag="Comment", default=None)
    timeout_ms: int = element(tag="Timeout")
    ccs: CCS = element(tags="Ccs")
    index: int = element(tags="Index")
    subindex: int = element(tags="SubIndex")
    data: HexBinary | None = element(tags="Data", default=None)
    disabled: bool | None = element(tags="Disabled", default=None)


class MailboxCoEInitCmds(BaseXmlModel):
    sdo_cmds: list[SDOCommand] = element("InitCmd", default_factory=list)


class ChannelInfo(BaseXmlModel):
    # TODO: should these be ints?
    overwritten_by_module: bool | None = attr(name="OverwrittenByModule", default=None)
    profile_number: str = element(tag="ProfileNo")
    add_info: str | None = element(tag="AddInfo", default=None)
    display_name: list[Name] = element(tag="Name", default_factory=list)


class Profile(BaseXmlModel, arbitrary_types_allowed=True):
    channel_infos: Annotated[list[ChannelInfo], Len(min_length=1)] = element(tag="ChannelInfo")
    vendor_specific: Element | None = element(tag="VendorSpecific", default=None)


class MailboxCoE(BaseXmlModel):
    init_cmds: MailboxCoEInitCmds | None = element("InitCmds", default=None)
    profile: Profile | None = element("Profile", default=None)


class ServiceChannelCommand(BaseXmlModel):
    fixed: bool | None = attr(name="Fixed", default=None)
    transitions: Annotated[list[Transition], Len(min_length=1)] = element(tag="Transition")
    comment: str | None = element(tag="Comment", default=None)
    timeout_ms: int = element(tag="Timeout")
    op_code: int = element(tag="OpCode")
    drive_number: int = element(tag="DriveNo")
    idn: int = element(tag="IDN")
    elements: int = element(tag="Elements")  # TODO: better elements type
    attribute: int = element(tag="Attribute")
    data: HexBinary | None = element(tag="Data", default=None)
    disabled: bool | None = element(tag="Disabled", default=None)


class MailboxSoEInitCmds(BaseXmlModel):
    service_channel_commands: list[ServiceChannelCommand] = element("InitCmd", default_factory=list)


class MailboxSoE(BaseXmlModel):
    init_cmds: MailboxSoEInitCmds | None = element("InitCmds", default=None)


class MailboxCommand(BaseXmlModel):
    transitions: Annotated[list[Transition], Len(min_length=1)] = element(tag="Transition")
    comment: str | None = element(tag="Comment", default=None)
    timeout_ms: int = element(tag="Timeout")
    data: HexBinary | None = element(tag="Data", default=None)
    disabled: bool | None = element(tag="Disabled", default=None)


class InitMailboxCmds(BaseXmlModel):
    mailbox_cmds: list[MailboxCommand] = element("InitCmd", default_factory=list)


class MailboxAoE(BaseXmlModel):
    init_cmds: InitMailboxCmds | None = element("InitCmds", default=None)
    net_id: str | None = element("NetId", default=None)  # TODO: better type for net id


class MailboxEoE(BaseXmlModel):
    init_cmds: InitMailboxCmds | None = element("InitCmds", default=None)


class MailboxFoE(BaseXmlModel):
    init_cmds: InitMailboxCmds | None = element("InitCmds", default=None)


class MailboxVoE(BaseXmlModel):
    init_cmds: InitMailboxCmds | None = element("InitCmds", default=None)


class Mailbox(BaseXmlModel):
    data_link_layer: bool | None = attr(name="DataLinkLayer", default=None)
    send: MailboxSendInfo = element(tag="Send")
    recv: MailboxRecvInfo = element(tag="Recv")
    bootstrap: Bootstrap | None = element(tag="Bootstrap", default=None)
    protocol: list[Protocol] = element(tag="Protocol", default_factory=list)
    coe: MailboxCoE | None = element(tag="CoE", default=None)
    soe: MailboxSoE | None = element(tag="SoE", default=None)
    aoe: MailboxAoE | None = element(tag="AoE", default=None)
    eoe: MailboxEoE | None = element(tag="EoE", default=None)
    foe: MailboxFoE | None = element(tag="FoE", default=None)
    voe: MailboxVoE | None = element(tag="VoE", default=None)


class Requires(StrEnum):
    SEPARATE_FRAME = "frame"
    SEPARATE_CYCLE = "cycle"


class InitECatCmdValidation(BaseXmlModel):
    data: HexBinary = element(tag="Data")
    data_mask: HexBinary | None = element(tag="DataMask", default=None)
    timeout_ms: int = element(tag="Timeout")


class ECatCmd(BaseXmlModel):
    transitions: list[Transition] = element(tag="Transition", default_factory=list)
    before_subdevice: bool | None = element(tag="BeforeSlave", default=None)
    comment: str | None = element(tag="Comment", default=None)
    requires: Requires | None = element(tag="Requires", default=None)
    command: EtherCATCommand = element(tag="Cmd")
    subdevice_address: int | None = element(tag="Adp", default=None)
    physical_memory_address: int | None = element(tag="Ado", default=None)
    logical_memory_address: int | None = element(tag="Addr", default=None)
    data: HexBinary | None = element(tag="Data", default=None)
    data_length: int | None = element(tag="DataLength", default=None)
    expected_wkc: int | None = element(tag="Cnt", default=None)
    retries: int | None = element(tag="Retries", default=None)
    validation: InitECatCmdValidation | None = element(tag="Validate", default=None)

    # TODO: add model validators for
    # data, data_length, physical_memory_address
    # logical_memory_address, subdevice_address
    # command


class InitECatCmds(BaseXmlModel):
    ecat_cmds: list[ECatCmd] = element(tag="InitCmd", default_factory=list)


class SubDeviceInfo(BaseXmlModel):
    name: str = element(tag="Name")
    physical_address: int | None = element(tag="PhysAddr", default=None)
    auto_increment_addres: int | None = element(tag="AutoIncAddr", default=None)
    physics: str | None = element(tag="Physics", default=None)
    vendor_id: int = element(tag="VendorId")
    product_code: int = element(tag="ProductCode")
    revision_number: int = element(tag="RevisionNo")
    serial_number: int = element(tag="SerialNo")
    product_revision: str | None = element(tag="ProductRevision")

    # TODO: add model validator
    # for physical_address, auto_increment_address
    # physics


class Port(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class PreviousPort(BaseXmlModel):
    selected: bool | None = attr("Selected", default=None)
    device_id: int | None = element("DeviceId", default=None)
    port: Port = element("Port")
    physical_address: int | None = element(tag="PhysAddr", default=None)


class HotConnect(BaseXmlModel):
    group_member_count: int = element("GroupMemberCnt")
    identify_command: Annotated[list[ECatCmd], Len(min_length=1)] = element("IdentifyCmd")


class DC(BaseXmlModel):
    potential_reference_clock: bool = element(tag="PotentialReferenceClock")

    # TODO: fix DC model


class SubDevice(BaseXmlModel):
    info: SubDeviceInfo = element(tag="Info")
    process_data: ProcessData | None = element(tag="ProcessData", default=None)
    mailbox: Mailbox | None = element(tag="Mailbox", default=None)
    init_cmds: InitECatCmds | None = element(tag="InitCmds", default=None)
    previous_port: PreviousPort | None = element(tag="PreviousPort", default=None)
    hot_connect: HotConnect | None = element(tags="HotConnect", default=None)
    dc: DC | None = element(tag="DC", default=None)
    # TODO; previous port model validator


class EtherType(StrEnum):
    UDP_ETHERCAT = "0080"  # little endian 0x8000
    ETHERCAT = "a488"  # little endian 0x88a4


class Info(BaseXmlModel):
    name: str = element(tag="Name")
    destination: HexBinary = element(tag="Destination")
    source: HexBinary = element(tag="Source")
    ether_type: EtherType | None = element(tag="EtherType")


class MailboxStates(BaseXmlModel):
    start_addr: int = element(tag="StartAddr")
    count: int = element(tag="Count")


class MainDeviceEoE(BaseXmlModel):
    max_ports: int = element(tag="MaxPorts")
    max_frames: int = element(tag="MaxFrames")
    max_macs: int = element(tag="MaxMACs")


class MainDevice(BaseXmlModel):
    info: Info = element(tag="Info")
    mailbox_states: MailboxStates | None = element(tag="MailboxStates", default=None)
    eoe: MainDeviceEoE | None = element(tag="EoE", default=None)
    init_cmds: InitECatCmds | None = element(tag="InitCmds", default=None)

    # TODO; previous port model validator


class Config(BaseXmlModel):
    main_device: MainDevice = element(tag="Master")
    subdevices: list[SubDevice] = element(tag="Slave", default_factory=list)
    cyclics: list[Cyclic] = element(tag="Cyclic", default_factory=list)
    process_image: ProcessImage | None = element(tag="ProcessImage", default=None)


class ENI(BaseXmlModel, tag="EtherCATConfig"):
    config: Config = element(tag="Config")
