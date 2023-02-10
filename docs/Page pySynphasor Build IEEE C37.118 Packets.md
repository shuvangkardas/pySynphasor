---
layout: default
title: Build IEEE C37.118 Packet
nav_order: 3
---

## Load the Module
Before using the script, import the module using the following script. Also before using the module, it is recommended to know the basic structure of the IEEE C37.118.2 protocol from [[Page IEEE C37.118 Summary]] page. 
```python
from pySynphasor.synphasor import *
```

## Build a Common Packet

The four packet types and their opcodes are as follows
```python
PACKET_TYPE = {
    0: 'DATA',
    1: 'HEADER',
    2: 'CFG1',
    3: 'CFG2',
    5: 'CFG3',
    4: 'CMD',
}
```

There are two versions of the protocol. The first one is IEEE Std. C37.118-2005 and another one is IEEE Std. C37.118.2-2021. These are defined in the protocol as follows
```python
VERSION = {
    1: 'Version 1', #IEEE Std C37.118-2005
    2: 'Version 2'  #IEEE Std C37.118.2-2011
}
```

The `synphasor` generates the common packet. See the list of arguments for common packet mentioned in the  [[Page IEEE C37.118 Summary]].

```python
CommonPkt = synphasor() # The function takes the  arguments
CommonPkt.show2()       # Prints the arguments in human readable form
```
Output:
```python
###[ IEEE C37.118.2 COMMON FRAME ]### 
  synByte   = 0xaa
  reserved  = 0
  type      = DATA
  version   = Version 2
  framesize = 14
  idcode    = 0
  soc       = 0
  fracsec   = 0
```

The good point is, if you forget yo put any arguments in the common message function, it will take the default arguments. 


Now, create the same packet by defining the message type and PMU ID code
```python
#Type 4 means command type of message and PMU ID =10
commonPkt2 = synphasor(type=4,idcode=10)
commonPkt2.show2()
print("The network packet representation of the message: ")
print(raw(commonPkt2))
```
Output:
```python
###[ IEEE C37.118.2 COMMON FRAME ]### 
  synByte   = 0xaa
  reserved  = 0
  type      = CMD
  version   = Version 2
  framesize = 14
  idcode    = 10
  soc       = 0
  fracsec   = 0

The network packet representation of the message: 
b'\xaaB\x00\x0e\x00\n\x00\x00\x00\x00\x00\x00\x00\x00'
```


## Build a Command Packet
The command packet is very simple to build. It takes only command argument as input. 

```python
cmdPkt = synphasor_cmd(cmd=5) #cmd =5 measns send the CFG2 frame
cmdPkt.show()                  #print the packet
```
Output
```python
###[ synphasor command ]### 
	cmd = 5
	chk = None
```

At this point, let's combine command and command frame to create a complete command message to ask a PMU for sending CFG2 packet. 
```python
cmdPktFull1 = synphasor(type=4,idcode=10)/synphasor_cmd(cmd=5)
cmdPktFull1.show2()
print("The network packet representation of the message: ")
print(raw(cmdPktFull1))
```
Output:
```python
###[ IEEE C37.118.2 COMMON FRAME ]### 
  synByte   = 0xaa
  reserved  = 0
  type      = CMD
  version   = Version 2
  framesize = 18
  idcode    = 10
  soc       = 0
  fracsec   = 0
###[ synphasor command ]### 
     cmd       = 5
     chk       = 0xb6b3

The network packet representation of the message: 
b'\xaaB\x00\x12\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xb6\xb3'
```
At this stage, the checksum is calculated automatically for the packet. If you just observe the last 2 bytes of the binary representation, you see the checksum. Another thing, you need to know that, if you use `pkt1.show()`, you will not see the checksum. `pkt1.show2()` calculates checksum that is dependent of the packet and done in post processing stage. 

Also the same things can be achieved as utilizing the previous instances of common frame and  command frame

```python
cmdPktFull2 = commonPkt2/cmdPkt
cmdPktFull2.show2()
print("The network packet representation of the message: ")
print(raw(cmdPktFull2))
```
The output is same as the previous example. That means, you can create a complete packet part by part and combine finally. It is very useful to make a clean code. 


