#include <nanobind/nanobind.h>
#include <nanobind/stl/bind_vector.h>
#include <ethercat.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/tuple.h>
namespace nb = nanobind;

using namespace nb::literals;

using BytesVector = std::vector<uint8_t>;
using BytesArray = nb::ndarray<nb::numpy, uint8_t, nb::ndim<1>, nb::c_contig>;
using SubDeviceVector = std::vector<ec_slavet>;
using ECGroupTVector = std::vector<ec_groupt>;

class SOEM_wrapper {
    public:
    ecx_contextt context;
    ecx_portt port;
    SubDeviceVector subdevices;
    int subdevice_count;
    uint16_t max_subdevices;
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
    bool manualstatechange;

    //iomap
    BytesVector iomap;

    //redundancy
    ecx_redportt redport;

    SOEM_wrapper(uint16_t max_subdevices_, uint8_t maxgroup_, size_t iomap_size_bytes, bool manualstatechange_){
        if (max_subdevices_ == 0) {
                throw std::invalid_argument("max_subdevices cannot be zero.");
            }
        if (maxgroup_ == 0) {
            throw std::invalid_argument("maxgroup cannot be zero.");
        }
        if (iomap_size_bytes == 0) {
            throw std::invalid_argument("iomap_size_bytes cannot be zero.");
        }
        manualstatechange = manualstatechange_;

        subdevices.resize(max_subdevices_); // index 0 reserved for main_device
        max_subdevices = max_subdevices_;        // index 0 reserved for main_device
        grouplist.resize(maxgroup_);
        maxgroup = maxgroup_;
        iomap.resize(iomap_size_bytes, 0);

        context.port = &port;
        context.slavelist = subdevices.data();
        context.slavecount = &subdevice_count;
        context.maxslave = max_subdevices;
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
        context.manualstatechange = manualstatechange; // the context is an int but bool is better for python.
        context.userdata = nullptr;
    }
    int init(const char * ifname){
        return ecx_init(&this->context, ifname);
    }
    int init_redundant(const char *ifname, const char *if2name){
        return ecx_init_redundant(&this->context, &this->redport, ifname, (char *)if2name);
    }
    int config_init(){
        return ecx_config_init(&this->context, 0); // don't usetable
    }
    int config_overlap_map(){
        return ecx_config_overlap_map_group(&this->context, iomap.data(), 0);
    }
    int send_overlap_processdata_group(uint8 group){
        return ecx_send_overlap_processdata_group(&this->context, group);
    }
    int receive_processdata_group(uint8 group, int timeout_us){
        return ecx_receive_processdata_group(&this->context, group, timeout_us);
    }
    auto poperror(){
        ec_errort Ec;
        bool popped_error;
        popped_error = ecx_poperror(&this->context, &Ec);
        return std::make_tuple(popped_error, Ec);
    }
    bool iserror(){
        return (bool)ecx_iserror(&this->context);
    }
    int readstate(){
        return ecx_readstate(&this->context);
    }
    int writestate(uint16_t subdevice){
        return ecx_writestate(&this->context, subdevice);
    }
    uint16_t statecheck(uint16 subdevice, uint16 reqstate, int timeout_us){
        return ecx_statecheck(&this->context, subdevice, reqstate, timeout_us);
    }
    int recover_subdevice(uint16 subdevice, int timeout_us){
        return ecx_recover_slave(&this->context, subdevice, timeout_us);
    }
    int reconfig_subdevice(uint16 subdevice, int timeout_us){
        return ecx_reconfig_slave(&this->context, subdevice, timeout_us);
    }
    bool configdc(){
        return (bool)ecx_configdc(&this->context);
    }
    void dcsync0(uint16 subdevice, boolean act, uint32 CyclTime_ns, int32 CyclShift_ns){
        return ecx_dcsync0(&this->context, subdevice, act, CyclTime_ns, CyclShift_ns);
    }
    void dcsync01(uint16 subdevice, boolean act, uint32 CyclTime0_ns, uint32 CyclTime1_ns, int32 CyclShift_ns){
        return ecx_dcsync01(&this->context, subdevice, act, CyclTime0_ns, CyclTime1_ns, CyclShift_ns);
    }
    auto SDOread(uint16 subdevice, uint16 index, uint8 subindex, boolean CA, int size, int timeout_us){
        if (size <= 0) {
            throw std::invalid_argument("size may not be <= 0.");
        }
        int wkc;
        BytesVector *buffer = new BytesVector(size, 0);
        nb::capsule owner(buffer, [](void *p) noexcept {
            delete (BytesVector *) p;
        });
        int bytes_read = size;
        wkc = ecx_SDOread(&this->context, subdevice, index, subindex, CA, &bytes_read, buffer->data(), timeout_us);
        size_t shape[1] = {buffer->size()};
        return std::make_tuple(wkc, bytes_read, BytesArray(buffer->data(), 1, shape, owner));
    }
    int SDOwrite(uint16 subdevice, uint16 Index, uint8 SubIndex, boolean CA, BytesArray data, int Timeout_us){
        return ecx_SDOwrite(&this->context, subdevice, Index, SubIndex, CA, data.size(), data.data(), Timeout_us);
    }
    auto readODlist(uint16 subdevice){
        int wkc;
        ec_ODlistt ODlist = {};
        wkc = ecx_readODlist(&this->context, subdevice, &ODlist);
        return std::make_tuple(wkc, ODlist);
    }
    auto readODdescription(uint16 item, ec_ODlistt ODlist){
        int wkc;
        wkc = ecx_readODdescription(&this->context, item, &ODlist);
        return std::make_tuple(wkc, ODlist);
    }
    auto readOE(uint16 item, ec_ODlistt ODlist){
        int wkc;
        ec_OElistt oe_list = {};
        wkc = ecx_readOE(&this->context, item, &ODlist, &oe_list);
        return std::make_tuple(wkc, oe_list);
    }
    uint16 siifind(uint16 subdevice, uint16 cat){
        return ecx_siifind(&this->context, subdevice, cat);
    }
    uint8 siigetbyte(uint16 subdevice, uint16 address){
        return ecx_siigetbyte(&this->context, subdevice, address);
    }
    void close(){
        return ecx_close(&this->context);
    }
    
};

