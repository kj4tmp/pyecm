from collections.abc import Iterable, Iterator
import enum
from typing import Annotated, overload

from numpy.typing import ArrayLike


class ECGroupTVector:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: ECGroupTVector) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[ec_groupt], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[ec_groupt]: ...

    @overload
    def __getitem__(self, arg: int, /) -> ec_groupt: ...

    @overload
    def __getitem__(self, arg: slice, /) -> ECGroupTVector: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: ec_groupt, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: ec_groupt, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> ec_groupt:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: ECGroupTVector, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: ec_groupt, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: ECGroupTVector, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

class SOEM:
    def __init__(self, max_subdevices: int = 512, maxgroup: int = 2, iomap_size_bytes: int = 4096, manualstatechange: bool = False) -> None: ...

    @property
    def port(self) -> ecx_portt: ...

    @property
    def subdevices(self) -> SubDeviceVector: ...

    @subdevices.setter
    def subdevices(self, arg: SubDeviceVector, /) -> None: ...

    @property
    def subdevice_count(self) -> int: ...

    @property
    def max_subdevices(self) -> int: ...

    @property
    def grouplist(self) -> ECGroupTVector: ...

    @property
    def maxgroup(self) -> int: ...

    @property
    def elist(self) -> ec_eringt: ...

    @property
    def idxstack(self) -> ec_idxstackT: ...

    @property
    def ecaterror(self) -> int: ...

    @property
    def DCtime(self) -> int: ...

    @property
    def SMcommtype(self) -> ec_SMcommtypet: ...

    @property
    def PDOassign(self) -> ec_PDOassignt: ...

    @property
    def PDOdesc(self) -> ec_PDOdesct: ...

    @property
    def eepSM(self) -> ec_eepromSMt: ...

    @property
    def eepFMMU(self) -> ec_eepromFMMUt: ...

    @property
    def manualstatechange(self) -> bool: ...

    def close(self) -> None: ...

    def iserror(self) -> bool: ...

    def poperror(self) -> tuple[bool, ec_errort]: ...

    def init_redundant(self, ifname: str, if2name: str) -> int:
        """Initialize SOEM library with cable redundancy. Returns > 0 if OK."""

    def readstate(self) -> int: ...

    def writestate(self, subdevice: int) -> int: ...

    def statecheck(self, subdevice: int, reqstate: int, timeout_us: int) -> int: ...

    def send_overlap_processdata_group(self, group: int) -> int: ...

    def receive_processdata_group(self, group: int, timeout_us: int) -> int: ...

    def init(self, ifname: str) -> int:
        """Initialize SOEM library. Returns > 0 if OK."""

    def config_init(self) -> int:
        """
        Enumerate and request INIT state for all subdevices. Returns workcounter of subdevice discovery datagram which is the number of subdevices found.
        """

    def config_overlap_map(self) -> int: ...

    def recover_subdevice(self, subdevice: int, timeout_us: int) -> int: ...

    def reconfig_subdevice(self, subdevice: int, timeout_us: int) -> int: ...

    def configdc(self) -> bool: ...

    def dcsync0(self, subdevice: int, act: int, CyclTime_ns: int, CycleShift_ns: int) -> None: ...

    def dcsync01(self, subdevice: int, act: int, CyclTime0_ns: int, CyclTime1_ns: int, CyclShift_ns: int) -> None: ...

    def SDOread(self, subdevice: int, index: int, subindex: int, complete_access: int, size: int, timeout_us: int) -> tuple[int, bytes]: ...

    def SDOwrite(self, subdevice: int, index: int, subindex: int, complete_access: bool, data: bytes, timeout_us: int) -> int: ...

    def readODlist(self, subdevice: int) -> tuple[int, ec_ODListt]: ...

    def readODdescription(self, item: int, ODlist: ec_ODListt) -> tuple[int, ec_ODListt]: ...

    def readOE(self, item: int, ODlist: ec_ODListt) -> tuple[int, ec_OEListt]: ...

    def siifind(self, subdevice: int, cat: int) -> int: ...

    def siigetbyte(self, subdevice: int, address: int) -> int: ...

    @property
    def iomap(self) -> Annotated[ArrayLike, dict(dtype='uint8', shape=(None), order='C')]: ...

    def get_iomap(self, subdevice: int) -> tuple[Annotated[ArrayLike, dict(dtype='uint8', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='uint8', shape=(None), order='C')]]: ...

