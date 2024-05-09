#include <nanobind/nanobind.h>
#include <nanobind/stl/bind_vector.h>
#include <ethercat.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/tuple.h>
#include <iostream>
namespace nb = nanobind;

using namespace nb::literals;

using BytesVector = std::vector<uint8_t>;
using BytesArray = nb::ndarray<nb::numpy, uint8_t, nb::ndim<1>, nb::c_contig>;
using ECSlaveTVector = std::vector<ec_slavet>;
using ECGroupTVector = std::vector<ec_groupt>;

class SOEM_wrapper {
    public:
    ecx_contextt context;
    ecx_portt port;
    ECSlaveTVector slavelist;
    int slavecount;
    uint16_t maxslave;
    ECGroupTVector grouplist;
    uint8_t maxgroup;
    uint8_t esibuf [EC_MAXEEPBUF]; 
    uint32_t esimap [EC_MAXEEPBITMAP];
    ec_eringt elist;
    ec_idxstackT idxstack;
    boolean ecaterror;
    int64_t DCtime;
    ec_SMcommtypet SMcommtype;
    ec_PDOassignt PDOassign;
    ec_PDOdesct PDOdesc;
    ec_eepromSMt eepSM;
    ec_eepromFMMUt eepFMMU;

    //iomap
    BytesVector iomap;

    SOEM_wrapper(uint16_t maxslave_, uint8_t maxgroup_, size_t iomap_size_bytes){
        if (maxslave_ == 0) {
                throw std::invalid_argument("maxslave cannot be zero.");
            }
        if (maxgroup_ == 0) {
            throw std::invalid_argument("maxgroup cannot be zero.");
        }
        if (iomap_size_bytes == 0) {
            throw std::invalid_argument("iomap_size_bytes cannot be zero.");
        }

        slavelist.resize(maxslave_);
        maxslave = maxslave_;
        grouplist.resize(maxgroup_);
        maxgroup = maxgroup_;
        iomap.resize(iomap_size_bytes, 0);
        //iomap_ndarray_shape[0] = iomap_size_bytes;
        //iomap_ndarray = BytesArray(iomap.data(), 1, iomap_ndarray_shape, nb::handle());

        context.port = &port;
        context.slavelist = slavelist.data();
        context.slavecount = &slavecount;
        context.maxslave = maxslave;
        context.grouplist = grouplist.data();
        context.maxgroup = maxgroup;
        context.esibuf = &esibuf[0];
        context.esimap = &esimap[0];
        context.esislave = 0;
        context.elist = &elist;
        context.idxstack = &idxstack;
        context.ecaterror = &ecaterror;
        context.DCtime = &DCtime;
        context.SMcommtype = &SMcommtype;
        context.PDOassign = &PDOassign;
        context.PDOdesc = &PDOdesc;
        context.eepSM = &eepSM;
        context.eepFMMU = &eepFMMU;
        context.FOEhook = nullptr;
        context.EOEhook = nullptr;
        context.manualstatechange = 0;
        context.userdata = nullptr;
    }
    auto close(){
        return ecx_close(&this->context);
    }
    auto pusherror(const ec_errort *Ec){
        return ecx_pusherror(&this->context, Ec);
    }
    auto poperror(ec_errort *Ec){
        return ecx_poperror(&this->context, Ec);
    }
    auto packeterror(uint16 Slave, uint16 Index, uint8 SubIdx, uint16 ErrorCode){
        return ecx_packeterror(&this->context, Slave, Index, SubIdx, ErrorCode);
    }
    auto iserror(){
        return ecx_iserror(&this->context);
    }
    auto init_redundant(ecx_redportt *redport, const char *ifname, const char *if2name){
        return ecx_init_redundant(&this->context, redport, ifname, (char *)if2name);
    }
    auto readstate(){
        return ecx_readstate(&this->context);
    }
    auto writestate(uint16_t slave){
        return ecx_writestate(&this->context, slave);
    }
    auto statecheck(uint16 slave, uint16 reqstate, int timeout_us){
        return ecx_statecheck(&this->context, slave, reqstate, timeout_us);
    }
    auto send_overlap_processdata_group(uint8 group){
        return ecx_send_overlap_processdata_group(&this->context, group);
    }
    auto receive_processdata_group(uint8 group, int timeout_us){
        return ecx_receive_processdata_group(&this->context, group, timeout_us);
    }
    auto send_processdata(){
        return ecx_send_processdata(&this->context);
    }
    auto send_overlap_processdata(){
        return ecx_send_overlap_processdata(&this->context);
    }
    auto receive_processdata(int timeout_us){
        return ecx_receive_processdata(&this->context, timeout_us);
    }
    auto send_processdata_group(uint8 group){
        return ecx_send_processdata_group(&this->context, group);
    }
    auto init(const char * ifname){
        return ecx_init(&this->context, ifname);
    }
    auto config_init(uint8 usetable){
        return ecx_config_init(&this->context, usetable);
    }
    auto config_map_group( uint8 group){
        return ecx_config_map_group(&this->context, iomap.data(), group);
    }
    auto config_map_group_aligned( uint8 group){
        return ecx_config_map_group_aligned(&this->context, iomap.data(), group);
    }
    auto config_overlap_map_group( uint8 group){
        return ecx_config_overlap_map_group(&this->context, iomap.data(), group);
    }
    auto recover_slave(uint16 slave, int timeout_us){
        return ecx_recover_slave(&this->context, slave, timeout_us);
    }
    auto reconfig_slave(uint16 slave, int timeout_us){
        return ecx_reconfig_slave(&this->context, slave, timeout_us);
    }
    auto configdc(){
        return ecx_configdc(&this->context);
    }
    auto dcsync0(uint16 slave, boolean act, uint32 CyclTime_ns, int32 CyclShift_ns){
        return ecx_dcsync0(&this->context, slave, act, CyclTime_ns, CyclShift_ns);
    }
    auto dcsync01(uint16 slave, boolean act, uint32 CyclTime0_ns, uint32 CyclTime1_ns, int32 CyclShift_ns){
        return ecx_dcsync01(&this->context, slave, act, CyclTime0_ns, CyclTime1_ns, CyclShift_ns);
    }

