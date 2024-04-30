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

def simpletest(ifname: str):
    context = pyecm.soem.ecx_contextt()

    if pyecm.soem.ecx_init(context, ifname) > 0:
        raise RuntimeError("Error occured on ecx_init. Are you running with admin privledges?")
    else:
        print("ecx_init succeeded.")
    
    num_sub_devices_found = pyecm.soem.ecx_config_init(context, False)
    if  num_sub_devices_found == 0:
        raise RuntimeError("No subdevices found!")
    else:
        print(f"found {num_sub_devices_found} subdevices")

    # do config map

    # config dc
    if pyecm.soem.ecx_configdc(context):
        print("Distrubuted clocks configured.")
    else:
        print("No distributed clock enabled subdevices found.")
    
    

    pass

def ecatcheck():
    pass


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

    ecatcheck_thread = threading.Thread(target=ecatcheck)
    ecatcheck_thread.start()
    simpletest(args.ifname)
        