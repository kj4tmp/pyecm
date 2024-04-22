#include <nanobind/nanobind.h>
#include <ethercat.h>
namespace nb = nanobind;

using namespace nb::literals;

nb::list wrap_ec_find_adapters() {
        ec_adaptert *adapters = ec_find_adapters();

        nb::list adapter_list;
        while (adapters != nullptr) {
            nb::dict adapter_dict;
            adapter_dict["name"] = std::string(adapters->name);
            adapter_dict["desc"] = std::string(adapters->desc);
            adapter_list.append(adapters->name);
            adapters = adapters->next;
        }

        return adapter_list;
    }


NB_MODULE(soem_ext, m) {
    m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a, "This function adds two numbers and increments if only one is provided.");


    // ethercat.h
    // nothing in here, yeet

    // from osal.h
    nb::class_<ec_timet> (m, "ec_timet")
        .def(nb::init<>())
        .def_rw("sec", &ec_timet::sec)
        .def_rw("usec", &ec_timet::usec);

    // ethercattype.h
    nb::enum_<ec_err_type> (m, "ec_err_type")
        .value("EC_ERR_TYPE_SDO_ERROR", ec_err_type::EC_ERR_TYPE_SDO_ERROR)
        .value("EC_ERR_TYPE_EMERGENCY", ec_err_type::EC_ERR_TYPE_EMERGENCY)
        .value("EC_ERR_TYPE_PACKET_ERROR", ec_err_type::EC_ERR_TYPE_PACKET_ERROR)
        .value("EC_ERR_TYPE_SDOINFO_ERROR", ec_err_type::EC_ERR_TYPE_FOE_ERROR)
        .value("EC_ERR_TYPE_FOE_ERROR", ec_err_type::EC_ERR_TYPE_FOE_ERROR)
        .value("EC_ERR_TYPE_FOE_BUF2SMALL", ec_err_type::EC_ERR_TYPE_FOE_BUF2SMALL)
        .value("EC_ERR_TYPE_FOE_PACKET_NUMBER", ec_err_type::EC_ERR_TYPE_FOE_PACKETNUMBER)
        .value("EC_ERR_TYPE_SOE_ERROR", ec_err_type::EC_ERR_TYPE_SOE_ERROR)
        .value("EC_ERR_TYPE_MBX_ERROR", ec_err_type::EC_ERR_TYPE_MBX_ERROR)
        .value("EC_ERR_TYPE_FOE_FILE_NOTFOUND", ec_err_type::EC_ERR_TYPE_FOE_FILE_NOTFOUND)
        .value("EC_ERR_TYPE_EOE_INVALID_RX_DATA", ec_err_type::EC_ERR_TYPE_EOE_INVALID_RX_DATA);
    
    nb::enum_<ec_state> (m, "ec_state")
        .value("EC_STATE_NONE", ec_state::EC_STATE_NONE)
        .value("EC_STATE_INIT", ec_state::EC_STATE_INIT)
        .value("EC_STATE_PRE_OP", ec_state::EC_STATE_PRE_OP)
        .value("EC_STATE_BOOT", ec_state::EC_STATE_BOOT)
        .value("EC_STATE_SAFE_OP", ec_state::EC_STATE_SAFE_OP)
        .value("EC_STATE_OPERATIONAL", ec_state::EC_STATE_OPERATIONAL)
        .value("EC_STATE_ACK", ec_state::EC_STATE_ACK)
        .value("EC_STATE_ERROR", ec_state::EC_STATE_ERROR);


    nb::class_<ec_errort>(m, "ec_errort")
        .def(nb::init<>())
        .def_rw("Time", &ec_errort::Time)
        .def_rw("Signal", &ec_errort::Signal)
        .def_rw("Slave", &ec_errort::Slave)
        .def_rw("Index", &ec_errort::Index)
        .def_rw("SubIdx", &ec_errort::SubIdx)
        .def_rw("Etype", &ec_errort::Etype)
        .def_rw("AbortCode", &ec_errort::AbortCode)
        .def_rw("ErrorCode", &ec_errort::ErrorCode)
        .def_rw("ErrorReg", &ec_errort::ErrorReg)
        .def_rw("b1", &ec_errort::b1)
        .def_rw("w1", &ec_errort::w1)
        .def_rw("w2", &ec_errort::w2);


    // ethercatmain.h
    // nb::class_<ec_adapter>(m, "ec_adapter")
    //      .def_rw("name", &ec_adapter::name)
    //      .def_rw("desc", &ec_adapter::desc)
    //      .def_rw("next", &ec_adapter::next);

    // Define the wrapper function for ec_find_adapters
    

    m.def("ec_find_adapters", &wrap_ec_find_adapters, "Find adapters and return as a list of dictionaries");

}