## Build Data Packet
Building data packet needs a little tweak. You need to understand that a single data frame could send multiple PMUs data. Also, one PMU data could have multiple phasor measurements. Therefore, to deal with this complexity better follow the step by step procedure of building data frame. 

```python
#Create the common frame for data packet,type 0 for data frame
commonFrm = synphasor(type=0, idcode = 10)
#Create the instance of data frame
dataFrm = synphasor_data()              
# Put the PMU data inside dataframe
dataFrm.pmu_data = PMU_DATA(
    phasors=[(1+2j),(3+4j),(5+6j),(7+8j)],
    freq = 2500,
    dfreq = 0,
    analogs = [10,20,30],
    digitals  = [0x3c12]) 

#Build the complete data packet
synDataPkt = commonFrm/dataFrm
synDataPkt.show2()
print("Data packet in machine representation:")
raw(synDataPkt)
```
Output
```python
###[ IEEE C37.118.2 COMMON FRAME ]### 
  synByte   = 0xaa
  reserved  = 0
  type      = DATA
  version   = Version 2
  framesize = 52
  idcode    = 10
  soc       = 0
  fracsec   = 0
###[ IEEE C37.118.2 Data ]### 
     \pmu_data  \
      |###[ PMU Data ]### 
      |  data_error= Good measurement
      |  pmu_sync  = sync with UTC
      |  data_storing= by time stamp
      |  pmu_trigger= trigger detected
      |  cfg_change= change effected
      |  data_modified= otherwise
      |  pmu_time_quality= Not used
      |  unlocked_time= Sync locked or unlocked < 10s
      |  trigger_reason= Magnitude low
      |  phasors   = [(1+2j), (3+4j), (5+6j), (7+8j)]
      |  freq      = 2500
      |  dfreq     = 0
      |  analogs   = [10.0, 20.0, 30.0]
      |  digitals  = [0x3c12]
     chk       = 0xeb68

```


### Multiple PMUs
If you need to put multiple PMUs into the same date packet, here is the code example
```python
#Build the first PMU
pmu1 = PMU_DATA(
    phasors=[(1+2j),(3+4j),(5+6j),(7+8j)],
    freq = 2500,
    dfreq = 0,
    analogs = [10,20,30],
    digitals  = [0x3c12])
#Build the second PMU
pmu2 = PMU_DATA(
    phasors=[(1+2j),(3+4j),(5+6j),(7+8j)],
    freq = 2500,
    dfreq = 0,
    analogs = [10,20,30],
    digitals  = [0x3c12])  

# Create the data packet using two PMU data. Theck checksum is put as dummy.
syndata = synphasor_data(pmu_data=[pmu1, pmu2],chk = 0x1213)
syndata.show()
```
Output
```python
###[ IEEE C37.118.2 Data ]### 
  \pmu_data  \
   |###[ PMU Data ]### 
   |  data_error= Good measurement
   |  pmu_sync  = sync with UTC
   |  data_storing= by time stamp
   |  pmu_trigger= trigger detected
   |  cfg_change= change effected
   |  data_modified= otherwise
   |  pmu_time_quality= Not used
   |  unlocked_time= Sync locked or unlocked < 10s
   |  trigger_reason= Magnitude low
   |  phasors   = [(1+2j), (3+4j), (5+6j), (7+8j)]
   |  freq      = 2500
   |  dfreq     = 0
   |  analogs   = [10, 20, 30]
   |  digitals  = [0x3c12]
   |###[ PMU Data ]### 
   |  data_error= Good measurement
   |  pmu_sync  = sync with UTC
   |  data_storing= by time stamp
   |  pmu_trigger= trigger detected
   |  cfg_change= change effected
   |  data_modified= otherwise
   |  pmu_time_quality= Not used
   |  unlocked_time= Sync locked or unlocked < 10s
   |  trigger_reason= Magnitude low
   |  phasors   = [(1+2j), (3+4j), (5+6j), (7+8j)]
   |  freq      = 2500
   |  dfreq     = 0
   |  analogs   = [10, 20, 30]
   |  digitals  = [0x3c12]
  chk       = 0x1213
```


## Build a Configuration Packet

