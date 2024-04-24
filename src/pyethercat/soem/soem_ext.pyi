import enum


def add(a: int, b: int) -> int:
    """This function adds two numbers and increments if only one is provided."""

class ec_adaptert:
    @property
    def name(self) -> bytes: ...

    @property
    def desc(self) -> bytes: ...

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
    def __init__(self) -> None: ...

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
    def __init__(self) -> None: ...

    @property
    def sec(self) -> int: ...

    @sec.setter
    def sec(self, arg: int, /) -> None: ...

    @property
    def usec(self) -> int: ...

    @usec.setter
    def usec(self, arg: int, /) -> None: ...
