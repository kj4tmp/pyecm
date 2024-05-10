"""
A re-write of simple_test.c from SOEM in python.
"""

import argparse
import sys
import threading
import time

import pyecm
from pyecm.soem import SOEM


def cyclic_task(main_device: pyecm.soem.SOEM):

    expected_wkc = (main_device.grouplist[0].outputsWKC * 2) + main_device.grouplist[0].inputsWKC

    while True:
        pyecm.soem.osal_usleep(10000)  # run 10 ms cycle
        try:
            res = main_device.send_processdata()
            assert res > 0, f"error on send process data({res})"
            wkc = main_device.receive_processdata(timeout_us=2000)
            if wkc != expected_wkc:
                print(f"invalid wkc!: {wkc}. expected: {expected_wkc}")

        except Exception as e:
            print("exception in cyclic task")
            print(e)


def start_main_operation(main_device: pyecm.soem.SOEM):
    # all subdevices will be in OP before entering this function
    print("started main operation")

    cyclic_task_thread = threading.Thread(target=cyclic_task, args=[main_device], daemon=True)
    cyclic_task_thread.start()
    cyclic_task_thread.join()


def simpletest(ifname: str):
    main_device = SOEM(maxslave=512, maxgroup=2, iomap_size_bytes=4096, manualstatechange=False)
    init_result = main_device.init(ifname)
    assert (
        init_result > 0
    ), f"Error occured on ecx_init ({init_result}). Are you running with admin privledges?"
    print("ecx_init succeeded.")

    num_sub_devices_found = main_device.config_init(False)
    if num_sub_devices_found == 0:
        raise RuntimeError("No subdevices found!")
    else:
        print(f"found {num_sub_devices_found} subdevices")
    for i, subdevice in enumerate(main_device.slavelist):
        if i <= main_device.slavecount:
            if i == 0:
                print(f"    {i}| main device")
            else:
                print(
                    f"    {i}|{hex(subdevice.configadr)}|{hex(subdevice.aliasadr)} name: {subdevice.name} manufacturer: {hex(subdevice.eep_man)} product: {hex(subdevice.eep_id)} revision: {hex(subdevice.eep_rev)}"
                )
        else:
            break

    # do config map
    reqd_iomap_size = main_device.config_overlap_map()

    assert (
        reqd_iomap_size <= main_device.iomap.size
    ), f"IO Map size is too small. req'd size: {reqd_iomap_size}. configured size: {main_device.iomap.size}"
    print(f"Successfully configured iomap. iomap size: {reqd_iomap_size}")
    print("iomap: ", main_device.iomap)

    # config dc
    dc_subdevice_found = main_device.configdc()
    if dc_subdevice_found:
        print("Distrubuted clocks configured.")
    else:
        print("No distributed clock enabled subdevices found.")

    lowest_state_found = main_device.statecheck(
        slave=0,
        reqstate=4,  # 4 = SAFEOP
        timeout_us=2000,
    )
    assert (
        lowest_state_found == 4
    ), f"not all subdevices reached SAFEOP. Lowest state: {lowest_state_found}"

    res = main_device.send_processdata()
    assert res > 0, f"error on send process data({res})"
    print("sent first process data")

    wkc = main_device.receive_processdata(timeout_us=2000)
    # assert wkc != -1, f"invalid wkc on first receive process data. wkc: {wkc}"
    # print(f"received first process data. wkc: {wkc}")
    main_device_entry = main_device.slavelist[0]
    main_device_entry.state = 8  # 8 = OP
    main_device.slavelist[0] = main_device_entry
    main_device.writestate(slave=0)

    for _ in range(200):
        res = main_device.send_processdata()
        assert res > 0, f"error on send process data({res})"
        main_device.receive_processdata(timeout_us=2000)
        lowest_state_found = main_device.statecheck(
            slave=0,
            reqstate=8,  # 8 = OP
            timeout_us=2000,
        )
        if lowest_state_found == 8:
            break
        print(f"attempting to reach OP. lowest state found: {lowest_state_found}")
    assert (
        lowest_state_found == 8
    ), f"not all subdevices reached OP. Lowest state: {lowest_state_found}"
    print("all subdevices reached OP")
    # print(main_device.iomap)

    start_main_operation(main_device)


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

    simpletest(args.ifname)
