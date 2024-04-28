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

    //TODO: fill in
    nb::class_<ecx_redportt>(m, "ecx_redportt")
        .def(nb::init<>());

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
    nb::class_<ec_slavet>(m, "ec_slavet")
        .def_rw("state", &ec_slavet::state)
        .def_rw("ALstatuscode", &ec_slavet::ALstatuscode)
        .def_rw("configadr", &ec_slavet::configadr)
        .def_rw("aliasadr", &ec_slavet::aliasadr)
        .def_rw("eep_man", &ec_slavet::eep_man)
        .def_rw("eep_id", &ec_slavet::eep_id)
        .def_rw("eep_rev", &ec_slavet::eep_rev)
        .def_rw("Itype", &ec_slavet::Itype)
        .def_rw("Dtype", &ec_slavet::Dtype)
        .def_rw("Obits", &ec_slavet::Obits)
        .def_rw("Obytes", &ec_slavet::Obytes)
        .def_rw("outputs", &ec_slavet::outputs)
        .def_rw("Ostartbit", &ec_slavet::Ostartbit)
        .def_rw("Ibits", &ec_slavet::Ibits)
        .def_rw("Ibytes", &ec_slavet::Ibytes)
        .def_rw("inputs", &ec_slavet::inputs)
        .def_rw("Istartbit", &ec_slavet::Istartbit)

        .def_ro("name", &ec_slavet::name);

    //TODO: fill in
    nb::class_<ec_groupt>(m, "ec_groupt");

    //TODO: fill in
    nb::class_<ec_eringt>(m, "ec_eringt");

    //TODO: fill in
    nb::class_<ec_idxstackT>(m, "ec_idxstackT");

    //TODO: fill in
    nb::class_<ec_SMcommtypet>(m, "ec_SMcommtypet");

    //TODO: fill in
    nb::class_<ec_PDOassignt>(m, "ec_PDOassignt");

    //TODO: fill in
    nb::class_<ec_PDOdesct>(m, "ec_PDOdesct");

    //TODO: fill in
    nb::class_<ec_eepromSMt>(m, "ec_eepromSMt");

    //TODO: fill in
    nb::class_<ec_eepromFMMUt>(m, "ec_eepromFMMUt");

    //TODO: fill in
    nb::class_<ecx_contextt>(m, "ecx_contextt")
        //.def(nb::init<>())
        .def("__init__", [](ecx_contextt *context)
        {
            char IOmap[4096];

            /** Main slave data array.
             *  Each slave found on the network gets its own record.
             *  ec_slave[0] is reserved for the master. Structure gets filled
             *  in by the configuration function ec_config().
             */
            ec_slavet   ec_slave[EC_MAXSLAVE];
            /** number of slaves found on the network */
            int         ec_slavecount;
            /** slave group structure */
            ec_groupt   ec_groups[EC_MAXGROUP];

            /** cache for EEPROM read functions */
            uint8        esibuf[EC_MAXEEPBUF];
            /** bitmap for filled cache buffer bytes */
            uint32       esimap[EC_MAXEEPBITMAP];
            /** current slave for EEPROM cache buffer */
            ec_eringt    ec_elist;
            ec_idxstackT ec_idxstack;

            /** SyncManager Communication Type struct to store data of one slave */
            ec_SMcommtypet  ec_SMcommtype;
            /** PDO assign struct to store data of one slave */
            ec_PDOassignt   ec_PDOassign;
            /** PDO description struct to store data of one slave */
            ec_PDOdesct     ec_PDOdesc;

            /** buffer for EEPROM SM data */
            ec_eepromSMt ec_SM;
            /** buffer for EEPROM FMMU data */
            ec_eepromFMMUt ec_FMMU;

            /** Global variable TRUE if error available in error stack */
            boolean    EcatError = FALSE;

            int64         ec_DCtime;
            int64         ec_DCtime2;

            ecx_portt      ecx_port;
            context->port = &ecx_port;
            context->slavelist = &ec_slave[0];
            context->slavecount = &ec_slavecount;
            context->maxslave = EC_MAXSLAVE;
            context->grouplist = &ec_groups[0];
            context->maxgroup = EC_MAXGROUP;
            context->esibuf = &esibuf[0];
            context->esimap = &esimap[0];
            context->esislave = 0;
            context->elist = &ec_elist;
            context->idxstack = &ec_idxstack;
            context->ecaterror = &EcatError;
            context->DCtime = &ec_DCtime;
            context->SMcommtype = &ec_SMcommtype;
            context->PDOassign = &ec_PDOassign;
            context->PDOdesc = &ec_PDOdesc;
            context->eepSM = &ec_SM;
            context->eepFMMU = &ec_FMMU;
            context->FOEhook = nullptr;
            context->EOEhook = nullptr;
            context->manualstatechange = 0;
            context->userdata = nullptr;
    })
        .def_rw("port", &ecx_contextt::port)
        .def_prop_ro("slavelist", [](ecx_contextt *context) -> nb::typed<nb::list, ec_slavet> {
            nb::typed<nb::list, ec_slavet> subdevices_list;
            for (int i = 0; i < *(context->slavecount); i++){
                subdevices_list.append(context->slavelist[i]);
            }
            return subdevices_list;
        })
        .def_rw("slavecount", &ecx_contextt::slavecount)
        .def_rw("maxslave", &ecx_contextt::maxslave)
        .def_rw("grouplist", &ecx_contextt::grouplist)
        .def_rw("maxgroup", &ecx_contextt::maxgroup)
        .def_rw("esibuf", &ecx_contextt::esibuf)
        .def_rw("esimap", &ecx_contextt::esimap)
        .def_rw("esislave", &ecx_contextt::esislave)
        .def_rw("elist", &ecx_contextt::elist)
        .def_rw("idxstack", &ecx_contextt::idxstack)
        .def_rw("ecaterror", &ecx_contextt::ecaterror)
        .def_rw("DCtime", &ecx_contextt::DCtime)
        .def_rw("SMcommtype", &ecx_contextt::SMcommtype)
        .def_rw("PDOassign", &ecx_contextt::PDOassign)
        .def_rw("PDOdesc", &ecx_contextt::PDOdesc)
        .def_rw("eepSM", &ecx_contextt::eepSM)
        .def_rw("eepFMMU", &ecx_contextt::eepFMMU)
        //.def_rw("FOEhook", &ecx_contextt::FOEhook);
        //.def_rw("EOEhook", &ecx_contextt::EOEhook)
        .def_rw("manualstatechange", &ecx_contextt::manualstatechange)
        .def_rw("userdata", &ecx_contextt::userdata);

    
    m.def("ecx_init", &ecx_init);
    m.def("ecx_config_init", &ecx_config_init);
    m.def("ecx_close", &ecx_close);
    m.def("ecx_iserror", &ecx_iserror);
    m.def("ecx_init_redundant", [](ecx_contextt *context, ecx_redportt *redport, const char *ifname, const char *if2name) {
        // if2name is incorrectly typed as char * instead of const char *
        // which causes nanobind compile error
        return ecx_init_redundant(context, redport, ifname, (char *)if2name);
        });
    

}
