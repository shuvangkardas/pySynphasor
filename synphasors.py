from scapy.all import *
import  crc
from zlib import crc32

############C37.118.2 Common Frame#############
#Packet Type
PACKET_TYPE = {
    0: 'DATA',
    1: 'HEADER',
    2: 'CFG1',
    3: 'CFG2',
    5: 'CFG3',
    4: 'CMD',
}

# Version
VERSION = {
    1: 'Version 1', #IEEE Std C37.118-2005
    2: 'Version 2'  #IEEE Std C37.118.2-2011
}


class synphasor(Packet):
    name = "IEEE C37.118.2 COMMON FRAME"
    fields_desc = [
        #SYNC byte(2 Byte)
        XByteField("synByte",0xAA),
        BitField("reserved", 0, 1),
        BitEnumField("type",0,3,PACKET_TYPE),
        BitEnumField("version",2,4,VERSION),
        #FRAME SIZE(2 byte) | Need to write VariableLenField for length
        # FieldLenField("framesize", None, length_of="framesize"),
        ShortField("framesize", None),
        #Data Stream IDCODE(2 bytes)
        ShortField("idcode",0),
        #SOC- Unix Timestamp(4 bytes)
        IntField("soc",None),
        #FRACSEC- Fraction of second(4 byte)
        IntField("fracsec",None),
    ]

    
    # Need to calculate length of current and next layer in post build methods
    def post_build(self, pkt,pay):
        #calculate sum length of current layer and payload
        if self.framesize is None:
            totalLen = len(pkt) + len(pay)
            # print("Total Len: ",totalLen)
            # print("pkt1:", pkt)
            # print("pay1: ",pay)
            # print("payload type: ",type(self.payload))
            pkt = pkt[:2] + struct.pack("!H", totalLen) + pkt[4:]
        
        #combine two layer byte string to calculate crc
        pktRaw = pkt + pay
        # print("has attribute: ",hasattr(self.payload,"chk"))
        #Calculate CRC of the whole packet
        if hasattr(self.payload,"chk"):
            if self.payload.chk is None:
            # if self.payload.chk==0:
                crcVal = crc.crc16xmodem(pktRaw[:-2])
                # print("Calculated CRC: ",crcVal)
                pay = pay[:-2]+struct.pack("!H",crcVal)
        return pkt + pay
        #return pktRaw

################C37.118.2 Command Frame##################
class synphasor_cmd(Packet):
    name = "synphasor command"
    fields_desc = [
        #CMD(2 byte)
        ShortField("cmd",0),
        #CRC(2 byte)
        XShortField("chk",None)
    ]
    #def post_build(self, pkt,pay):
    #    return pkt + pay



###############C37.118.2 CFG1 and CFG2 Frame#############

#One set of digital status word name for CFG2 frame
class DGNAME(Packet):
    name="digital status name"
    fields_desc = [
        StrFixedLenField("dname1", "BREAKER 1 STATUS", length=16),
        StrFixedLenField("dname2", "BREAKER 2 STATUS", length=16),
        StrFixedLenField("dname3", "BREAKER 3 STATUS", length=16),
        StrFixedLenField("dname4", "BREAKER 4 STATUS", length=16),
        StrFixedLenField("dname5", "BREAKER 5 STATUS", length=16),
        StrFixedLenField("dname6", "BREAKER 6 STATUS", length=16),
        StrFixedLenField("dname7", "BREAKER 7 STATUS", length=16),
        StrFixedLenField("dname8", "BREAKER 8 STATUS", length=16),
        StrFixedLenField("dname9", "BREAKER 9 STATUS", length=16),
        StrFixedLenField("dname10", "BREAKER A STATUS", length=16),
        StrFixedLenField("dname11", "BREAKER B STATUS", length=16),
        StrFixedLenField("dname12", "BREAKER C STATUS", length=16),
        StrFixedLenField("dname13", "BREAKER D STATUS", length=16),
        StrFixedLenField("dname14", "BREAKER E STATUS", length=16),
        StrFixedLenField("dname15", "BREAKER F STATUS", length=16),
        StrFixedLenField("dname16", "BREAKER G STATUS", length=16),
    ]
    #Source https://stackoverflow.com/questions/8073508
    def extract_padding(self, s):
        return '', s

#Conversion Factor for phasor channel
class PHUNIT(Packet):
    name = "Phasor Conversion Factor",
    fields_desc = [
        #Flag to identify whether the factor is for voltage or current
        ByteEnumField("flag", 0, {0:'voltage', 1:'current'}),
        #Conversin Factor
        ThreeBytesField("phfactor",1)     
    ]
    def extract_padding(self, s):
        return '', s