class SubDevice:
    def __init__(self) -> None: ...

    @property
    def state(self) -> int: ...

    @state.setter
    def state(self, arg: int, /) -> None: ...

    @property
    def ALstatuscode(self) -> int: ...

    @property
    def configadr(self) -> int: ...

    @property
    def aliasadr(self) -> int: ...

    @property
    def eep_man(self) -> int: ...

    @property
    def eep_id(self) -> int: ...

    @property
    def eep_rev(self) -> int: ...

    @property
    def Itype(self) -> int: ...

    @property
    def Dtype(self) -> int: ...

    @property
    def Obits(self) -> int: ...

    @property
    def Obytes(self) -> int: ...

    @property
    def outputs(self) -> int: ...

    @property
    def Ostartbit(self) -> int: ...

    @property
    def Ibits(self) -> int: ...

    @property
    def Ibytes(self) -> int: ...

    @property
    def inputs(self) -> int: ...

    @property
    def Istartbit(self) -> int: ...

    @property
    def SM(self) -> list[ec_smt]: ...

    @property
    def SMtype(self) -> list[int]: ...

    @property
    def FMMU(self) -> list[ec_fmmut]: ...

    @property
    def FMMU0func(self) -> int: ...

    @property
    def FMMU1func(self) -> int: ...

    @property
    def FMMU2func(self) -> int: ...

    @property
    def FMMU3func(self) -> int: ...

    @property
    def mbx_l(self) -> int: ...

    @property
    def mbx_wo(self) -> int: ...

    @property
    def mbx_rl(self) -> int: ...

    @property
    def mbx_ro(self) -> int: ...

    @property
    def mbx_proto(self) -> int: ...

    @property
    def mbx_cnt(self) -> int: ...

    @property
    def hasdc(self) -> bool: ...

    @property
    def ptype(self) -> int: ...

    @property
    def topology(self) -> int: ...

    @property
    def activeports(self) -> int: ...

    @property
    def consumedports(self) -> int: ...

    @property
    def parent(self) -> int: ...

    @property
    def parentport(self) -> int: ...

    @property
    def entryport(self) -> int: ...

    @property
    def DCrtA(self) -> int: ...

    @property
    def DCrtB(self) -> int: ...

    @property
    def DCrtC(self) -> int: ...

    @property
    def DCrtD(self) -> int: ...

    @property
    def pdelay(self) -> int: ...

    @property
    def DCnext(self) -> int: ...

    @property
    def DCprevious(self) -> int: ...

    @property
    def DCcycle(self) -> int: ...

    @property
    def DCshift(self) -> int: ...

    @property
    def DCactive(self) -> int: ...

    @property
    def configindex(self) -> int: ...

    @property
    def SIIindex(self) -> int: ...

    @property
    def eep_8byte(self) -> int: ...

    @property
    def eep_pdi(self) -> int: ...

    @property
    def CoEdetails(self) -> int: ...

    @CoEdetails.setter
    def CoEdetails(self, arg: int, /) -> None: ...

    @property
    def FoEdetails(self) -> int: ...

    @FoEdetails.setter
    def FoEdetails(self, arg: int, /) -> None: ...

    @property
    def EoEdetails(self) -> int: ...

    @EoEdetails.setter
    def EoEdetails(self, arg: int, /) -> None: ...

    @property
    def SoEdetails(self) -> int: ...

    @SoEdetails.setter
    def SoEdetails(self, arg: int, /) -> None: ...

    @property
    def Ebuscurrent(self) -> int: ...

    @Ebuscurrent.setter
    def Ebuscurrent(self, arg: int, /) -> None: ...

    @property
    def blockLRW(self) -> int: ...

    @blockLRW.setter
    def blockLRW(self, arg: int, /) -> None: ...

    @property
    def group(self) -> int: ...

    @group.setter
    def group(self, arg: int, /) -> None: ...

    @property
    def FMMUunused(self) -> int: ...

    @property
    def islost(self) -> bool: ...

    @islost.setter
    def islost(self, arg: bool, /) -> None: ...

    @property
    def name(self) -> str: ...

class SubDeviceVector:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: SubDeviceVector) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[SubDevice], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[SubDevice]: ...

    @overload
    def __getitem__(self, arg: int, /) -> SubDevice: ...

    @overload
    def __getitem__(self, arg: slice, /) -> SubDeviceVector: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: SubDevice, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: SubDevice, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> SubDevice:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: SubDeviceVector, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: SubDevice, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: SubDeviceVector, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

def add(a: int, b: int) -> int: ...

