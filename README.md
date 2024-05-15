# pyecm
An EtherCAT MainDevice in Python, fully free and open source.

| Priority | Goal                                                 | Status   |
|---|------------------------------------------------------|----------|
|1| Fully functional and complete python bindings for the Simple Open EtherCAT Master [SOEM](https://github.com/OpenEtherCATsociety/SOEM) (originally written in C) using [nanobind](https://github.com/wjakob/nanobind) | work in progress  |
|2| Configuration of the MainDevice and SubDevices via an EtherCAT Network Information (ENI) file. | not started  |
|3| Software-in-the-loop (SiL) network simulation capability. | not started  |
|4| Async API.                                           | not started  |

## Warnings

This library is extremely early in development.

We will follow semantic versioning. Expect drastic changes to the API prior to v1.0.0.


## Installation

Windows / Mac OSX compatibility is intended for developer convenience only. The intended targets are linux with PREEMPT_RT patches. Typically, the easiest to work with is Debian since pre-compiled patches are available from the repositories.

```
pip install pyecm
```
### Windows
Windows requires installation of an additional dependency npcap. https://npcap.com/

Please install it in winpcap compatibility mode (I believe this is the default configuration.)

## Usage

On a typical windows system:

```
C:\repos\pyecm>python examples/soem/simple_test.py --ifname "\Device\NPF_{6F17F41B-E756-4470-B7B8-74A3504B4F7B}"
```

will output something like:

```
C:\repos\pyecm>python examples/soem/simple_test.py --ifname "\Device\NPF_{6F17F41B-E756-4470-B7B8-74A3504B4F7B}"
simple_test.py args=Namespace(ifname='\\Device\\NPF_{6F17F41B-E756-4470-B7B8-74A3504B4F7B}', if2name=None)
ecx_init succeeded.
found 5 subdevices:
network summary:
position|configadr|aliasadr|name ---|manufacturer|product|revision
       0|main device
       1|0x1001   |0x0     |EK1100                  |0x2       |0x44c2c52 |0x100000  
       2|0x1002   |0x0     |EL3314                  |0x2       |0xcf23052 |0x120000  
       3|0x1003   |0x0     |EL2088                  |0x2       |0x8283052 |0x110000  
       4|0x1004   |0x0     |EL3681                  |0x2       |0xe613052 |0x120000  
       5|0x1005   |0x0     |EL3204                  |0x2       |0xc843052 |0x110000  
reached state: 2
successfully configured iomap. iomap size: 66
distrubuted clocks configured
reached state: 4
reached state: OPERATIONAL
started main operation
iomap:  [0 0 0 ... 0 0 0]
```

## Development
1. clone repo (and submodules)

    > use `git clone <repo clone url> --recursive`


1. install vscode
1. install docker desktop
1. install vscode dev containers extension
1. open vscode in repo
1. click reopen in container
1. open new terminal
1. run `pip install . && pytest`