#Conversion Factor for Analog Channel
class ANUNIT(Packet):
    name = "Analog Conversion Factor",
    fields_desc = [
        #Flag to identify whether the factor is for voltage or current
        ByteEnumField("flag", 0, {0:'single point on wave', 1:'rms of analog',2:'peak of analog',}),
        #Conversin Factor
        ThreeBytesField("anfactor",1)     
    ]
    def extract_padding(self, s):
        return '', s

#Conversion factor for digital status word
class DIGUNIT(Packet):
    name = "Digital Status Words"
    fields_desc = [
        XShortField("normal_status",0),
        XShortField("valid_input",0)
    ]
    
    def extract_padding(self, s):
        return '', s    

#Configuration Frame for a single pmu. This packet will be used to
#build final CFG1 and CFG2 packet
class PMU_CFG(Packet):
    name = "PMU Configuration"
    fields_desc = [
        #Station name in ASCII | 16 bytes 
        StrFixedLenField("stn", "STATION 1       ", length=16),
        #data source id number | 2 byte
        ShortField("idcode",0),
        #Data format | 2 byte
        BitField("unused",0,12),
        BitEnumField("freq",0,1,{0:'16-bit integer',1:'32-bit IEEE floating point'}),
        BitEnumField("analog",0,1,{0:'16-bit integer',1:'32-bit IEEE floating point'}),
        BitEnumField("phasor_dtype",0,1,{0:'16-bit integer',1:'32-bit IEEE floating point'}),
        BitEnumField("phasor_format",0,1,{0:'rectangular',1:'polar'}),
        #Number of phasors | 2 Byte
        FieldLenField("phnmr",None, count_of="phname"),
        #Number of Analog Value | 2 Byte
        FieldLenField("annmr",None, count_of="anname"),
        #Number of set of digital status word | Each set contains 16 status
        FieldLenField("dgnmr",None,count_of="dgname"),
        #FieldListField is used to create list of similar field. 
        FieldListField("phname",None,StrFixedLenField("name1","", length=16),count_from=lambda pkt:pkt.phnmr),
        #Analog Name List
        FieldListField("anname",None,StrFixedLenField("name2","", length=16),count_from=lambda pkt:pkt.annmr),
        #Digital Set List
        PacketListField("dgname", None, pkt_cls=DGNAME, count_from = lambda pkt:pkt.dgnmr),
        #Conversion factor for phasor  | 4 byte for each phasor
        PacketListField("phunit",None,pkt_cls=PHUNIT,count_from=lambda pkt:pkt.phnmr),
        #Conversion factor for analog channel
        PacketListField("anunit",None,pkt_cls=ANUNIT,count_from=lambda pkt:pkt.annmr),
        #Digital Status word
        PacketListField("dgunit",None,pkt_cls=DIGUNIT,count_from = lambda pkt:pkt.dgnmr),
        #Nominal Line Frequency | 2 Byte
        BitField("reserved",0,15),
        BitEnumField("fnom",0,1,{0:'60Hz',1:'50Hz'}),
        #Configuration Change Count | 2 byte
        ShortField("CFGCNT",0),
    ]
    def extract_padding(self, s):
        return '', s

class synphasor_cfg2(Packet):
    name = "IEEE C37.118.2 CFG2"
    fields_desc = [
        #Time base | 4 bytes
        IntField("TIME_BASE",0),
        #number of pmu | 2 bytes
        FieldLenField("num_pmu",None, count_of="pmu"),
        PacketListField("pmu",None,pkt_cls=PMU_CFG,
        count_from = lambda pkt:pkt.num_pmu),
        #Data rate | Data rate can be positive and negative| 2 byte
        SignedShortField("data_rate",30),
        #CRC value | 2 Byte
        XShortField("chk",None)
    ]


#################IEEE C37.118.2 Dataframe#####################

