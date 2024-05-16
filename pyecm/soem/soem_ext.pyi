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

    def init_redundant(self, ifname: str, if2name: str) -> int: ...

    def readstate(self) -> int: ...

    def writestate(self, subdevice: int) -> int: ...

    def statecheck(self, subdevice: int, reqstate: int, timeout_us: int) -> int: ...

    def send_overlap_processdata_group(self, group: int) -> int: ...

    def receive_processdata_group(self, group: int, timeout_us: int) -> int: ...

    def init(self, ifname: str) -> int: ...

    def config_init(self) -> int: ...

    def config_overlap_map(self) -> int: ...

    def recover_subdevice(self, subdevice: int, timeout_us: int) -> int: ...

    def reconfig_subdevice(self, subdevice: int, timeout_us: int) -> int: ...

    def configdc(self) -> bool: ...

    def dcsync0(self, subdevice: int, act: int, CyclTime_ns: int, CycleShift_ns: int) -> None: ...

    def dcsync01(self, subdevice: int, act: int, CyclTime0_ns: int, CyclTime1_ns: int, CyclShift_ns: int) -> None: ...

    def SDOread(self, subdevice: int, index: int, subindex: int, complete_access: int, size: int, timeout_us: int) -> tuple[int, int, Annotated[ArrayLike, dict(dtype='uint8', shape=(None), order='C')]]: ...

    def SDOwrite(self, subdevice: int, index: int, subindex: int, complete_access: int, data: Annotated[ArrayLike, dict(dtype='uint8', shape=(None), order='C')], timeout_us: int) -> int: ...

    @property
    def iomap(self) -> Annotated[ArrayLike, dict(dtype='uint8', shape=(None), order='C')]: ...

    def get_iomap(self, subdevice: int) -> tuple[Annotated[ArrayLike, dict(dtype='uint8', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='uint8', shape=(None), order='C')]]: ...

    def get_subdevice(self, subdevice: int) -> SubDevice: ...