NB_MODULE(soem_ext, m)
{
    m.def(
        "add", [](int a, int b)
        { return a + b; },
        "a"_a, "b"_a);

    // ethercatcoe.h
    nb::class_<ec_OElistt>(m, "ec_OEListt")
        .def_ro("Entries", &ec_OElistt::Entries)
        .def_prop_ro("ValueInfo", [](ec_OElistt &oe_list){
            nb::typed<nb::list, uint8_t> vi_list;

            for (int i = 0; i < oe_list.Entries; i++){
                vi_list.append(oe_list.ValueInfo[i]);
            }
            return vi_list;
        })
        .def_prop_ro("DataType", [](ec_OElistt &oe_list){
            nb::typed<nb::list, uint16_t> dt_list;

            for (int i = 0; i < oe_list.Entries; i++){
                dt_list.append(oe_list.DataType[i]);
            }
            return dt_list;
        })
        .def_prop_ro("BitLength", [](ec_OElistt &oe_list){
            nb::typed<nb::list, uint16_t> bl_list;

            for (int i = 0; i < oe_list.Entries; i++){
                bl_list.append(oe_list.BitLength[i]);
            }
            return bl_list;
        })
        .def_prop_ro("ObjAccess", [](ec_OElistt &oe_list){
            nb::typed<nb::list, uint8_t> oa_list;

            for (int i = 0; i < oe_list.Entries; i++){
                oa_list.append(oe_list.ObjAccess[i]);
            }
            return oa_list;
        })
        .def_prop_ro("Name", [](ec_OElistt &oe_list){
            nb::typed<nb::list, nb::str> name_list;

            for (int i = 0; i < oe_list.Entries; i++){
                name_list.append(nb::str(oe_list.Name[i]));
            }
            return name_list;
        });
    nb::class_<ec_ODlistt>(m, "ec_ODListt")
        .def_ro("subdevice", &ec_ODlistt::Slave)
        .def_ro("Entries", &ec_ODlistt::Entries)
        .def_prop_ro("Index", [](ec_ODlistt &od_list){
            nb::typed<nb::list, uint16_t> index_list;

            for (int i = 0; i < od_list.Entries; i++){
                index_list.append(od_list.Index[i]);
            }
            return index_list;
        })
        .def_prop_ro("DataType", [](ec_ODlistt &od_list){
            nb::typed<nb::list, uint16_t> dt_list;

            for (int i = 0; i < od_list.Entries; i++){
                dt_list.append(od_list.DataType[i]);
            }
            return dt_list;
        })
        .def_prop_ro("ObjectCode", [](ec_ODlistt &od_list){
            nb::typed<nb::list, uint8_t> oc_list;

            for (int i = 0; i < od_list.Entries; i++){
                oc_list.append(od_list.ObjectCode[i]);
            }
            return oc_list;
        })
        .def_prop_ro("MaxSub", [](ec_ODlistt &od_list){
            nb::typed<nb::list, uint8_t> ms_list;

            for (int i = 0; i < od_list.Entries; i++){
                ms_list.append(od_list.MaxSub[i]);
            }
            return ms_list;
        })
        .def_prop_ro("Name", [](ec_ODlistt &od_list){
            nb::typed<nb::list, nb::str> name_list;

            for (int i = 0; i < od_list.Entries; i++){
                name_list.append(nb::str(od_list.Name[i]));
            }
            return name_list;
        });

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

    nb::enum_<ec_state>(m, "ec_state", nb::is_arithmetic())
        .value("NONE", ec_state::EC_STATE_NONE)
        .value("INIT", ec_state::EC_STATE_INIT)
        .value("PRE_OP", ec_state::EC_STATE_PRE_OP)
        .value("BOOT", ec_state::EC_STATE_BOOT)
        .value("SAFE_OP", ec_state::EC_STATE_SAFE_OP)
        .value("OPERATIONAL", ec_state::EC_STATE_OPERATIONAL)
        .value("ACK", ec_state::EC_STATE_ACK)
        .value("ERROR", ec_state::EC_STATE_ERROR);

    nb::class_<ec_errort>(m, "ec_errort")
        .def_rw("Time", &ec_errort::Time)
        .def_rw("Signal", &ec_errort::Signal)
        .def_rw("subdevice", &ec_errort::Slave)
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
        .def_prop_ro("name", [](ec_adaptert *adp) -> nb::str
                     { return nb::str(adp->name); })
        .def_prop_ro("desc", [](ec_adaptert *adp) -> nb::str
                     { return nb::str(adp->desc); });

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
    
    nb::class_<ec_smt>(m, "ec_smt")
        .def_ro("StartAddr", &ec_smt::StartAddr)
        .def_ro("SMlength", &ec_smt::SMlength)
        .def_ro("SMflags", &ec_smt::SMflags);
    nb::class_<ec_fmmut>(m, "ec_fmmut")
        .def_ro("LogStart", &ec_fmmut::LogStart)
        .def_ro("LogLength", &ec_fmmut::LogLength)
        .def_ro("LogStartbit", &ec_fmmut::LogStartbit)
        .def_ro("LogEndbit", &ec_fmmut::LogEndbit)
        .def_ro("PhysStart", &ec_fmmut::PhysStart)
        .def_ro("PhysStartBit", &ec_fmmut::PhysStartBit)
        .def_ro("FMMUtype", &ec_fmmut::FMMUtype)
        .def_ro("FMMUactive", &ec_fmmut::FMMUactive)
        .def_ro("unused1", &ec_fmmut::unused1)
        .def_ro("unused2", &ec_fmmut::unused2);

    // TODO: fill in
    nb::class_<ec_slavet>(m, "SubDevice")
        .def(nb::init<>())
        .def_rw("state", &ec_slavet::state)
        .def_ro("ALstatuscode", &ec_slavet::ALstatuscode)
        .def_ro("configadr", &ec_slavet::configadr)
        .def_ro("aliasadr", &ec_slavet::aliasadr)
        .def_ro("eep_man", &ec_slavet::eep_man)
        .def_ro("eep_id", &ec_slavet::eep_id)
        .def_ro("eep_rev", &ec_slavet::eep_rev)
        .def_ro("Itype", &ec_slavet::Itype)
        .def_ro("Dtype", &ec_slavet::Dtype)
        .def_ro("Obits", &ec_slavet::Obits)
        .def_ro("Obytes", &ec_slavet::Obytes)
        .def_ro("outputs", &ec_slavet::outputs)
        .def_ro("Ostartbit", &ec_slavet::Ostartbit)
        .def_ro("Ibits", &ec_slavet::Ibits)
        .def_ro("Ibytes", &ec_slavet::Ibytes)
        .def_ro("inputs", &ec_slavet::inputs)
        .def_ro("Istartbit", &ec_slavet::Istartbit)
        .def_prop_ro("SM", [](ec_slavet &subdevice){
            nb::typed<nb::list, ec_smt> sm_list;

            for (int i = 0; i < EC_MAXSM; i++){
                sm_list.append(subdevice.SM[i]);
            }
            return sm_list;
        })
        .def_prop_ro("SMtype", [](ec_slavet &subdevice){
            nb::typed<nb::list, uint8_t> smtype_list;

            for (int i = 0; i < EC_MAXSM; i++){
                smtype_list.append(subdevice.SMtype[i]);
            }
            return smtype_list;
        })
        .def_prop_ro("FMMU", [](ec_slavet &subdevice){
            nb::typed<nb::list, ec_fmmut> fmmu_list;

            for (int i = 0; i < EC_MAXFMMU; i++){
                fmmu_list.append(subdevice.FMMU[i]);
            }
            return fmmu_list;
        })
        //.def_rw("FMMU", &ec_slavet::FMMU)
        .def_ro("FMMU0func", &ec_slavet::FMMU0func)
        .def_ro("FMMU1func", &ec_slavet::FMMU1func)
        .def_ro("FMMU2func", &ec_slavet::FMMU2func)
        .def_ro("FMMU3func", &ec_slavet::FMMU3func)
        .def_ro("mbx_l", &ec_slavet::mbx_l)
        .def_ro("mbx_wo", &ec_slavet::mbx_wo)
        .def_ro("mbx_rl", &ec_slavet::mbx_rl)
        .def_ro("mbx_ro", &ec_slavet::mbx_ro)
        .def_ro("mbx_proto", &ec_slavet::mbx_proto)
        .def_ro("mbx_cnt", &ec_slavet::mbx_cnt)
        .def_prop_ro("hasdc", [](ec_slavet &subdevice){
            return (bool)subdevice.hasdc;})
        .def_ro("ptype", &ec_slavet::ptype)
        .def_ro("topology", &ec_slavet::topology)
        .def_ro("activeports", &ec_slavet::activeports)
        .def_ro("consumedports", &ec_slavet::consumedports)
        .def_ro("parent", &ec_slavet::parent)
        .def_ro("parentport", &ec_slavet::parentport)
        .def_ro("entryport", &ec_slavet::entryport)
        .def_ro("DCrtA", &ec_slavet::DCrtA)
        .def_ro("DCrtB", &ec_slavet::DCrtB)
        .def_ro("DCrtC", &ec_slavet::DCrtC)
        .def_ro("DCrtD", &ec_slavet::DCrtD)
        .def_ro("pdelay", &ec_slavet::pdelay)
        .def_ro("DCnext", &ec_slavet::DCnext)
        .def_ro("DCprevious", &ec_slavet::DCprevious)
        .def_ro("DCcycle", &ec_slavet::DCcycle)
        .def_ro("DCshift", &ec_slavet::DCshift)
        .def_ro("DCactive", &ec_slavet::DCactive)
        .def_ro("configindex", &ec_slavet::configindex)
        .def_ro("SIIindex", &ec_slavet::SIIindex)
        .def_ro("eep_8byte", &ec_slavet::eep_8byte)
        .def_ro("eep_pdi", &ec_slavet::eep_pdi)
        .def_rw("CoEdetails", &ec_slavet::CoEdetails)
        .def_rw("FoEdetails", &ec_slavet::FoEdetails)
        .def_rw("EoEdetails", &ec_slavet::EoEdetails)
        .def_rw("SoEdetails", &ec_slavet::SoEdetails)
        .def_rw("Ebuscurrent", &ec_slavet::Ebuscurrent)
        .def_rw("blockLRW", &ec_slavet::blockLRW)
        .def_rw("group", &ec_slavet::group)
        .def_ro("FMMUunused", &ec_slavet::FMMUunused)
        .def_prop_rw("islost", [](ec_slavet &subdevice){
            return (bool)subdevice.islost;}, 
            [](ec_slavet &subdevice, bool value){
                subdevice.islost = value;
            })
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
    nb::bind_vector<SubDeviceVector, nb::rv_policy::reference_internal>(m, "SubDeviceVector");
    nb::bind_vector<ECGroupTVector, nb::rv_policy::reference_internal>(m, "ECGroupTVector");
    nb::class_<SOEM_wrapper>(m, "SOEM")
        .def("__init__", [](SOEM_wrapper *context_wrapper, uint16_t max_subdevices, uint8_t maxgroup, size_t iomap_size_bytes, bool manualstatechange) {
            new (context_wrapper) SOEM_wrapper(max_subdevices, maxgroup, iomap_size_bytes, manualstatechange);
        }, "max_subdevices"_a = uint16_t(512), "maxgroup"_a = uint8_t(2), "iomap_size_bytes"_a = size_t(4096), "manualstatechange"_a = bool(0))
        .def_ro("port", &SOEM_wrapper::port)
        .def_rw("subdevices", &SOEM_wrapper::subdevices)
        .def_ro("subdevice_count", &SOEM_wrapper::subdevice_count)
        .def_ro("max_subdevices", &SOEM_wrapper::max_subdevices)
        .def_ro("grouplist", &SOEM_wrapper::grouplist)
        .def_ro("maxgroup", &SOEM_wrapper::maxgroup)
        .def_ro("elist", &SOEM_wrapper::elist)
        .def_ro("idxstack", &SOEM_wrapper::idxstack)
        .def_ro("ecaterror", &SOEM_wrapper::ecaterror)
        .def_ro("DCtime", &SOEM_wrapper::DCtime)
        .def_ro("SMcommtype", &SOEM_wrapper::SMcommtype)
        .def_ro("PDOassign", &SOEM_wrapper::PDOassign)
        .def_ro("PDOdesc", &SOEM_wrapper::PDOdesc)
        .def_ro("eepSM", &SOEM_wrapper::eepSM)
        .def_ro("eepFMMU", &SOEM_wrapper::eepFMMU)
        .def_ro("manualstatechange", &SOEM_wrapper::manualstatechange)
        .def("close", &SOEM_wrapper::close)
        .def("iserror", &SOEM_wrapper::iserror)
        .def("poperror", &SOEM_wrapper::poperror)
        .def("init_redundant", &SOEM_wrapper::init_redundant, "ifname"_a, "if2name"_a)
        .def("readstate", &SOEM_wrapper::readstate)
        .def("writestate", &SOEM_wrapper::writestate, "subdevice"_a)
        .def("statecheck", &SOEM_wrapper::statecheck, "subdevice"_a, "reqstate"_a, "timeout_us"_a)
        .def("send_overlap_processdata_group", &SOEM_wrapper::send_overlap_processdata_group, "group"_a)
        .def("receive_processdata_group", &SOEM_wrapper::receive_processdata_group, "group"_a, "timeout_us"_a)
        .def("init", &SOEM_wrapper::init, "ifname"_a)
        .def("config_init", &SOEM_wrapper::config_init)
        .def("config_overlap_map", &SOEM_wrapper::config_overlap_map)
        .def("recover_subdevice", &SOEM_wrapper::recover_subdevice, "subdevice"_a, "timeout_us"_a)
        .def("reconfig_subdevice", &SOEM_wrapper::reconfig_subdevice, "subdevice"_a, "timeout_us"_a)
        // ethercatdc.h
        .def("configdc", &SOEM_wrapper::configdc)
        .def("dcsync0", &SOEM_wrapper::dcsync0, "subdevice"_a, "act"_a, "CyclTime_ns"_a, "CycleShift_ns"_a)
        .def("dcsync01", &SOEM_wrapper::dcsync01, "subdevice"_a, "act"_a, "CyclTime0_ns"_a, "CyclTime1_ns"_a, "CyclShift_ns"_a)
        //CoE
        .def("SDOread", &SOEM_wrapper::SDOread, "subdevice"_a, "index"_a, "subindex"_a, "complete_access"_a, "size"_a, "timeout_us"_a)
        .def("SDOwrite", &SOEM_wrapper::SDOwrite, "subdevice"_a, "index"_a, "subindex"_a, "complete_access"_a, "data"_a, "timeout_us"_a)
        .def("readODlist", &SOEM_wrapper::readODlist, "subdevice"_a)
        .def("readODdescription", &SOEM_wrapper::readODdescription, "item"_a, "ODlist"_a)
        .def("readOE", &SOEM_wrapper::readOE, "item"_a, "ODlist"_a)
        //sii
        .def("siifind", &SOEM_wrapper::siifind, "subdevice"_a, "cat"_a)
        .def("siigetbyte", &SOEM_wrapper::siigetbyte, "subdevice"_a, "address"_a)
        //iomap
        .def_prop_ro("iomap", [](SOEM_wrapper &wrapper){
            size_t shape[1] = {wrapper.iomap.size()};
            return BytesArray(wrapper.iomap.data(), 1, shape, nb::handle());
        }, nb::rv_policy::reference_internal)
        .def("get_iomap", [](SOEM_wrapper &wrapper, uint16_t subdevice) -> std::tuple<BytesArray, BytesArray> {
            if (subdevice > wrapper.max_subdevices) {
                throw std::invalid_argument("requested subdevice is larger than max_subdevices.");
            }
            // when viewing maindevice iomap (subdevice=0). bytecount will be accurate
            if (subdevice == 0){
                size_t shape_inputs[1] = {static_cast<size_t>(wrapper.subdevices[subdevice].Ibytes)};
                size_t shape_outputs[1] = {static_cast<size_t>(wrapper.subdevices[subdevice].Obytes)};
                return std::make_tuple(
                    BytesArray(wrapper.subdevices[subdevice].inputs, 1, shape_inputs, nb::handle()),
                    BytesArray(wrapper.subdevices[subdevice].outputs, 1, shape_outputs, nb::handle()));
            }
            // for subdevice iomaps, since bytecount can be zero for bitcount < 8, 
            // we will only trust bitcount
            size_t shape_inputs[1] = {static_cast<size_t>(wrapper.subdevices[subdevice].Ibits / 8 + (wrapper.subdevices[subdevice].Ibits % 8 != 0))};
            size_t shape_outputs[1] = {static_cast<size_t>(wrapper.subdevices[subdevice].Obits / 8 + (wrapper.subdevices[subdevice].Obits % 8 != 0))};
            return std::make_tuple(
                    BytesArray(wrapper.subdevices[subdevice].inputs, 1, shape_inputs, nb::handle()),
                    BytesArray(wrapper.subdevices[subdevice].outputs, 1, shape_outputs, nb::handle()));
        }, nb::rv_policy::reference_internal, "subdevice"_a);


    
    // osal.h
    m.def("osal_usleep", &osal_usleep, "usec"_a);
}