class ec_ODListt:
    @property
    def subdevice(self) -> int: ...

    @property
    def Entries(self) -> int: ...

    @property
    def Index(self) -> list[int]: ...

    @property
    def DataType(self) -> list[int]: ...

    @property
    def ObjectCode(self) -> list[int]: ...

    @property
    def MaxSub(self) -> list[int]: ...

    @property
    def Name(self) -> list[str]: ...

class ec_OEListt:
    @property
    def Entries(self) -> int: ...

    @property
    def ValueInfo(self) -> list[int]: ...

    @property
    def DataType(self) -> list[int]: ...

    @property
    def BitLength(self) -> list[int]: ...

    @property
    def ObjAccess(self) -> list[int]: ...

    @property
    def Name(self) -> list[str]: ...

class ec_PDOassignt:
    pass

class ec_PDOdesct:
    pass

class ec_SMcommtypet:
    pass

class ec_adaptert:
    @property
    def name(self) -> str: ...

    @property
    def desc(self) -> str: ...

class ec_eepromFMMUt:
    def __init__(self) -> None: ...

    @property
    def Startpos(self) -> int: ...

    @Startpos.setter
    def Startpos(self, arg: int, /) -> None: ...

    @property
    def nFMMU(self) -> int: ...

    @nFMMU.setter
    def nFMMU(self, arg: int, /) -> None: ...

    @property
    def FMMU0(self) -> int: ...

    @FMMU0.setter
    def FMMU0(self, arg: int, /) -> None: ...

    @property
    def FMMU1(self) -> int: ...

    @FMMU1.setter
    def FMMU1(self, arg: int, /) -> None: ...

    @property
    def FMMU2(self) -> int: ...

    @FMMU2.setter
    def FMMU2(self, arg: int, /) -> None: ...

    @property
    def FMMU3(self) -> int: ...

    @FMMU3.setter
    def FMMU3(self, arg: int, /) -> None: ...

class ec_eepromSMt:
    def __init__(self) -> None: ...

    @property
    def Startpos(self) -> int: ...

    @Startpos.setter
    def Startpos(self, arg: int, /) -> None: ...

    @property
    def nSM(self) -> int: ...

    @nSM.setter
    def nSM(self, arg: int, /) -> None: ...

    @property
    def PhStart(self) -> int: ...

    @PhStart.setter
    def PhStart(self, arg: int, /) -> None: ...

    @property
    def Plength(self) -> int: ...

    @Plength.setter
    def Plength(self, arg: int, /) -> None: ...

    @property
    def Creg(self) -> int: ...

    @Creg.setter
    def Creg(self, arg: int, /) -> None: ...

    @property
    def Sreg(self) -> int: ...

    @Sreg.setter
    def Sreg(self, arg: int, /) -> None: ...

    @property
    def Activate(self) -> int: ...

    @Activate.setter
    def Activate(self, arg: int, /) -> None: ...

    @property
    def PDIctrl(self) -> int: ...

    @PDIctrl.setter
    def PDIctrl(self, arg: int, /) -> None: ...

class ec_eringt:
    pass

class ec_err_type(enum.Enum):
    EC_ERR_TYPE_SDO_ERROR = 0

    EC_ERR_TYPE_EMERGENCY = 1

    EC_ERR_TYPE_PACKET_ERROR = 3

    EC_ERR_TYPE_SDOINFO_ERROR = 5

    EC_ERR_TYPE_FOE_ERROR = 5

    EC_ERR_TYPE_FOE_BUF2SMALL = 6

    EC_ERR_TYPE_FOE_PACKET_NUMBER = 7

    EC_ERR_TYPE_SOE_ERROR = 8

    EC_ERR_TYPE_MBX_ERROR = 9

    EC_ERR_TYPE_FOE_FILE_NOTFOUND = 10

    EC_ERR_TYPE_EOE_INVALID_RX_DATA = 11