#ComplexIntField number field class to deal with phasor data in 16-bit integer format
#Human value 10+20j #machine value b'\x00\x0a\x00\x14'
class ComplexIntField(Field):

    def h2i(self, pkt, x):
        return complex(x)

    #Convert b'\x00\x08\x00\x09' to (8+9j)
    def m2i(self,pkt,x):
        x,y = struct.unpack("!HH",x)
        # print("unpack vale",x,y)
        # num = complex(x,y)
        return complex(x,y)
    
    #internal to machine | (8+9j) to b'\x00\x08\x00\x09'
    def i2m(self,pkt,x):
        # print("i2m input: ",x)
        if x is None:
            return struct.pack('!HH',int(0),int(0))
        return struct.pack('!HH',int(x.real),int(x.imag))

    #Extract complex value form byte string and return rest string
    def getfield(self, pkt,s):
        # print("str: ",s[4:])
        return s[4:],self.m2i(pkt,s[:4])
    #Add internal val(1+2j) to network string s
    def addfield(self, pkt, s, val):
        # print("addfield called")
        return s+self.i2m(pkt,val)

# ComplexFloatField for dealing float type complex number
class ComplexFloatField(Field):
    #machine to internal
    def m2i(self,pkt,x):
        x,y = struct.unpack("!ff",x)
        # print("unpack vale",x,y)
        # num = complex(x,y)
        return complex(x,y)
    
    #internal to machine
    def i2m(self,pkt,x):
        # print("i2m input: ",x)
        if x is None:
            return struct.pack('!ff',0,0)
        return struct.pack('!ff',x.real,x.imag)
    
    #Extract complex value form byte string and return rest string
    def getfield(self, pkt,s):
        # print("str: ",s[4:])
        return s[8:],self.m2i(pkt,s[:8])
    #Add internal val(1+2j) to network string s
    def addfield(self, pkt, s, val):
        # print("addfield called")
        return s+self.i2m(pkt,val)
        
#Enumeration dictionary for PMU Data
PMU_DATA_FLAG = {
    0: 'Good measurement',
    1: 'PMU error. No information about data',
    2: 'PMU in test mode',
    3: 'PMU error(do not use value)',
}

PMU_TIME_QUALITY = {
    0: 'Not used',
    1: 'Max time error < 100ns',
    2: 'Max time error <1us',
    3: 'Max time error 10us',
    4: 'Max time error 100us',
    5: 'Max time error 1ms',
    6: 'Max time error 10ms',
    7: 'Max time error >10ms or unknown'
}

UNOCKED_TIME = {
    0:'Sync locked or unlocked < 10s',
    1:'10s<=unlocked time<100s',
    2:'100s<unlock_time<=1000s',
    2:'Unlocked time>1000s'
}

TRIGGER_REASON = {
    0:'Manual',
    1:'Magnitude low',
    2:'Magnitude high',
    3:'Phase angle diff',
    4:'Freq high or low',
    5:'df/dt high',
    6:'Reserved',
    7:'Digital',
}

#Define static methods for getting pmu data information
pmu_count = 1
phasor_count = 4
analog_count = 3
digital_count = 1

# Analog 16 bit = 0 | floating = 1
analog_type = 1
# Bit 1: 0 = phasors 16-bit integer, 1 = floating point
phasor_type = 0
#FREQ/DFREQ format flag | 0 = 16-bit integer, 1 = float
freq_type = 0


def set_cfg_data(pkt):
    cfg = pkt['synphasor_cfg2']
    
    pmu_count =  cfg.num_pmu
    phasor_count = cfg.pmu[0].phnmr 
    analog_count = cfg.pmu[0].annmr      
    digital_count = cfg.pmu[0].dgnmr      
    analog_type = cfg.pmu[0].analog    
    phasor_type =cfg.pmu[0].phasor_dtype
    freq_type = cfg.pmu[0].freq 
    # print("Number of PMU: ",pmu_count)     

#pkt should input of length_from function. 
def get_ph_count(pkt):
    return phasor_count

def get_anlog_count(pkt):
    return analog_count

def get_digtal_count(pkt):
    return digital_count

def get_pmu_count(pkt):
    return pmu_count

# Bit 1: 0 = phasors 16-bit integer, 1 = floating point
def get_phasor_type(pkt):
    return phasor_type
#FREQ/DFREQ format flag | 0 = 16-bit integer, 1 = float  
def get_freq_type(pkt):
    return freq_type

def get_analog_type(pkt):
    return analog_type