class SubDevice:
    def __init__(self) -> None: ...

    @property
    def state(self) -> int: ...

    @state.setter
    def state(self, arg: int, /) -> None: ...

    @property
    def ALstatuscode(self) -> int: ...

    @ALstatuscode.setter
    def ALstatuscode(self, arg: int, /) -> None: ...

    @property
    def configadr(self) -> int: ...

    @configadr.setter
    def configadr(self, arg: int, /) -> None: ...

    @property
    def aliasadr(self) -> int: ...

    @aliasadr.setter
    def aliasadr(self, arg: int, /) -> None: ...

    @property
    def eep_man(self) -> int: ...

    @eep_man.setter
    def eep_man(self, arg: int, /) -> None: ...

    @property
    def eep_id(self) -> int: ...

    @eep_id.setter
    def eep_id(self, arg: int, /) -> None: ...

    @property
    def eep_rev(self) -> int: ...

    @eep_rev.setter
    def eep_rev(self, arg: int, /) -> None: ...

    @property
    def Itype(self) -> int: ...

    @Itype.setter
    def Itype(self, arg: int, /) -> None: ...

    @property
    def Dtype(self) -> int: ...

    @Dtype.setter
    def Dtype(self, arg: int, /) -> None: ...

    @property
    def Obits(self) -> int: ...

    @Obits.setter
    def Obits(self, arg: int, /) -> None: ...

    @property
    def Obytes(self) -> int: ...

    @Obytes.setter
    def Obytes(self, arg: int, /) -> None: ...

    @property
    def outputs(self) -> int: ...

    @property
    def Ostartbit(self) -> int: ...

    @Ostartbit.setter
    def Ostartbit(self, arg: int, /) -> None: ...

    @property
    def Ibits(self) -> int: ...

    @Ibits.setter
    def Ibits(self, arg: int, /) -> None: ...

    @property
    def Ibytes(self) -> int: ...

    @Ibytes.setter
    def Ibytes(self, arg: int, /) -> None: ...

    @property
    def inputs(self) -> int: ...

    @property
    def Istartbit(self) -> int: ...

    @Istartbit.setter
    def Istartbit(self, arg: int, /) -> None: ...

    @property
    def FMMU0func(self) -> int: ...

    @FMMU0func.setter
    def FMMU0func(self, arg: int, /) -> None: ...

    @property
    def FMMU1func(self) -> int: ...

    @FMMU1func.setter
    def FMMU1func(self, arg: int, /) -> None: ...

    @property
    def FMMU2func(self) -> int: ...

    @FMMU2func.setter
    def FMMU2func(self, arg: int, /) -> None: ...

    @property
    def FMMU3func(self) -> int: ...

    @FMMU3func.setter
    def FMMU3func(self, arg: int, /) -> None: ...

    @property
    def mbx_l(self) -> int: ...

    @mbx_l.setter
    def mbx_l(self, arg: int, /) -> None: ...

    @property
    def mbx_wo(self) -> int: ...

    @mbx_wo.setter
    def mbx_wo(self, arg: int, /) -> None: ...

    @property
    def mbx_rl(self) -> int: ...

    @mbx_rl.setter
    def mbx_rl(self, arg: int, /) -> None: ...

    @property
    def mbx_ro(self) -> int: ...

    @mbx_ro.setter
    def mbx_ro(self, arg: int, /) -> None: ...

    @property
    def mbx_proto(self) -> int: ...

    @mbx_proto.setter
    def mbx_proto(self, arg: int, /) -> None: ...

    @property
    def mbx_cnt(self) -> int: ...

    @mbx_cnt.setter
    def mbx_cnt(self, arg: int, /) -> None: ...

    @property
    def hasdc(self) -> int: ...

    @hasdc.setter
    def hasdc(self, arg: int, /) -> None: ...

    @property
    def ptype(self) -> int: ...

    @ptype.setter
    def ptype(self, arg: int, /) -> None: ...

    @property
    def topology(self) -> int: ...

    @topology.setter
    def topology(self, arg: int, /) -> None: ...

    @property
    def activeports(self) -> int: ...

    @activeports.setter
    def activeports(self, arg: int, /) -> None: ...

    @property
    def consumedports(self) -> int: ...

    @consumedports.setter
    def consumedports(self, arg: int, /) -> None: ...

    @property
    def parent(self) -> int: ...

    @parent.setter
    def parent(self, arg: int, /) -> None: ...

    @property
    def parentport(self) -> int: ...

    @parentport.setter
    def parentport(self, arg: int, /) -> None: ...

    @property
    def entryport(self) -> int: ...

    @entryport.setter
    def entryport(self, arg: int, /) -> None: ...

    @property
    def DCrtA(self) -> int: ...

    @DCrtA.setter
    def DCrtA(self, arg: int, /) -> None: ...

    @property
    def DCrtB(self) -> int: ...

    @DCrtB.setter
    def DCrtB(self, arg: int, /) -> None: ...

    @property
    def DCrtC(self) -> int: ...

    @DCrtC.setter
    def DCrtC(self, arg: int, /) -> None: ...

    @property
    def DCrtD(self) -> int: ...

    @DCrtD.setter
    def DCrtD(self, arg: int, /) -> None: ...

    @property
    def pdelay(self) -> int: ...

    @pdelay.setter
    def pdelay(self, arg: int, /) -> None: ...

    @property
    def DCnext(self) -> int: ...

    @DCnext.setter
    def DCnext(self, arg: int, /) -> None: ...

    @property
    def DCprevious(self) -> int: ...

    @DCprevious.setter
    def DCprevious(self, arg: int, /) -> None: ...

    @property
    def DCcycle(self) -> int: ...

    @DCcycle.setter
    def DCcycle(self, arg: int, /) -> None: ...

    @property
    def DCshift(self) -> int: ...

    @DCshift.setter
    def DCshift(self, arg: int, /) -> None: ...

    @property
    def DCactive(self) -> int: ...

    @DCactive.setter
    def DCactive(self, arg: int, /) -> None: ...

    @property
    def configindex(self) -> int: ...

    @configindex.setter
    def configindex(self, arg: int, /) -> None: ...

    @property
    def SIIindex(self) -> int: ...

    @SIIindex.setter
    def SIIindex(self, arg: int, /) -> None: ...

    @property
    def eep_8byte(self) -> int: ...

    @eep_8byte.setter
    def eep_8byte(self, arg: int, /) -> None: ...

    @property
    def eep_pdi(self) -> int: ...

    @eep_pdi.setter
    def eep_pdi(self, arg: int, /) -> None: ...

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

    @FMMUunused.setter
    def FMMUunused(self, arg: int, /) -> None: ...

    @property
    def islost(self) -> int: ...

    @islost.setter
    def islost(self, arg: int, /) -> None: ...

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
    EC_ERR_TYPE_SDO_ERROR: ec_err_type

    EC_ERR_TYPE_EMERGENCY: ec_err_type

    EC_ERR_TYPE_PACKET_ERROR: ec_err_type

    EC_ERR_TYPE_SDOINFO_ERROR: ec_err_type

    EC_ERR_TYPE_FOE_ERROR: ec_err_type

    EC_ERR_TYPE_FOE_BUF2SMALL: ec_err_type

    EC_ERR_TYPE_FOE_PACKET_NUMBER: ec_err_type

    EC_ERR_TYPE_SOE_ERROR: ec_err_type

    EC_ERR_TYPE_MBX_ERROR: ec_err_type

    EC_ERR_TYPE_FOE_FILE_NOTFOUND: ec_err_type

    EC_ERR_TYPE_EOE_INVALID_RX_DATA: ec_err_type

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

class ec_state(enum.IntEnum):
    NONE: ec_state

    INIT: ec_state

    PRE_OP: ec_state

    BOOT: ec_state

    SAFE_OP: ec_state

    OPERATIONAL: ec_state

    ACK: ec_state

    ERROR: ec_state

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
