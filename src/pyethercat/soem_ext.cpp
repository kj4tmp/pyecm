#include <nanobind/nanobind.h>
#include <ethercat.h>
namespace nb = nanobind;

using namespace nb::literals;

NB_MODULE(soem_ext, m) {
    m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a, "This function adds two numbers and increments if only one is provided.");


    // ethercat.h
    // nothing in here, yeet

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
    

}