# PMU Data class for a single PMU. Data packet might have data from multiple PMU
# This will be used to define  C37.118.2 data packet
class PMU_DATA(Packet):
    name="PMU Data"
    fields_desc = [
        #Start bit-mapped flag | 2 byte
        BitEnumField("data_error",0,2,PMU_DATA_FLAG),
        BitEnumField("pmu_sync",0,1,{0:'sync with UTC',1:'unknown'}),
        BitEnumField("data_storing",0,1,{0:'by time stamp',1:'by arrival'}),
        BitEnumField("pmu_trigger",1,1,{0:'no trigger',1:'trigger detected'}),
        BitEnumField("cfg_change",0,1,{0:'change effected',1:'cfg will change'}),
        BitEnumField("data_modified",0,1,{1:'data modified by post processing',0:'otherwise'}),
        BitEnumField("pmu_time_quality",0,3,PMU_TIME_QUALITY),
        BitEnumField("unlocked_time",0,2,UNOCKED_TIME),
        BitEnumField("trigger_reason",1,4,TRIGGER_REASON),
        #Phasors data
        # FieldListField("phasors",None,ComplexField("phvalue",0),count_from=get_ph_count),
        # FieldListField("phasors",None,ComplexField("phvalue",complex()),count_from= get_ph_count),
        MultipleTypeField(
            [
                (FieldListField("phasors",None,ComplexIntField("phvalue",complex()),count_from= get_ph_count),
                lambda pkt:get_phasor_type(pkt)==0),
                (FieldListField("phasors",None,ComplexFloatField("phvalue",complex()),count_from= get_ph_count),
                lambda pkt:get_phasor_type(pkt)==1)
            ],
            FieldListField("phasors",None,ComplexIntField("phvalue",complex()),count_from= get_ph_count),
        ),
        #Frequency | 2 byte if fixed, 4 byte if floating point
        MultipleTypeField(
            [
                (ShortField("freq",0), lambda pkt:get_freq_type(pkt)==0),
                (IEEEFloatField("freq",12.0), lambda pkt:get_freq_type(pkt)==1)
            ],
            ShortField("freq",0) #default field
        ),
        #DFREQ | 2 byte if fixed, 4 byte if floating point
        MultipleTypeField(
            [
                (ShortField("dfreq",0),lambda pkt:get_freq_type(pkt)==0),
                (IEEEFloatField("dfreq",0),lambda pkt:get_freq_type(pkt)==1)
            ],
            ShortField("dfreq",0) #default field
        ),

        #Analog Value
        MultipleTypeField(
            [
                # (ShortField("analogs",0),lambda pkt:get_analog_type(pkt)==0),
                # (IEEEFloatField("analogs",0),lambda pkt:get_analog_type(pkt)==1)
                (FieldListField("analogs",None,ShortField("anvalue",0),count_from= get_anlog_count),
                lambda pkt:get_analog_type(pkt)==0),
                (FieldListField("analogs",None,IEEEFloatField("anvalue",0),count_from= get_anlog_count),
                lambda pkt:get_analog_type(pkt)==1)
            ],
            FieldListField("analogs",None,ShortField("anvalue",0),count_from= get_anlog_count)
        ),

        # FieldListField("analogs",None,ShortField("anvalue",0), count_from=get_anlog_count),
        #Digital Status word
        FieldListField("digitals",None,XShortField("dgword",0),count_from=get_digtal_count)
    ]
    def extract_padding(self, s):
        return '', s

class synphasor_data(Packet):
    name="IEEE C37.118.2 Data"
    fields_desc = [
        #PMU Data Frame
        PacketListField("pmu_data",None,pkt_cls=PMU_DATA,
        count_from = get_pmu_count),
        #CRC checksum | 2 bytes
        XShortField ("chk",None)
    ]


##################IEEE C37.118.2 Header Frame#################
def header_str_len(pkt):
    if(hasattr(pkt.underlayer,"framesize")):
        #synphasor() size = 14 bytes | crc 2 bytes
        l = pkt.underlayer.framesize-14-2
        # print("========> My Str Len: ",l)
        return l
    # else:
    #     print("============ No attribute")
    return 0

class synphasor_header(Packet):
    name  = "IEEE C37.118.2 Header"
    fields_desc = [
        # StrLenField("data","", length_from=lambda pkt: (pkt.underlayer.framesize-4)),
        StrLenField("data","", length_from = lambda pkt:header_str_len(pkt)),
        XShortField("chk",None)
    ]

####################### Bind Layers ####################
#0: 'DATA',
#1: 'HEADER',
#2: 'CFG1',
#3: 'CFG2',
#5: 'CFG3',
#4: 'CMD',
bind_layers(TCP,synphasor,sport=4712)
bind_layers(TCP,synphasor,dport=4712)
bind_layers(synphasor,synphasor_data, type = 0) 
bind_layers(synphasor, synphasor_header, type = 1) #type header
bind_layers(synphasor,synphasor_cfg2, type = 3)
bind_layers(synphasor, synphasor_cmd, type = 4) #type CMD

