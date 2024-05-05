#include <nanobind/nanobind.h>
#include <nanobind/stl/bind_vector.h>
#include <nanobind/stl/vector.h>
#include <ethercat.h>
#include <memory>
namespace nb = nanobind;

using namespace nb::literals;

using IOMapVector = std::vector<uint8_t>;

NB_MAKE_OPAQUE(IOMapVector)

NB_MODULE(soem_ext, m)
{
    m.def(
        "add", [](int a, int b)
        { return a + b; },
        "a"_a, "b"_a);

    // ethercat.h
    // nothing in here, yeet

    // from osal.h
    nb::class_<ec_timet>(m, "ec_timet")
        .def_rw("sec", &ec_timet::sec)
        .def_rw("usec", &ec_timet::usec);

    // ethercattype.h
    nb::enum_<ec_err_type>(m, "ec_err_type")
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

    nb::enum_<ec_state>(m, "ec_state")
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

    // nicdrv.h
    // TODO: fill in
    nb::class_<ecx_portt>(m, "ecx_portt");

    // TODO: fill in
    nb::class_<ecx_redportt>(m, "ecx_redportt")
        .def(nb::init<>());

    // ethercatmain.h
    nb::class_<ec_adaptert>(m, "ec_adaptert")
        .def_prop_ro("name", [](ec_adaptert *adp) -> nb::bytes
                     { return nb::bytes(adp->name); })
        .def_prop_ro("desc", [](ec_adaptert *adp) -> nb::bytes
                     { return nb::bytes(adp->desc); });

    m.def("ec_find_adapters", []() -> nb::typed<nb::list, ec_adaptert>
          {
        ec_adaptert *adapters = ec_find_adapters();
        nb::typed<nb::list, ec_adaptert> adapter_list;
        while (adapters != nullptr) {
            adapter_list.append(adapters);
            adapters = adapters->next;
        }
        ec_free_adapters(adapters);
        return adapter_list; });

    // TODO: fill in
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
        //.def_rw("SM", &ec_slavet::SM)
        //.def_rw("SMtype", &ec_slavet::SMtype)
        //.def_rw("FMMU", &ec_slavet::FMMU)
        .def_rw("FMMU0func", &ec_slavet::FMMU0func)
        .def_rw("FMMU1func", &ec_slavet::FMMU1func)
        .def_rw("FMMU2func", &ec_slavet::FMMU2func)
        .def_rw("FMMU3func", &ec_slavet::FMMU3func)
        .def_rw("mbx_l", &ec_slavet::mbx_l)
        .def_rw("mbx_wo", &ec_slavet::mbx_wo)
        .def_rw("mbx_rl", &ec_slavet::mbx_rl)
        .def_rw("mbx_ro", &ec_slavet::mbx_ro)
        .def_rw("mbx_proto", &ec_slavet::mbx_proto)
        .def_rw("mbx_cnt", &ec_slavet::mbx_cnt)
        .def_rw("hasdc", &ec_slavet::hasdc)
        .def_rw("ptype", &ec_slavet::ptype)
        .def_rw("topology", &ec_slavet::topology)
        .def_rw("activeports", &ec_slavet::activeports)
        .def_rw("consumedports", &ec_slavet::consumedports)
        .def_rw("parent", &ec_slavet::parent)
        .def_rw("parentport", &ec_slavet::parentport)
        .def_rw("entryport", &ec_slavet::entryport)
        .def_rw("DCrtA", &ec_slavet::DCrtA)
        .def_rw("DCrtB", &ec_slavet::DCrtB)
        .def_rw("DCrtC", &ec_slavet::DCrtC)
        .def_rw("DCrtD", &ec_slavet::DCrtD)
        .def_rw("pdelay", &ec_slavet::pdelay)
        .def_rw("DCnext", &ec_slavet::DCnext)
        .def_rw("DCprevious", &ec_slavet::DCprevious)
        .def_rw("DCcycle", &ec_slavet::DCcycle)
        .def_rw("DCshift", &ec_slavet::DCshift)
        .def_rw("DCactive", &ec_slavet::DCactive)
        .def_rw("configindex", &ec_slavet::configindex)
        .def_rw("SIIindex", &ec_slavet::SIIindex)
        .def_rw("eep_8byte", &ec_slavet::eep_8byte)
        .def_rw("eep_pdi", &ec_slavet::eep_pdi)
        .def_rw("CoEdetails", &ec_slavet::CoEdetails)
        .def_rw("FoEdetails", &ec_slavet::FoEdetails)
        .def_rw("EoEdetails", &ec_slavet::EoEdetails)
        .def_rw("SoEdetails", &ec_slavet::SoEdetails)
        .def_rw("Ebuscurrent", &ec_slavet::Ebuscurrent)
        .def_rw("blockLRW", &ec_slavet::blockLRW)
        .def_rw("group", &ec_slavet::group)
        .def_rw("FMMUunused", &ec_slavet::FMMUunused)
        .def_rw("islost", &ec_slavet::islost)
        //.def_rw("PO2SOconfig", &ec_slavet::PO2SOconfig)
        //.def_rw("PO2SOconfigx", &ec_slavet::PO2SOconfigx)
        .def_ro("name", &ec_slavet::name);

    // TODO: fill in
    nb::class_<ec_groupt>(m, "ec_groupt")
        .def_rw("logstartaddr", &ec_groupt::logstartaddr)
        .def_rw("Obytes", &ec_groupt::Obytes)
        .def_rw("outputs", &ec_groupt::outputs)
        .def_rw("Ibytes", &ec_groupt::Ibytes)
        .def_rw("inputs", &ec_groupt::inputs)
        .def_rw("hasdc", &ec_groupt::hasdc)
        .def_rw("DCnext", &ec_groupt::DCnext)
        .def_rw("Ebuscurrent", &ec_groupt::Ebuscurrent)
        .def_rw("blockLRW", &ec_groupt::blockLRW)
        .def_rw("nsegments", &ec_groupt::nsegments)
        .def_rw("Isegment", &ec_groupt::Isegment)
        .def_rw("Ioffset", &ec_groupt::Ioffset)
        .def_rw("outputsWKC", &ec_groupt::outputsWKC)
        .def_rw("inputsWKC", &ec_groupt::inputsWKC)
        .def_rw("docheckstate", &ec_groupt::docheckstate);
    //.def_rw("IOsegment", &ec_groupt::IOsegment);

    // TODO: fill in
    nb::class_<ec_eringt>(m, "ec_eringt");

    // TODO: fill in
    nb::class_<ec_idxstackT>(m, "ec_idxstackT");

    // TODO: fill in
    nb::class_<ec_SMcommtypet>(m, "ec_SMcommtypet");

    // TODO: fill in
    nb::class_<ec_PDOassignt>(m, "ec_PDOassignt");

    // TODO: fill in
    nb::class_<ec_PDOdesct>(m, "ec_PDOdesct");

    nb::class_<ec_eepromSMt>(m, "ec_eepromSMt")
        .def(nb::init<>())
        .def_rw("Startpos", &ec_eepromSMt::Startpos)
        .def_rw("nSM", &ec_eepromSMt::nSM)
        .def_rw("PhStart", &ec_eepromSMt::PhStart)
        .def_rw("Plength", &ec_eepromSMt::Plength)
        .def_rw("Creg", &ec_eepromSMt::Creg)
        .def_rw("Sreg", &ec_eepromSMt::Sreg)
        .def_rw("Activate", &ec_eepromSMt::Activate)
        .def_rw("PDIctrl", &ec_eepromSMt::PDIctrl);

    nb::class_<ec_eepromFMMUt>(m, "ec_eepromFMMUt")
        .def(nb::init<>())
        .def_rw("Startpos", &ec_eepromFMMUt::Startpos)
        .def_rw("nFMMU", &ec_eepromFMMUt::nFMMU)
        .def_rw("FMMU0", &ec_eepromFMMUt::FMMU0)
        .def_rw("FMMU1", &ec_eepromFMMUt::FMMU1)
        .def_rw("FMMU2", &ec_eepromFMMUt::FMMU2)
        .def_rw("FMMU3", &ec_eepromFMMUt::FMMU3);

    // TODO: fill in
    nb::class_<ecx_contextt>(m, "ecx_contextt")
        //.def(nb::init<>())
        .def(
            "__init__", [](ecx_contextt *context, uint16_t maxslave, uint8_t maxgroup)
            {
            if (maxslave == 0) {
                throw std::invalid_argument("maxslave cannot be zero.");
            }
            if (maxgroup == 0) {
                throw std::invalid_argument("maxgroup cannot be zero.");
            }
            context->port = new ecx_portt();
            context->slavelist = new ec_slavet[maxslave];
            context->slavecount = new int;
            context->maxslave = maxslave;
            context->grouplist = new ec_groupt[maxgroup];
            context->maxgroup = maxgroup;
            context->esibuf = new uint8_t[EC_MAXEEPBUF];
            context->esimap = new uint32_t[EC_MAXEEPBITMAP];
            context->esislave = 0;
            context->elist = new ec_eringt;
            context->idxstack = new ec_idxstackT;
            context->ecaterror = new boolean(false);
            context->DCtime = new int64_t;
            context->SMcommtype = new ec_SMcommtypet;
            context->PDOassign = new ec_PDOassignt;
            context->PDOdesc = new ec_PDOdesct;
            context->eepSM = new ec_eepromSMt;
            context->eepFMMU = new ec_eepromFMMUt;
            context->FOEhook = nullptr;
            context->EOEhook = nullptr;
            context->manualstatechange = 0;
            context->userdata = nullptr; },
            "maxslave"_a, "maxgroup"_a)
        .def_rw("port", &ecx_contextt::port)
        .def_prop_ro("slavelist", [](ecx_contextt *context) -> nb::typed<nb::list, ec_slavet>
                     {
            nb::typed<nb::list, ec_slavet> subdevices_list;
            // first subdevice in slavelist is reserved for the maindevice.
            for (int i = 0; i < *(context->slavecount) + 1; i++){
                subdevices_list.append(context->slavelist[i]);
            }
            return subdevices_list; })
        .def_rw("slavecount", &ecx_contextt::slavecount)
        .def_rw("maxslave", &ecx_contextt::maxslave)
        .def_prop_rw(
            "grouplist", [](ecx_contextt &context) -> nb::typed<nb::list, ec_groupt>
            {
            nb::typed<nb::list, ec_groupt> grouplist;
            for (int i = 0; i < context.maxgroup; i++){
                grouplist.append(context.grouplist[i]);
            }
            return grouplist; },
            [](ecx_contextt &context, std::vector<ec_groupt> grouplist)
            {
                if (grouplist.size() > context.maxgroup)
                {
                    throw std::invalid_argument("attempted to set grouplist having length larger than maxgroup");
                }
                for (std::size_t i = 0; i < grouplist.size(); i++)
                {
                    context.grouplist[i] = grouplist[i];
                }
            })
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

    m.def("ecx_close", &ecx_close);
    m.def("ecx_iserror", &ecx_iserror);
    m.def("ecx_init_redundant", [](ecx_contextt *context, ecx_redportt *redport, const char *ifname, const char *if2name)
          {
        // if2name is incorrectly typed as char * instead of const char *
        // which causes nanobind compile error
        return ecx_init_redundant(context, redport, ifname, (char *)if2name); });
    m.def("ecx_readstate", &ecx_readstate);
    m.def("ecx_writestate", &ecx_writestate);

    m.def("ecx_send_overlap_processdata_group", &ecx_send_overlap_processdata_group, "context"_a, "group"_a);
    m.def("ecx_receive_processdata_group", &ecx_receive_processdata_group, "context"_a, "group"_a, "timeout"_a);
    m.def("ecx_send_processdata", &ecx_send_processdata, "context"_a);
    m.def("ecx_send_overlap_processdata", &ecx_send_overlap_processdata, "context"_a);
    m.def("ecx_receive_processdata", &ecx_receive_processdata, "context"_a, "timeout"_a);
    m.def("ecx_send_processdata_group", &ecx_send_processdata_group, "context"_a, "group"_a);


    // ethercatconfig.h
    nb::bind_vector<IOMapVector>(m, "IOMapVector");
    m.def("ecx_init", &ecx_init, "context"_a, "ifname"_a);
    m.def("ecx_config_init", &ecx_config_init, "context"_a, "usetable"_a);
    m.def(
        "ecx_config_map_group", [](ecx_contextt *context, IOMapVector IOmap, uint8 group)
        { return ecx_config_overlap_map_group(context, IOmap.data(), group); },
        "context"_a, "iomap"_a, "group"_a);
    m.def("ecx_config_overlap_map_group", &ecx_config_overlap_map_group, "context"_a, "iomap"_a, "group"_a);
    m.def("ecx_config_map_group_aligned", &ecx_config_map_group_aligned, "context"_a, "iomap"_a, "group"_a);
    m.def("ecx_recover_slave", &ecx_recover_slave, "context"_a, "slave"_a, "timeout"_a);
    m.def("ecx_reconfig_slave", &ecx_reconfig_slave, "context"_a, "slave"_a, "timeout"_a);

    // ethercatdc.h
    m.def("ecx_configdc", &ecx_configdc, "context"_a);

    m.def("osal_usleep", &osal_usleep, "usec"_a);
}
