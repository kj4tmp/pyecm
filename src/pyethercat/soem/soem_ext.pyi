import enum
import types


def add(a: int, b: int) -> int: ...

class ec_PDOassignt:
    pass

class ec_PDOdesct:
    pass

class ec_SMcommtypet:
    pass

class ec_adaptert:
    @property
    def name(self) -> bytes: ...

    @property
    def desc(self) -> bytes: ...

class ec_eepromFMMUt:
    pass

class ec_eepromSMt:
    pass

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
    def Slave(self) -> int: ...

    @Slave.setter
    def Slave(self, arg: int, /) -> None: ...

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
    pass

class ec_idxstackT:
    pass

class ec_slavet:
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

    @outputs.setter
    def outputs(self, arg: int, /) -> None: ...

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

    @inputs.setter
    def inputs(self, arg: int, /) -> None: ...

    @property
    def Istartbit(self) -> int: ...

    @Istartbit.setter
    def Istartbit(self, arg: int, /) -> None: ...

    @property
    def name(self) -> str: ...

class ec_state(enum.Enum):
    EC_STATE_NONE: ec_state

    EC_STATE_INIT: ec_state

    EC_STATE_PRE_OP: ec_state

    EC_STATE_BOOT: ec_state

    EC_STATE_SAFE_OP: ec_state

    EC_STATE_OPERATIONAL: ec_state

    EC_STATE_ACK: ec_state

    EC_STATE_ERROR: ec_state

class ec_timet:
    @property
    def sec(self) -> int: ...

    @sec.setter
    def sec(self, arg: int, /) -> None: ...

    @property
    def usec(self) -> int: ...

    @usec.setter
    def usec(self, arg: int, /) -> None: ...

def ecx_close(arg: ecx_contextt, /) -> None: ...

def ecx_config_init(arg0: ecx_contextt, arg1: int, /) -> int: ...

class ecx_contextt:
    def __init__(self) -> None: ...

    @property
    def port(self) -> ecx_portt: ...

    @port.setter
    def port(self, arg: ecx_portt, /) -> None: ...

    @property
    def slavelist(self) -> list[ec_slavet]: ...

    @property
    def slavecount(self) -> int: ...

    @slavecount.setter
    def slavecount(self, arg: int, /) -> None: ...

    @property
    def maxslave(self) -> int: ...

    @maxslave.setter
    def maxslave(self, arg: int, /) -> None: ...

    @property
    def grouplist(self) -> ec_groupt: ...

    @grouplist.setter
    def grouplist(self, arg: ec_groupt, /) -> None: ...

    @property
    def maxgroup(self) -> int: ...

    @maxgroup.setter
    def maxgroup(self, arg: int, /) -> None: ...

    @property
    def esibuf(self) -> int: ...

    @esibuf.setter
    def esibuf(self, arg: int, /) -> None: ...

    @property
    def esimap(self) -> int: ...

    @esimap.setter
    def esimap(self, arg: int, /) -> None: ...

    @property
    def esislave(self) -> int: ...

    @esislave.setter
    def esislave(self, arg: int, /) -> None: ...

    @property
    def elist(self) -> ec_eringt: ...

    @elist.setter
    def elist(self, arg: ec_eringt, /) -> None: ...

    @property
    def idxstack(self) -> ec_idxstackT: ...

    @idxstack.setter
    def idxstack(self, arg: ec_idxstackT, /) -> None: ...

    @property
    def ecaterror(self) -> int: ...

    @ecaterror.setter
    def ecaterror(self, arg: int, /) -> None: ...

    @property
    def DCtime(self) -> int: ...

    @DCtime.setter
    def DCtime(self, arg: int, /) -> None: ...

    @property
    def SMcommtype(self) -> ec_SMcommtypet: ...

    @SMcommtype.setter
    def SMcommtype(self, arg: ec_SMcommtypet, /) -> None: ...

    @property
    def PDOassign(self) -> ec_PDOassignt: ...

    @PDOassign.setter
    def PDOassign(self, arg: ec_PDOassignt, /) -> None: ...

    @property
    def PDOdesc(self) -> ec_PDOdesct: ...

    @PDOdesc.setter
    def PDOdesc(self, arg: ec_PDOdesct, /) -> None: ...

    @property
    def eepSM(self) -> ec_eepromSMt: ...

    @eepSM.setter
    def eepSM(self, arg: ec_eepromSMt, /) -> None: ...

    @property
    def eepFMMU(self) -> ec_eepromFMMUt: ...

    @eepFMMU.setter
    def eepFMMU(self, arg: ec_eepromFMMUt, /) -> None: ...

    @property
    def manualstatechange(self) -> int: ...

    @manualstatechange.setter
    def manualstatechange(self, arg: int, /) -> None: ...

    @property
    def userdata(self) -> types.CapsuleType: ...

    @userdata.setter
    def userdata(self, arg: types.CapsuleType, /) -> None: ...

def ecx_init(arg0: ecx_contextt, arg1: str, /) -> int: ...

def ecx_init_redundant(arg0: ecx_contextt, arg1: ecx_redportt, arg2: str, arg3: str, /) -> int: ...

def ecx_iserror(arg: ecx_contextt, /) -> int: ...

class ecx_portt:
    pass

class ecx_redportt:
    def __init__(self) -> None: ...
