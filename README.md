# pyecm
An EtherCAT MainDevice in Python, fully free and open source.

| Priority | Goal                                                 | Status   |
|---|------------------------------------------------------|----------|
|1| Fully functional and complete python bindings for the Simple Open EtherCAT Master [SOEM](https://github.com/OpenEtherCATsociety/SOEM) (originally written in C) using [nanobind](https://github.com/wjakob/nanobind) | work in progress  |
|2| Configuration of the MainDevice and SubDevices via an EtherCAT Network Information (ENI) file. | not started  |
|3| Software-in-the-loop (SiL) network simulation capability. | not started  |
|4| Async API.                                           | not started  |


## Development
1. clone repo (and submodules)
1. install vscode
1. install docker desktop
1. install vscode dev containers extension
1. open vscode in repo
1. click reopen in container
1. open new terminal
1. run `pip install . && pytest`

