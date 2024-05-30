"""
A re-write of SOEM example slaveinfo.c in python.
"""

import argparse
import sys

import pyecm


def subdevice_info(ifname: str):
    # create soem
    # manual state change means SOEM will not request PREOP automatically on config map
    main_device = pyecm.soem.SOEM(
        max_subdevices=512, maxgroup=2, iomap_size_bytes=4096, manualstatechange=False
    )

    # set network interface
    init_result = main_device.init(ifname)
    assert (
        init_result > 0
    ), f"error occured on init ({init_result}). are you running with admin privledges?"
    print("ecx_init succeeded.")

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
    main_device.subdevices[0].state = pyecm.soem.ec_state.PRE_OP
    main_device.writestate(subdevice=0)
    lowest_state_found = main_device.statecheck(
        subdevice=0,
        reqstate=pyecm.soem.ec_state.PRE_OP,
        timeout_us=2000,
    )
    assert (
        lowest_state_found == pyecm.soem.ec_state.PRE_OP
    ), f"not all subdevices reached PREOP! lowest state found: {pyecm.soem.ec_state(lowest_state_found).name}"
    print(f"reached state: {pyecm.soem.ec_state(lowest_state_found).name}")

    # create iomap
    required_iomap_size_bytes = main_device.config_overlap_map()
    assert (
        required_iomap_size_bytes <= main_device.iomap.size  # type: ignore
    ), f"io map size is too small. required size: {required_iomap_size_bytes}. configured size: {main_device.iomap.size}"  # type: ignore
    print(f"successfully configured iomap. iomap size: {required_iomap_size_bytes}")

    # config dc
    dc_subdevice_found = main_device.configdc()
    if dc_subdevice_found:
        print("distrubuted clocks configured")
    else:
        print("no distributed clock enabled subdevices found")

    # print errors

    while main_device.iserror():
        _, error = main_device.poperror()
        print(f"Subdevice error. {error.subdevice}, type: {error.Etype}")
        # TODO: print more information here

    main_device.statecheck(0, reqstate=pyecm.soem.ec_state.SAFE_OP, timeout_us=10_000_000)
    if main_device.subdevices[0].state != pyecm.soem.ec_state.SAFE_OP:

        main_device.readstate()
        for i, subdevice in enumerate(main_device.subdevices[: main_device.subdevice_count + 1]):
            if i != 0:
                print(
                    f"Subdevice {i}, state: {subdevice.state}, statuscode: {subdevice.ALstatuscode}"
                )
        raise RuntimeError(
            f"Not all subdevices reached SAFEOP. Lowest state: {main_device.subdevices[0].state}"
        )

    main_device.readstate()

    for i, subdevice in enumerate(main_device.subdevices[: main_device.subdevice_count + 1]):
        if i != 0:

            print(
                f"Subdevice:{i}\n Name:{subdevice.name}\n Output size: {subdevice.Obits}bits\n Input size: {subdevice.Ibits}bits\n State: {subdevice.state}\n Delay: {subdevice.pdelay}[ns]\n Has DC: {subdevice.hasdc}"
            )
            if subdevice.hasdc:
                print(f" DCParentport:{subdevice.parentport}")
            print(
                f" Activeports:{bool(subdevice.activeports & 0x01)}.{bool(subdevice.activeports & 0x02)}.{bool(subdevice.activeports & 0x04)}.{bool(subdevice.activeports & 0x08)}"
            )
            print(f" Configured address: {subdevice.configadr}")
            print(f" Man: {subdevice.eep_man} ID: {subdevice.eep_id} Rev: {subdevice.eep_rev}")
            for j, sm in enumerate(subdevice.SM):
                if sm.StartAddr > 0:
                    print(
                        f" SM{j} A:{sm.StartAddr:04x} L:{sm.SMlength:04d} F:{sm.SMflags:08x} Type:{subdevice.SMtype[j]}"
                    )
            for j in range(subdevice.FMMUunused):
                print(
                    f" FMMU{j} Ls:{subdevice.FMMU[j].LogStart:08x} Ll:{subdevice.FMMU[j].LogLength:04d} Lsb:{subdevice.FMMU[j].LogStartbit} Leb:{subdevice.FMMU[j].LogEndbit} Ps:{subdevice.FMMU[j].PhysStart:04x} Psb:{subdevice.FMMU[j].PhysStartBit} Ty:{subdevice.FMMU[j].FMMUtype:02x} Act:{subdevice.FMMU[j].FMMUactive:02x}"
                )
            print(
                f" FMMUfunc 0:{subdevice.FMMU0func} 1:{subdevice.FMMU1func} 2:{subdevice.FMMU2func} 3:{subdevice.FMMU3func}"
            )
            print(
                f" MBX length wr: {subdevice.mbx_l} rd: {subdevice.mbx_rl} MBX protocols : {subdevice.mbx_proto:02x}"
            )


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
    args = parser.parse_args()

    print(f"simple_test.py {args=}")

    if not args.ifname:
        parser.print_help()
        print("Available adapters (use the name of the adapter for this script):")
        for i, adapter in enumerate(pyecm.soem.ec_find_adapters()):
            print(f"    Adapter {i}:")
            print(f"        name: {adapter.name}")
            print(f"        desc: {adapter.desc}")
        sys.exit(1)

    # check ifname in available adapters
    adapters = [adapter.name for adapter in pyecm.soem.ec_find_adapters()]
    assert args.ifname in adapters, f"ifname: {args.ifname} not in available adapters: {adapters}"

    subdevice_info(args.ifname)
