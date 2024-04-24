#include <nanobind/nanobind.h>
#include <ethercat.h>
namespace nb = nanobind;

using namespace nb::literals;


NB_MODULE(soem_ext, m) {
    m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a);


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


    //nicdrv.h
    //TODO: fill in
    nb::class_<ecx_portt>(m, "ecx_portt");
        

    // ethercatmain.h
    nb::class_<ec_adaptert>(m, "ec_adaptert")
        .def_prop_ro("name", [](ec_adaptert *adp) -> nb::bytes { return nb::bytes(adp->name); })
        .def_prop_ro("desc", [](ec_adaptert *adp) -> nb::bytes { return nb::bytes(adp->desc); });

    m.def("ec_find_adapters", []() -> nb::typed<nb::list, ec_adaptert> {
        ec_adaptert *adapters = ec_find_adapters();
        nb::typed<nb::list, ec_adaptert> adapter_list;
        while (adapters != nullptr) {
            adapter_list.append(adapters);
            adapters = adapters->next;
        }
        ec_free_adapters(adapters);
        return adapter_list;
    });

    //TODO: fill in
    nb::class_<ec_slavet>(m, "ec_slavet");

    //TODO: fill in
    nb::class_<ecx_contextt>(m, "ecx_contextt")
        .def_ro("port", ecx_contextt::port)
        .def_ro("slavelist", &ecx_contextt::slavelist)
        .def_ro("slavecount", &ecx_contextt::slavecount)
        .def_ro("maxslave", &ecx_contextt::maxslave)
        .def_ro("grouplist", &ecx_contextt::grouplist)
        .def_ro("maxgroup", &ecx_contextt::maxgroup)
        .def_ro("esibuf", &ecx_contextt::esibuf)
        .def_ro("esimap", &ecx_contextt::esimap)
        .def_ro("esislave", &ecx_contextt::esislave)
        .def_ro("elist", &ecx_contextt::elist)
        .def_ro("idxstack", &ecx_contextt::idxstack)
        .def_ro("ecaterror", &ecx_contextt::ecaterror)
        .def_ro("DCtime", &ecx_contextt::DCtime)
        .def_ro("SMcommtype", &ecx_contextt::SMcommtype)
        .def_ro("PDOassign", &ecx_contextt::PDOassign)
        .def_ro("PDOdesc", &ecx_contextt::PDOdesc)
        .def_ro("eepSM", &ecx_contextt::eepSM)
        .def_ro("eepFMMU", &ecx_contextt::eepFMMU)
        .def_ro("FOEhook", &ecx_contextt::FOEhook)
        .def_ro("EOEhook", &ecx_contextt::EOEhook)
        .def_ro("manualstatechange", &ecx_contextt::manualstatechange)
        .def_ro("userdata", &ecx_contextt::userdata);
        

    m.def("ecx_init", &ecx_init);
    

}