class ec_errort:
    @property
    def Time(self) -> ec_timet: ...

    @Time.setter
    def Time(self, arg: ec_timet, /) -> None: ...

    @property
    def Signal(self) -> int: ...

    @Signal.setter
    def Signal(self, arg: int, /) -> None: ...

    @property
    def subdevice(self) -> int: ...

    @subdevice.setter
    def subdevice(self, arg: int, /) -> None: ...

    @property
    def Index(self) -> int: ...

    @Index.setter
    def Index(self, arg: int, /) -> None: ...

    @property
    def SubIdx(self) -> int: ...

    @SubIdx.setter
    def SubIdx(self, arg: int, /) -> None: ...

    @property
    def Etype(self) -> ec_err_type: ...

    @Etype.setter
    def Etype(self, arg: ec_err_type, /) -> None: ...

    @property
    def AbortCode(self) -> int: ...

    @AbortCode.setter
    def AbortCode(self, arg: int, /) -> None: ...

    @property
    def ErrorCode(self) -> int: ...

    @ErrorCode.setter
    def ErrorCode(self, arg: int, /) -> None: ...

    @property
    def ErrorReg(self) -> int: ...

    @ErrorReg.setter
    def ErrorReg(self, arg: int, /) -> None: ...

    @property
    def b1(self) -> int: ...

    @b1.setter
    def b1(self, arg: int, /) -> None: ...

    @property
    def w1(self) -> int: ...

    @w1.setter
    def w1(self, arg: int, /) -> None: ...

    @property
    def w2(self) -> int: ...

    @w2.setter
    def w2(self, arg: int, /) -> None: ...

def ec_find_adapters() -> list[ec_adaptert]: ...

class ec_fmmut:
    @property
    def LogStart(self) -> int: ...

    @property
    def LogLength(self) -> int: ...

    @property
    def LogStartbit(self) -> int: ...

    @property
    def LogEndbit(self) -> int: ...

    @property
    def PhysStart(self) -> int: ...

    @property
    def PhysStartBit(self) -> int: ...

    @property
    def FMMUtype(self) -> int: ...

    @property
    def FMMUactive(self) -> int: ...

    @property
    def unused1(self) -> int: ...

    @property
    def unused2(self) -> int: ...

class ec_groupt:
    @property
    def logstartaddr(self) -> int: ...

    @logstartaddr.setter
    def logstartaddr(self, arg: int, /) -> None: ...

    @property
    def Obytes(self) -> int: ...

    @Obytes.setter
    def Obytes(self, arg: int, /) -> None: ...

    @property
    def outputs(self) -> int: ...

    @outputs.setter
    def outputs(self, arg: int, /) -> None: ...

    @property
    def Ibytes(self) -> int: ...

    @Ibytes.setter
    def Ibytes(self, arg: int, /) -> None: ...

    @property
    def inputs(self) -> int: ...

    @inputs.setter
    def inputs(self, arg: int, /) -> None: ...

    @property
    def hasdc(self) -> int: ...

    @hasdc.setter
    def hasdc(self, arg: int, /) -> None: ...

    @property
    def DCnext(self) -> int: ...

    @DCnext.setter
    def DCnext(self, arg: int, /) -> None: ...

    @property
    def Ebuscurrent(self) -> int: ...

    @Ebuscurrent.setter
    def Ebuscurrent(self, arg: int, /) -> None: ...

    @property
    def blockLRW(self) -> int: ...

    @blockLRW.setter
    def blockLRW(self, arg: int, /) -> None: ...

    @property
    def nsegments(self) -> int: ...

    @nsegments.setter
    def nsegments(self, arg: int, /) -> None: ...

    @property
    def Isegment(self) -> int: ...

    @Isegment.setter
    def Isegment(self, arg: int, /) -> None: ...

    @property
    def Ioffset(self) -> int: ...

    @Ioffset.setter
    def Ioffset(self, arg: int, /) -> None: ...

    @property
    def outputsWKC(self) -> int: ...

    @outputsWKC.setter
    def outputsWKC(self, arg: int, /) -> None: ...

    @property
    def inputsWKC(self) -> int: ...

    @inputsWKC.setter
    def inputsWKC(self, arg: int, /) -> None: ...

    @property
    def docheckstate(self) -> int: ...

    @docheckstate.setter
    def docheckstate(self, arg: int, /) -> None: ...

class ec_idxstackT:
    pass

class ec_smt:
    @property
    def StartAddr(self) -> int: ...

    @property
    def SMlength(self) -> int: ...

    @property
    def SMflags(self) -> int: ...

class ec_state(enum.IntEnum):
    NONE = 0

    INIT = 1

    PRE_OP = 2

    BOOT = 3

    SAFE_OP = 4

    OPERATIONAL = 8

    ACK = 16

    ERROR = 16

class ec_timet:
    @property
    def sec(self) -> int: ...

    @sec.setter
    def sec(self, arg: int, /) -> None: ...

    @property
    def usec(self) -> int: ...

    @usec.setter
    def usec(self, arg: int, /) -> None: ...

class ecx_portt:
    pass

class ecx_redportt:
    def __init__(self) -> None: ...

def osal_usleep(usec: int) -> int: ...