    // CoE
    auto SDOread(uint16 slave, uint16 index, uint8 subindex, boolean CA, int *psize, int timeout_us){
        if (*psize <= 0) {
            throw std::invalid_argument("size may not be <= 0.");
        }
        
        int wkc;
        char buffer[static_cast<size_t>(*psize)];
        wkc = ecx_SDOread(&this->context, slave, index, subindex, CA, psize, &buffer[0], timeout_us);
        size_t shape[1] = {static_cast<size_t>(*psize)};
        return std::make_tuple(wkc, BytesArray(buffer, 1, shape, nb::handle()));
    }
    auto SDOwrite(uint16 Slave, uint16 Index, uint8 SubIndex, boolean CA, BytesArray data, int Timeout_us){

        return ecx_SDOwrite(&this->context, Slave, Index, SubIndex, CA, data.size(), data.data(), Timeout_us);
    }
    
};

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
        .def(nb::init<>())
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
    nb::bind_vector<ECSlaveTVector>(m, "ECSlaveTVector");
    //nb::bind_vector<BytesVector>(m, "BytesVector");
    nb::bind_vector<ECGroupTVector>(m, "ECGroupTVector");
    nb::class_<SOEM_wrapper>(m, "SOEM")
        .def("__init__", [](SOEM_wrapper *context_wrapper, uint16_t maxslave, uint8_t maxgroup, size_t iomap_size_bytes) {
            new (context_wrapper) SOEM_wrapper(maxslave, maxgroup, iomap_size_bytes);
        }, "maxslave"_a, "maxgroup"_a, "iomap_size_bytes"_a)
        .def_rw("port", &SOEM_wrapper::port)
        .def_rw("slavelist", &SOEM_wrapper::slavelist)
        .def_ro("slavecount", &SOEM_wrapper::slavecount)
        .def_ro("maxslave", &SOEM_wrapper::maxslave)
        .def_rw("grouplist", &SOEM_wrapper::grouplist)
        .def_rw("maxgroup", &SOEM_wrapper::maxgroup)
        .def_rw("elist", &SOEM_wrapper::elist)
        .def_rw("idxstack", &SOEM_wrapper::idxstack)
        .def_rw("ecaterror", &SOEM_wrapper::ecaterror)
        .def_rw("DCtime", &SOEM_wrapper::DCtime)
        .def_rw("SMcommtype", &SOEM_wrapper::SMcommtype)
        .def_rw("PDOassign", &SOEM_wrapper::PDOassign)
        .def_rw("PDOdesc", &SOEM_wrapper::PDOdesc)
        .def_rw("eepSM", &SOEM_wrapper::eepSM)
        .def_rw("eepFMMU", &SOEM_wrapper::eepFMMU)
        //.def_rw("iomap", &SOEM_wrapper::iomap_ndarray)
        .def_prop_ro("iomap", [](SOEM_wrapper &wrapper){
            size_t shape[1] = {wrapper.iomap.size()};
            std::cout << "Size of iomap array: " << shape[0] << std::endl;
            nb::ndarray<nb::numpy, uint8_t, nb::shape<-1>, nb::c_contig> myarray(wrapper.iomap.data(), 1, shape, nb::handle());
            std::cout << "here " << std::endl;
            return myarray;
            //return BytesArray(wrapper.iomap.data(), 1, shape, nb::handle());
        })
        .def("close", &SOEM_wrapper::close)
        .def("iserror", &SOEM_wrapper::iserror)
        .def("poperror", &SOEM_wrapper::poperror)
        .def("pusherror", &SOEM_wrapper::pusherror)
        .def("init_redundant", &SOEM_wrapper::init_redundant)
        .def("readstate", &SOEM_wrapper::readstate)
        .def("writestate", &SOEM_wrapper::writestate, "slave"_a)
        .def("statecheck", &SOEM_wrapper::statecheck, "slave"_a, "reqstate"_a, "timeout_us"_a)
        .def("send_overlap_processdata_group", &SOEM_wrapper::send_overlap_processdata_group)
        .def("send_overlap_processdata_group", &SOEM_wrapper::send_overlap_processdata_group, "group"_a)
        .def("receive_processdata_group", &SOEM_wrapper::receive_processdata_group, "group"_a, "timeout_us"_a)
        .def("send_processdata", &SOEM_wrapper::send_processdata)
        .def("send_overlap_processdata", &SOEM_wrapper::send_overlap_processdata)
        .def("receive_processdata", &SOEM_wrapper::receive_processdata, "timeout_us"_a)
        .def("send_processdata_group", &SOEM_wrapper::send_processdata_group, "group"_a)
        .def("init", &SOEM_wrapper::init, "ifname"_a)
        .def("config_init", &SOEM_wrapper::config_init, "usetable"_a)
        .def("config_map_group", &SOEM_wrapper::config_map_group, "group"_a)
        .def("config_overlap_map_group", &SOEM_wrapper::config_overlap_map_group, "group"_a)
        .def("config_map_group_aligned", &SOEM_wrapper::config_map_group_aligned, "group"_a)
        .def("recover_slave", &SOEM_wrapper::recover_slave, "slave"_a, "timeout_us"_a)
        .def("reconfig_slave", &SOEM_wrapper::reconfig_slave, "slave"_a, "timeout_us"_a)
        // ethercatdc.h
        .def("configdc", &SOEM_wrapper::configdc)
        .def("dcsync0", &SOEM_wrapper::dcsync0, "slave"_a, "act"_a, "CyclTime_ns"_a, "CycleShift_ns"_a)
        .def("dcsync01", &SOEM_wrapper::dcsync01, "slave"_a, "act"_a, "CyclTime0_ns"_a, "CyclTime1_ns"_a, "CyclShift_ns"_a)
        //CoE
        .def("SDOread", &SOEM_wrapper::SDOread, "slave"_a, "index"_a, "subindex"_a, "complete_access"_a, "size"_a, "timeout_us"_a)
        .def("SDOwrite", &SOEM_wrapper::SDOwrite, "slave"_a, "index"_a, "subindex"_a, "complete_access"_a, "data"_a, "timeout_us"_a);


    
    // osal.h
    m.def("osal_usleep", &osal_usleep, "usec"_a);
}
