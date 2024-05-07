"""
A re-write of simple_test.c from SOEM in python.
"""

import argparse
import sys
import threading

import pyecm

iomap: bytearray = bytearray(4096)
expectedWKC: int = 0
needlf: bool = False
wkc: int = 0
inOP: bool = False
currentgroup: int = 0
forceByteAlignment: bool = False


def cyclic_task():
    return

    while True:
        pyecm.soem.osal_usleep(10000)  # run 10 ms cycle

        try:
            pass

        except Exception as e:
            print("exception in cyclic task")
            print(e)

    pass


def simpletest(ifname: str):
    context = pyecm.soem.ecx_contextt(maxslave=512, maxgroup=2)

    ifname = "enx00e04c681629"
    init_result = pyecm.soem.ecx_init(context, ifname)
    assert (
        init_result > 0
    ), f"Error occured on ecx_init ({init_result}). Are you running with admin privledges?"
    print("ecx_init succeeded.")

    num_sub_devices_found = pyecm.soem.ecx_config_init(context, False)
    if num_sub_devices_found == 0:
        raise RuntimeError("No subdevices found!")
    else:
        print(f"found {num_sub_devices_found} subdevices")

    # do config map

    iomap = pyecm.soem.IOMapVector(bytearray(256))
    reqd_iomap_size = pyecm.soem.ecx_config_map_group(context=context, iomap=iomap, group=0)
    assert reqd_iomap_size < len(
        iomap
    ), f"IO Map size is too small. req'd size: {reqd_iomap_size}. configured size: {len(iomap)}"
    print("Successfully configured iomap.")

    # config dc
    dc_subdevice_found = pyecm.soem.ecx_configdc(context)
    if dc_subdevice_found:
        print("Distrubuted clocks configured.")
    else:
        print("No distributed clock enabled subdevices found.")

    lowest_state_found = pyecm.soem.ecx_statecheck(
        context=context,
        slave=0,
        reqstate=4,  # 4 = SAFEOP
        timeout_us=50_000,
    )
    assert (
        lowest_state_found == 4
    ), f"not all subdevices reached SAFEOP. Lowest state: {lowest_state_found}"

    res = pyecm.soem.ecx_send_processdata(context=context)
    assert res > 0, f"error on send process data({res})"
    print("sent first process data")

    wkc = pyecm.soem.ecx_receive_processdata(context=context, timeout_us=2000)
    # assert wkc != -1, f"invalid wkc on first receive process data. wkc: {wkc}"
    # print(f"received first process data. wkc: {wkc}")
    context.slavelist[0]
    pyecm.soem.ecx_writestate(context=context, slave=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyecm simple test")
    parser.add_argument("--ifname", type=str, help="Interface name (e.g., eth0)", required=False)
    args = parser.parse_args()

    if not args.ifname:
        parser.print_help()
        print("Available adapters (use the name of the adapter for this script):")
        for i, adapter in enumerate(pyecm.soem.ec_find_adapters()):
            print(f"Adapter {i}:")
            print(f"name: {adapter.name}")
            print(f"desc: {adapter.desc}")
        sys.exit(1)

    adapters = [adapter.name for adapter in pyecm.soem.ec_find_adapters()]
    assert (
        args.ifname.encode() in adapters
    ), f"ifname: {args.ifname.encode()} not in available adapters: {adapters}"

    cyclic_thread = threading.Thread(target=cyclic_task, daemon=True)
    cyclic_thread.start()
    simpletest(args.ifname)
