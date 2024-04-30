"""
A re-write of simple_test.c from SOEM in python.
"""
import argparse
import threading

import pyecm


def simpletest(ifname: str):
    pass

def ecatcheck():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyecm simple test")
    parser.add_argument("ifname", type=str, help="Interface name (e.g., eth0)")
    args = parser.parse_args()

    if args.ifname:
        # create thread to handle slave error handling in OP
        ecatcheck_thread = threading.Thread(target=ecatcheck)
        ecatcheck_thread.start()
        simpletest(args.ifname)
    else:
        print("Available adapters:")
        for i, adapter in enumerate(pyecm.soem.ec_find_adapters()):
            print(f"Adapter {i}:")
            print(f"name: {adapter.name}")
            print(f"desc: {adapter.desc}")