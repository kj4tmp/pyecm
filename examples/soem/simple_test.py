"""
A re-write of simple_test.c from SOEM in python.
"""

import argparse
import sys
import threading
import time

import pyecm
from pyecm.soem import SOEM, ec_state


def maintainance_task(main_device: SOEM):
    while True:
        time.sleep(0.5)  # run every 500 ms

        main_device.readstate()  # read state of all subdevices into main_device.subdevices

        for subdevice in main_device.subdevices[
            1 : main_device.subdevice_count + 1
        ]:  # index 0 is reserved for main_device
            if subdevice.state == ec_state.SAFE_OP + ec_state.ERROR:
                # write SAFEOP + ACK
                pass
            elif subdevice.state == ec_state.SAFE_OP:
                pass
                # write OP
            elif subdevice.state == ec_state.NONE:
                # reconfig
                pass

    pass


def cyclic_task(main_device: SOEM):

    expected_wkc = (main_device.grouplist[0].outputsWKC * 2) + main_device.grouplist[0].inputsWKC

    last_iomap_print_time = time.perf_counter()
    while True:
        time.sleep(0.01)  # run 10 ms cycle
        try:
            res = main_device.send_overlap_processdata_group(0)
            assert res > 0, f"error on send process data({res})"
            wkc = main_device.receive_processdata_group(0, timeout_us=2000)
            if wkc != expected_wkc:
                print(f"invalid wkc!: {wkc}. expected: {expected_wkc}")

            if time.perf_counter() - last_iomap_print_time > 5:
                print("iomap: ", main_device.iomap)
                last_iomap_print_time = time.perf_counter()
        except Exception as e:
            print("exception in cyclic task")
            print(e)


def start_cyclic_operation(main_device: pyecm.soem.SOEM):
    # all subdevices will be in OP before entering this function
    print("started main operation")

    cyclic_task_thread = threading.Thread(target=cyclic_task, args=[main_device], daemon=True)
    cyclic_task_thread.start()
    cyclic_task_thread.join()