```python
pktcfg = synphasor_cfg2(
    pmu = [PMU_CFG(
        phname=["Va","Vb"],
        anname=["an0","an1"],
        dgname=[DGNAME(dname1 = "BREAKER X STATUS",dname2="BREAKER Y STATUS")],
        phunit=[PHUNIT(flag=0,phfactor=10),PHUNIT(flag=1,phfactor=20)],
        anunit=[ANUNIT(),ANUNIT()],
        dgunit=[DIGUNIT(),DIGUNIT()])]
 )


cfgFullPkt = synphasor(type=3,)/pktcfg
cfgFullPkt.show()
print("Packet Raw Output")
raw(pktcfg)
```

Output:
```python
###[ IEEE C37.118.2 COMMON FRAME ]### 
  synByte   = 0xaa
  reserved  = 0
  type      = CFG2
  version   = Version 2
  framesize = None
  idcode    = 0
  soc       = None
  fracsec   = None
###[ IEEE C37.118.2 CFG2 ]### 
     TIME_BASE = 0
     num_pmu   = None
     \pmu       \
      |###[ PMU Configuration ]### 
      |  stn       = 'STATION 1       '
      |  idcode    = 0
      |  unused    = 0
      |  freq      = 16-bit integer
      |  analog    = 16-bit integer
      |  phasor_dtype= 16-bit integer
      |  phasor_format= rectangular
      |  phnmr     = None
      |  annmr     = None
      |  dgnmr     = None
      |  phname    = ['Va', 'Vb']
      |  anname    = ['an0', 'an1']
      |  \dgname    \
      |   |###[ digital status name ]### 
      |   |  dname1    = 'BREAKER X STATUS'
      |   |  dname2    = 'BREAKER Y STATUS'
      |   |  dname3    = 'BREAKER 3 STATUS'
      |   |  dname4    = 'BREAKER 4 STATUS'
      |   |  dname5    = 'BREAKER 5 STATUS'
      |   |  dname6    = 'BREAKER 6 STATUS'
      |   |  dname7    = 'BREAKER 7 STATUS'
      |   |  dname8    = 'BREAKER 8 STATUS'
      |   |  dname9    = 'BREAKER 9 STATUS'
      |   |  dname10   = 'BREAKER A STATUS'
      |   |  dname11   = 'BREAKER B STATUS'
      |   |  dname12   = 'BREAKER C STATUS'
      |   |  dname13   = 'BREAKER D STATUS'
      |   |  dname14   = 'BREAKER E STATUS'
      |   |  dname15   = 'BREAKER F STATUS'
      |   |  dname16   = 'BREAKER G STATUS'
      |  \phunit    \
      |   |###[ ('Phasor Conversion Factor',) ]### 
      |   |  flag      = voltage
      |   |  phfactor  = 10
      |   |###[ ('Phasor Conversion Factor',) ]### 
      |   |  flag      = current
      |   |  phfactor  = 20
      |  \anunit    \
      |   |###[ ('Analog Conversion Factor',) ]### 
      |   |  flag      = single point on wave
      |   |  anfactor  = 1
      |   |###[ ('Analog Conversion Factor',) ]### 
      |   |  flag      = single point on wave
      |   |  anfactor  = 1
      |  \dgunit    \
      |   |###[ Digital Status Words ]### 
      |   |  normal_status= 0x0
      |   |  valid_input= 0x0
      |   |###[ Digital Status Words ]### 
      |   |  normal_status= 0x0
      |   |  valid_input= 0x0
      |  reserved  = 0
      |  fnom      = 60Hz
      |  CFGCNT    = 0
     data_rate = 30
     chk       = None
```


## Header Packet

```python
pkt5 = synphasor(type=1,)/synphasor_header(data="This is a sample header from PMU 10")
pkt5.show2()        #Show to packet in huma readble format
print("-------------Network Packet---------------")
print(raw(pkt5))    # Show the network packet in raw format
```

Output:
```python
###[ IEEE C37.118.2 COMMON FRAME ]### 
  synByte   = 0xaa
  reserved  = 0
  type      = HEADER
  version   = Version 2
  framesize = 51
  idcode    = 0
  soc       = 0
  fracsec   = 0
###[ IEEE C37.118.2 Header ]### 
     data      = 'This is a sample header from PMU 10'
     chk       = 0x1035

```









## References