def simpletest(ifname: str, if2name: str | None):
    # create soem
    # manual state change means SOEM will not request PREOP automatically on config map
    main_device = SOEM(
        max_subdevices=512, maxgroup=2, iomap_size_bytes=4096, manualstatechange=False
    )

    # set network interface
    if not if2name:
        init_result = main_device.init(ifname)
        assert (
            init_result > 0
        ), f"error occured on init ({init_result}). are you running with admin privledges?"
        print("ecx_init succeeded.")
    else:
        red_init_result = main_device.init_redundant(ifname, if2name)
        assert (
            red_init_result > 0
        ), f"error occured on init_redundant ({red_init_result}). are you running with admin privledges?"
        print("init_redundant succeeded.")

    # find subdevices
    # requests INIT!
    num_sub_devices_found = main_device.config_init()
    if num_sub_devices_found <= 0:
        raise RuntimeError("no subdevices found!")
    else:
        print(f"found {num_sub_devices_found} subdevices:")

    # check not exceeded max_subdevices
    max_allowable_subdevices = main_device.max_subdevices - 1  # index 0 is reserved for main device
    assert (
        num_sub_devices_found <= max_allowable_subdevices
    ), f"number of subdevices found exceeds max allowable: {max_allowable_subdevices}"

    # print info about subdevices
    print("network summary:")
    print("position|configadr|aliasadr|name ---|manufacturer|product|revision")
    for i, subdevice in enumerate(main_device.subdevices):
        if i <= main_device.subdevice_count:
            if i == 0:
                pass
                print(f"{i:8}|main device")
            else:
                print(
                    f"{i:8}|{hex(subdevice.configadr):9}|{hex(subdevice.aliasadr):8}|{subdevice.name:<24}|{hex(subdevice.eep_man):10}|{hex(subdevice.eep_id):10}|{hex(subdevice.eep_rev):10}"
                )
        else:
            break

    # request and verify PREOP state
    main_device.get_subdevice(0).state = ec_state.PRE_OP
    main_device.writestate(subdevice=0)
    lowest_state_found = main_device.statecheck(
        subdevice=0,
        reqstate=pyecm.soem.ec_state.PRE_OP,
        timeout_us=2000,
    )
    assert (
        lowest_state_found == ec_state.PRE_OP
    ), f"not all subdevices reached PREOP! lowest state found: {ec_state(lowest_state_found).name}"
    print(f"reached state: {ec_state(lowest_state_found)}")

    # create iomap
    required_iomap_size_bytes = main_device.config_overlap_map()
    assert (
        required_iomap_size_bytes <= main_device.iomap.size  # type: ignore
    ), f"io map size is too small. required size: {required_iomap_size_bytes}. configured size: {main_device.iomap.size}"
    print(f"successfully configured iomap. iomap size: {required_iomap_size_bytes}")

    # config dc
    dc_subdevice_found = main_device.configdc()
    if dc_subdevice_found:
        print("distrubuted clocks configured")
    else:
        print("no distributed clock enabled subdevices found")

    # request and verify SAFEOP
    main_device.get_subdevice(0).state = ec_state.SAFE_OP
    main_device.writestate(subdevice=0)
    lowest_state_found = main_device.statecheck(
        subdevice=0,
        reqstate=pyecm.soem.ec_state.SAFE_OP,
        timeout_us=2000,
    )
    assert (
        lowest_state_found == ec_state.SAFE_OP
    ), f"Not all subdevices reached SAFEOP! Lowest state found: {ec_state(lowest_state_found).name}"
    print(f"reached state: {ec_state(lowest_state_found)}")

    # request and verify OP
    # need to send at least one set of process data
    res = main_device.send_overlap_processdata_group(0)
    assert res > 0, f"error on send process data({res})"
    wkc = main_device.receive_processdata_group(0, timeout_us=2000)

    main_device.get_subdevice(0).state = ec_state.OPERATIONAL
    main_device.writestate(subdevice=0)

    for _ in range(200):
        res = main_device.send_overlap_processdata_group(0)
        assert res > 0, f"error on send process data({res})"
        main_device.receive_processdata_group(0, timeout_us=2000)
        lowest_state_found = main_device.statecheck(
            subdevice=0,
            reqstate=ec_state.OPERATIONAL,
            timeout_us=2000,
        )
        if lowest_state_found == ec_state.OPERATIONAL:
            break
        print(f"attempting to reach OP. lowest state found: {ec_state(lowest_state_found).name}")
    assert (
        lowest_state_found == ec_state.OPERATIONAL
    ), f"not all subdevices reached OP. Lowest state: {ec_state(lowest_state_found).name}"
    print(f"reached state: {ec_state(lowest_state_found).name}")

    # print(main_device.iomap)

    start_cyclic_operation(main_device)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyecm simple test")
    windows_example_interface_name = (
        '"' + r"\Device\NPF_{6F17F41B-E756-4470-B7B8-74A3504B4F7B}" + '"'
    )
    parser.add_argument(
        "--ifname",
        type=str,
        help=f"Interface name (e.g., eth0, {windows_example_interface_name})",
        required=False,
    )

    parser.add_argument(
        "--if2name",
        type=str,
        help="Redundant interface name (e.g., eth1)",
        required=False,
    )
    args = parser.parse_args()

    print(f"simple_test.py {args=}")

    if not args.ifname:
        parser.print_help()
        print("Available adapters (use the name of the adapter for this script):")
        for i, adapter in enumerate(pyecm.soem.ec_find_adapters()):
            print(f"Adapter {i}:")
            print(f"name: {adapter.name}")
            print(f"desc: {adapter.desc}")
        sys.exit(1)

    # check ifname in available adapters
    adapters = [adapter.name for adapter in pyecm.soem.ec_find_adapters()]
    assert args.ifname in adapters, f"ifname: {args.ifname} not in available adapters: {adapters}"

    if args.if2name:
        assert (
            args.if2name in adapters
        ), f"if2name: {args.if2name} not in available adapters: {adapters}"

    assert args.ifname != args.if2name, "ifname and if2name cannot be the same."

    simpletest(args.ifname, args.if2name)
